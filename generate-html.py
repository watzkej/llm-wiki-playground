#!/usr/bin/env python3
"""
Generate a self-contained HTML wiki browser from the LLM wiki markdown files.
Output: wiki-browser.html — open in any browser.
"""

import re, json, os, sys

WIKI_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wiki")

def parse_page(filepath):
    """Parse a wiki markdown file into frontmatter dict and body text."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    fm = {}
    body = content
    fm_match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if fm_match:
        for line in fm_match.group(1).strip().split('\n'):
            kv = re.match(r'^(\w+):\s*(.+)', line)
            if kv:
                key = kv.group(1)
                val = kv.group(2).strip()
                if val.startswith('[') and val.endswith(']'):
                    val = [v.strip() for v in val[1:-1].split(',')]
                fm[key] = val
        body = fm_match.group(2)
    
    # Convert markdown body to HTML
    html = body
    
    # Provenance markers
    html = re.sub(r'\^\[(raw/[^\]]+)\]', r'<sup class="provenance">[\1]</sup>', html)
    
    # Wikilinks
    html = re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]', r'<a href="#" class="wikilink" data-page="\1">\2</a>', html)
    html = re.sub(r'\[\[([^\]]+)\]\]', r'<a href="#" class="wikilink" data-page="\1">\1</a>', html)
    
    # External links
    html = re.sub(r'\[([^\]]+)\]\(((?!raw/)[^)]+)\)', r'<a href="\2" target="_blank" class="extlink">\1</a>', html)
    
    # Images
    html = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1" class="content-img">', html)
    
    # Headings
    html = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # Code blocks
    html = re.sub(r'```(.*?)```', r'<pre><code>\1</code></pre>', html, flags=re.DOTALL)
    
    # Inline code
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    
    # Bold / italic
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', html)
    
    # Horizontal rules
    html = re.sub(r'^---$', r'<hr>', html, flags=re.MULTILINE)
    
    # Blockquotes
    html = re.sub(r'^> (.+)$', r'<blockquote><p>\1</p></blockquote>', html, flags=re.MULTILINE)
    
    # Tables (pipe-separated)
    table_lines = []
    in_table = False
    result_lines = []
    for line in html.split('\n'):
        if re.match(r'^\|.+\|$', line.strip()):
            if not in_table:
                in_table = True
                table_lines = ['<table>']
            is_sep = re.match(r'^\|[\s\-:]+\|$', line.strip().replace('|', '|'))
            if not is_sep:
                cells = [c.strip() for c in line.strip().split('|')[1:-1]]
                row = '<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>'
                table_lines.append(row)
            continue
        else:
            if in_table:
                table_lines.append('</table>')
                result_lines.extend(table_lines)
                in_table = False
                table_lines = []
            result_lines.append(line)
    if in_table:
        table_lines.append('</table>')
        result_lines.extend(table_lines)
    html = '\n'.join(result_lines)
    
    # Lists
    html = re.sub(r'^- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'(<li>.*?</li>\n?)+', r'<ul>\g<0></ul>', html)
    
    # Paragraph wrapping
    parts = html.split('\n\n')
    wrapped = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if re.match(r'^<(h[1-4]|pre|table|ul|ol|blockquote|hr)', p):
            wrapped.append(p)
        else:
            wrapped.append(f'<p>{p}</p>')
    html = '\n'.join(wrapped)
    
    return {
        "title": fm.get('title', ''),
        "type": fm.get('type', ''),
        "tags": fm.get('tags', []) if isinstance(fm.get('tags', []), list) else [fm.get('tags', '')],
        "html": html,
        "created": fm.get('created', ''),
        "updated": fm.get('updated', ''),
        "confidence": fm.get('confidence', ''),
        "contested": fm.get('contested', ''),
        "sources": fm.get('sources', []),
    }


def collect_pages(wiki_dir):
    """Collect all wiki pages from concepts/, entities/, comparisons/, queries/."""
    pages = {}
    for dir_name in ["concepts", "entities", "comparisons", "queries"]:
        dir_path = os.path.join(wiki_dir, dir_name)
        if not os.path.exists(dir_path):
            continue
        for fname in sorted(os.listdir(dir_path)):
            if not fname.endswith('.md'):
                continue
            slug = fname.replace('.md', '')
            filepath = os.path.join(dir_path, fname)
            pages[slug] = parse_page(filepath)
    return pages


def parse_index(wiki_dir):
    """Parse index.md into sections."""
    index_path = os.path.join(wiki_dir, "index.md")
    if not os.path.exists(index_path):
        return {"entities": [], "concepts": [], "comparisons": [], "queries": []}
    
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    sections = {"entities": [], "concepts": [], "comparisons": [], "queries": []}
    current = None
    for line in content.split('\n'):
        m = re.match(r'^## (Entities|Concepts|Comparisons|Queries)', line)
        if m:
            current = m.group(1).lower()
        elif current and line.startswith('- [['):
            m2 = re.match(r'- \[\[([^\]]+)\]\] — (.+)', line)
            if m2:
                sections[current].append({"slug": m2.group(1), "summary": m2.group(2)})
    return sections


def generate_html(pages, sections):
    """Generate the full self-contained HTML."""
    pages_js = json.dumps(pages)
    sections_js = json.dumps(sections)
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>LLM Wiki — Agent Architectures</title>
<style>
:root {{
    --bg: #1e1e2e;
    --bg2: #282840;
    --bg3: #313150;
    --text: #cdd6f4;
    --text2: #a6adc8;
    --text3: #6c7086;
    --accent: #89b4fa;
    --accent2: #cba6f7;
    --green: #a6e3a1;
    --yellow: #f9e2af;
    --red: #f38ba8;
    --border: #45475a;
    --link: #89b4fa;
    --link-hover: #b4d0fb;
    --tag-bg: #313150;
    --provenance: #6c7086;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    display: flex;
    height: 100vh;
    overflow: hidden;
}}
a {{ color: var(--link); text-decoration: none; }}
a:hover {{ color: var(--link-hover); text-decoration: underline; }}

/* === SIDEBAR === */
.sidebar {{
    width: 320px;
    min-width: 320px;
    background: var(--bg2);
    border-right: 1px solid var(--border);
    overflow-y: auto;
    padding: 20px;
}}
.sidebar h1 {{
    font-size: 1.2em;
    margin-bottom: 4px;
    color: var(--accent2);
}}
.sidebar .subtitle {{
    font-size: 0.75em;
    color: var(--text3);
    margin-bottom: 20px;
}}
.sidebar h2 {{
    font-size: 0.7em;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text3);
    margin: 16px 0 6px 0;
    padding-top: 12px;
    border-top: 1px solid var(--border);
}}
.sidebar h2:first-of-type {{
    border-top: none;
    padding-top: 0;
}}
.sidebar-item {{
    display: block;
    padding: 4px 8px;
    margin: 1px 0;
    border-radius: 4px;
    font-size: 0.85em;
    cursor: pointer;
    color: var(--text);
}}
.sidebar-item:hover {{
    background: var(--bg3);
    color: var(--link-hover);
    text-decoration: none;
}}
.sidebar-item .type-badge {{
    display: inline-block;
    font-size: 0.65em;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 1px 5px;
    border-radius: 3px;
    margin-right: 6px;
    vertical-align: middle;
}}
.type-entity {{ background: #45475a; color: #89b4fa; }}
.type-concept {{ background: #313150; color: #a6e3a1; }}
.type-comparison {{ background: #45475a; color: #f9e2af; }}
.type-query {{ background: #313150; color: #cba6f7; }}

.sidebar-stats {{
    font-size: 0.7em;
    color: var(--text3);
    margin-top: 20px;
    padding-top: 12px;
    border-top: 1px solid var(--border);
}}

/* === MAIN CONTENT === */
.main {{
    flex: 1;
    overflow-y: auto;
    padding: 40px 60px;
}}
.main h1 {{ font-size: 2em; color: var(--accent2); margin-bottom: 8px; }}
.main h2 {{ font-size: 1.4em; color: var(--accent); margin: 32px 0 12px 0; padding-bottom: 4px; border-bottom: 1px solid var(--border); }}
.main h3 {{ font-size: 1.1em; color: var(--text); margin: 24px 0 8px 0; }}
.main h4 {{ font-size: 1em; color: var(--text2); margin: 16px 0 6px 0; }}
.main p {{ line-height: 1.7; margin: 8px 0; }}
.main ul, .main ol {{ margin: 8px 0 8px 20px; }}
.main li {{ line-height: 1.6; margin: 2px 0; }}
.main table {{
    border-collapse: collapse;
    width: 100%;
    margin: 12px 0;
    font-size: 0.9em;
}}
.main th, .main td {{
    border: 1px solid var(--border);
    padding: 6px 10px;
    text-align: left;
}}
.main th {{ background: var(--bg3); color: var(--accent); font-weight: 600; }}
.main blockquote {{
    border-left: 3px solid var(--accent);
    padding: 4px 16px;
    margin: 12px 0;
    color: var(--text2);
    background: var(--bg2);
    border-radius: 0 4px 4px 0;
}}
.main code {{
    background: var(--bg3);
    padding: 2px 6px;
    border-radius: 3px;
    font-size: 0.9em;
    font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
}}
.main pre {{
    background: var(--bg3);
    padding: 12px 16px;
    border-radius: 6px;
    overflow-x: auto;
    margin: 12px 0;
}}
.main pre code {{ background: none; padding: 0; }}
.main hr {{ border: none; border-top: 1px solid var(--border); margin: 16px 0; }}
.main sup.provenance {{
    font-size: 0.7em;
    color: var(--provenance);
    cursor: help;
}}
.main sup.provenance:hover {{ color: var(--text2); }}

/* === PAGE META === */
.page-meta {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;
    margin: 8px 0 20px 0;
    font-size: 0.8em;
    color: var(--text3);
}}
.page-meta .tag {{
    background: var(--tag-bg);
    padding: 2px 8px;
    border-radius: 3px;
    font-size: 0.85em;
}}
.page-meta .confidence-high {{ color: var(--green); }}
.page-meta .confidence-medium {{ color: var(--yellow); }}
.page-meta .confidence-low {{ color: var(--red); }}

/* === WELCOME PAGE === */
.welcome {{
    max-width: 700px;
}}
.welcome h1 {{ font-size: 2.5em; margin-bottom: 12px; }}
.welcome p {{ font-size: 1.05em; line-height: 1.7; }}
.welcome .quick-links {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin: 24px 0;
}}
.welcome .quick-link {{
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px;
    cursor: pointer;
    transition: border-color 0.2s;
}}
.welcome .quick-link:hover {{
    border-color: var(--accent);
    text-decoration: none;
}}
.welcome .quick-link strong {{ color: var(--accent); }}

/* Scrollbar */
::-webkit-scrollbar {{ width: 8px; }}
::-webkit-scrollbar-track {{ background: var(--bg); }}
::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 4px; }}

/* Mobile */
@media (max-width: 768px) {{
    body {{ flex-direction: column; }}
    .sidebar {{ width: 100%; min-width: 0; max-height: 40vh; }}
    .main {{ padding: 20px; }}
}}
</style>
</head>
<body>

<nav class="sidebar">
    <h1>🧠 LLM Wiki</h1>
    <div class="subtitle">Agent Architectures — 15 pages</div>

    <h2>Entities</h2>
    <div id="nav-entities"></div>

    <h2>Concepts</h2>
    <div id="nav-concepts"></div>

    <h2>Comparisons</h2>
    <div id="nav-comparisons"></div>

    <h2>Queries</h2>
    <div id="nav-queries"></div>

    <div class="sidebar-stats">
        <a href="#" onclick="showPage('_home')">← Wiki Home</a><br>
        4 sources · 15 pages · cron every 12h
    </div>
</nav>

<main class="main" id="content"></main>

<script>
const PAGES = {pages_js};
const SECTIONS = {sections_js};

// Build sidebar navigation
function buildNav() {{
    const typeLabels = {{ entities: 'entity', concepts: 'concept', comparisons: 'comparison', queries: 'query' }};
    for (const [section, items] of Object.entries(SECTIONS)) {{
        const container = document.getElementById('nav-' + section);
        if (!container) continue;
        items.forEach(item => {{
            const page = PAGES[item.slug];
            const typeClass = page ? 'type-' + page.type : '';
            const link = document.createElement('a');
            link.className = 'sidebar-item';
            link.href = '#';
            link.onclick = (e) => {{ e.preventDefault(); showPage(item.slug); }};
            link.title = item.summary;
            const badge = document.createElement('span');
            badge.className = 'type-badge ' + typeClass;
            badge.textContent = page ? page.type : typeLabels[section] || '';
            link.appendChild(badge);
            link.appendChild(document.createTextNode(page ? page.title : item.slug));
            container.appendChild(link);
        }});
    }}
}}

function showPage(slug) {{
    const main = document.getElementById('content');
    if (slug === '_home') {{
        return showHome();
    }}

    const page = PAGES[slug];
    if (!page) {{
        main.innerHTML = `<div class="welcome">
            <h1>Page not found</h1>
            <p>The page <code>[[${{slug}}]]</code> does not exist yet. 
            This is a growth target — ingest a source covering this topic to create it.</p>
            <p><a href="#" onclick="showPage('_home')">← Back to home</a></p>
        </div>`;
        return;
    }}

    let tagsHtml = '';
    if (page.tags && page.tags.length > 0) {{
        tagsHtml = page.tags.filter(t => t).map(t => `<span class="tag">${{t}}</span>`).join('');
    }}

    let confidenceHtml = '';
    if (page.confidence) {{
        confidenceHtml = `<span class="confidence-${{page.confidence}}">confidence: ${{page.confidence}}</span>`;
    }}

    let sourcesHtml = '';
    if (page.sources && page.sources.length > 0) {{
        sourcesHtml = '<span>📎 ' + page.sources.map(s => s.replace('raw/articles/', '')).join(', ') + '</span>';
    }}

    let updatedHtml = page.updated ? `<span>updated: ${{page.updated}}</span>` : '';

    main.innerHTML = `
        <h1>${{page.title}}</h1>
        <div class="page-meta">
            <span class="type-badge type-${{page.type}}">${{page.type}}</span>
            ${{tagsHtml}}
            ${{confidenceHtml}}
            ${{sourcesHtml}}
            ${{updatedHtml}}
        </div>
        ${{page.html}}
    `;

    // Wire up wikilink clicks
    main.querySelectorAll('a.wikilink').forEach(link => {{
        link.onclick = (e) => {{
            e.preventDefault();
            const target = link.getAttribute('data-page');
            if (target) showPage(target);
        }};
    }});

    // Scroll to top
    main.scrollTop = 0;
}}

function showHome() {{
    const main = document.getElementById('content');
    let quickLinks = '';
    const hubs = ['agent-system-overview', 'wiki-compilation-pattern', 'planning-in-agents', 'react-pattern'];
    hubs.forEach(slug => {{
        const page = PAGES[slug];
        if (page) {{
            quickLinks += `
                <div class="quick-link" onclick="showPage('${{slug}}')">
                    <strong>${{page.title}}</strong><br>
                    <small style="color: var(--text3);">${{page.type}} · ${{(page.tags||[]).slice(0,3).join(', ')}}</small>
                </div>`;
        }}
    }});

    main.innerHTML = `
        <div class="welcome">
            <h1>🧠 LLM Agent Architectures Wiki</h1>
            <p>A compounding knowledge base on <strong>LLM agent architectures</strong>, 
            maintained by an AI agent using <a href="https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f" target="_blank">Karpathy's LLM Wiki pattern</a>.</p>
            <p>15 interlinked pages across 4 ingested sources. Updated every 12 hours via automated RSS pipeline.</p>

            <h3>Start Here</h3>
            <div class="quick-links">
                ${{quickLinks}}
            </div>

            <h3>How This Works</h3>
            <table>
                <tr><th>Layer</th><th>Purpose</th><th>Maintainer</th></tr>
                <tr><td>Raw sources</td><td>Immutable source material with SHA256 provenance</td><td>Human curator</td></tr>
                <tr><td>Wiki pages</td><td>Interlinked markdown built by the agent</td><td>LLM agent</td></tr>
                <tr><td>Schema</td><td>Conventions, tag taxonomy, page thresholds</td><td>Human + LLM</td></tr>
            </table>

            <h3>Ingested Sources</h3>
            <ul>
                <li><strong>Lilian Weng</strong> — "LLM Powered Autonomous Agents" (Jun 2023) → 9 pages</li>
                <li><strong>Andrej Karpathy</strong> — "LLM Wiki" gist (2026) → 2 pages</li>
                <li><strong>Leandro Bernardo</strong> — "I Built Karpathy's LLM Wiki Twice" (May 2026) → 2 pages</li>
                <li><strong>Google Cloud</strong> — "Introducing the Open Knowledge Format" (Jun 2026) → 1 page</li>
            </ul>

            <p style="margin-top: 24px; color: var(--text3); font-size: 0.85em;">
                Browse via the sidebar → or click any [[wikilink]] to navigate.<br>
                Open in <a href="obsidian://open?path=${{encodeURI(WIKI_DIR)}}" target="_blank">Obsidian</a> for graph view and backlinks.
            </p>
        </div>`;
}}

// Initialize
buildNav();
showHome();
</script>

</body>
</html>'''.replace('{{WIKI_DIR}}', WIKI_DIR.replace('\\', '/'))


def main():
    pages = collect_pages(WIKI_DIR)
    sections = parse_index(WIKI_DIR)
    html = generate_html(pages, sections)

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wiki-browser.html")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Generated: {output_path}")
    print(f"Size: {len(html):,} bytes")
    print(f"Pages: {len(pages)}")


if __name__ == "__main__":
    main()