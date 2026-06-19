#!/usr/bin/env python3
"""
LLM Wiki RSS Watcher — monitors RSS/Atom feeds, saves new posts to raw/articles/,
and outputs a summary for the agent to ingest.

Config: wiki/rss-watcher-config.json — list of feeds to monitor
State:  wiki/.rss-state.json — tracks seen article GUIDs/URLs

Strategy:
- On first run for a feed: only save articles within `window_days` (default 30).
  Mark ALL articles as "seen" so we don't re-import them later.
- On subsequent runs: only save truly new articles (not in state).
"""

import feedparser
import hashlib
import json
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.parse import urlparse


def slugify(text):
    import re
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    return text[:80]


def load_config(config_path):
    if not os.path.exists(config_path):
        print(f"ERROR: Config file not found: {config_path}", file=sys.stderr)
        sys.exit(1)
    with open(config_path) as f:
        return json.load(f)


def load_state(state_path):
    if os.path.exists(state_path):
        with open(state_path) as f:
            return json.load(f)
    return {"seen": {}, "last_run": None}


def save_state(state_path, state):
    tmp = state_path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, indent=2)
    os.replace(tmp, state_path)


def fetch_feed(name, url):
    """Fetch and parse a feed. Returns list of article dicts."""
    try:
        f = feedparser.parse(url)
    except Exception as e:
        print(f"  [{name}] ERROR: {e}", file=sys.stderr)
        return []

    if not f.entries:
        if hasattr(f, 'bozo_exception'):
            print(f"  [{name}] Feed warning: {f.bozo_exception}", file=sys.stderr)
        return []

    articles = []
    for entry in f.entries:
        article_id = entry.get('id') or entry.get('link') or hashlib.sha256(
            (entry.get('title', '') + entry.get('link', '')).encode()
        ).hexdigest()[:16]

        pub_date = None
        for df in ['published_parsed', 'updated_parsed']:
            if entry.get(df):
                pub_date = datetime(*entry[df][:6], tzinfo=timezone.utc)
                break
        if not pub_date:
            pub_date = datetime.now(timezone.utc)

        content = ""
        if entry.get('content'):
            content = entry.content[0].get('value', '')
        elif entry.get('summary'):
            content = entry.summary
        elif entry.get('description'):
            content = entry.description

        import re
        content = re.sub(r'<[^>]+>', '', content)
        content = re.sub(r'\n{3,}', '\n\n', content)
        content = content.strip()

        articles.append({
            "id": article_id,
            "title": entry.get('title', 'Untitled'),
            "url": entry.get('link', ''),
            "published": pub_date.isoformat(),
            "published_dt": pub_date,
            "content": content[:50000],
            "blog_name": name,
        })

    return articles


def save_article(wiki_raw_dir, article):
    date_str = article['published'][:10]
    title_slug = slugify(article['title'])[:60]
    blog_slug = slugify(article['blog_name'])[:20]
    filename = f"{date_str}-{blog_slug}-{title_slug}.md"
    filepath = os.path.join(wiki_raw_dir, filename)

    body = f"# {article['title']}\n\n"
    body += f"> Source: {article['url']}\n"
    body += f"> Published: {article['published'][:10]}\n"
    body += f"> Blog: {article['blog_name']}\n\n"
    body += article['content']

    body_hash = hashlib.sha256(body.encode()).hexdigest()

    raw_content = f"""---
source_url: {article['url']}
ingested: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}
sha256: {body_hash}
---

{body}
"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(raw_content)

    return filepath, body_hash


def main():
    # Use WIKI_PATH env var if set, otherwise look for wiki/ relative to cwd
    wiki_dir = os.environ.get("WIKI_PATH", os.path.join(os.getcwd(), "wiki"))
    cwd = os.getcwd()
    config_path = os.path.join(wiki_dir, "rss-watcher-config.json")
    state_path = os.path.join(wiki_dir, ".rss-state.json")
    raw_dir = os.path.join(wiki_dir, "raw", "articles")

    os.makedirs(raw_dir, exist_ok=True)

    config = load_config(config_path)
    feeds = config.get("feeds", [])
    default_window = config.get("default_window_days", 30)

    if not feeds:
        print("No feeds configured.")
        sys.exit(0)

    state = load_state(state_path)
    if "seen" not in state:
        state["seen"] = {}

    now = datetime.now(timezone.utc)
    window_cutoff = now - timedelta(days=default_window)

    print(f"Scanning {len(feeds)} feed(s)...")
    new_articles = []

    for feed_def in feeds:
        name = feed_def["name"]
        url = feed_def["url"]
        window_days = feed_def.get("window_days", default_window)
        feed_cutoff = now - timedelta(days=window_days)

        feed_state = state["seen"].get(name, {"article_ids": [], "first_seen": None})
        is_first_run = feed_state["first_seen"] is None

        print(f"  [{name}] Fetching...", end=" ")
        articles = fetch_feed(name, url)
        print(f"{len(articles)} articles")

        all_ids = []
        for article in articles:
            all_ids.append(article["id"])

            if article["id"] in feed_state.get("article_ids", []):
                continue  # Already seen

            article_is_recent = article["published_dt"] >= feed_cutoff if article["published_dt"] else False

            if is_first_run and article_is_recent:
                # First run + recent: save it
                new_articles.append(article)
                # Don't mark as seen yet — we'll do that after saving

        # Mark ALL articles as seen for this feed
        feed_state["article_ids"] = all_ids
        if is_first_run:
            feed_state["first_seen"] = now.isoformat()
        state["seen"][name] = feed_state

    # Save state before processing so we don't re-download on failure
    state["last_run"] = now.isoformat()
    save_state(state_path, state)

    if not new_articles:
        print("\nNo new articles to ingest.")
        return

    print(f"\n=== {len(new_articles)} new article(s) to ingest ===\n")

    saved_files = []
    for article in new_articles:
        filepath, body_hash = save_article(raw_dir, article)
        saved_files.append(filepath)
        print(f"  [{article['blog_name']}] {article['title'][:80]}")
        print(f"      → {os.path.relpath(filepath, cwd)}")
        print()

    print(f"Saved {len(saved_files)} new article(s) to wiki/raw/articles/")
    print("FILES:", "|".join(os.path.relpath(f, cwd) for f in saved_files))


if __name__ == "__main__":
    main()
