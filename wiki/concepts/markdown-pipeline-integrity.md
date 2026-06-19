---
title: Markdown Pipeline Integrity
created: 2026-06-18
updated: 2026-06-18
type: concept
tags: [pattern, deployment, emerging]
sources: [raw/articles/bernardo-llm-wiki-twice-2026.md]
---

# Markdown Pipeline Integrity

When LLM agents produce Markdown as intermediate output in a pipeline, structural noise — malformed headings, broken links, invalid frontmatter — propagates and corrupts every downstream stage. This is a neglected failure mode in agent architectures that generate and consume structured text.

## The Problem

LLM-generated Markdown is **plausible but not reliable**:

| Failure | Impact on Pipeline |
|---|---|
| Drifting heading hierarchy (two H1s, skipped levels) | Chunker misroutes overlap across sections |
| Broken wikilinks (point to non-existent pages) | Navigation and cross-reference chains break |
| Invalid YAML frontmatter (unquoted colons) | Dataview queries, indexers, parsers fail |
| Inconsistent section ordering between regenerations | Deduplicator merges wrong pages |
| Syntactically valid but semantically wrong structure | Lint pass reports unfixable problems |

In a compounding system like [[wiki-compilation-pattern|Karpathy's wiki]], every page becomes input to topics, groups, the index, and the chat retriever. Structural noise is **not cosmetic** — it's correctness-critical.

## The Solution: Structured Markdown Processing

Bernardo's `markdown-hero` library (Python, 2026) addresses this with:

- **Type-checked Markdown** — headings, links, frontmatter validated against a schema
- **Section-aware chunking** — overlap windows stay within heading boundaries
- **Deduplication with heading awareness** — `markdown_merge(dedupe_headings=True)` prevents structural collisions
- **Multilingual support** — same guarantees across languages
- **Pipeline integration** — every page passes through `lint()` before leaving the Generate stage

## Agentic vs. Programmatic Approaches

The [[wiki-llm|programmatic version]] can enforce these guarantees because markdown-hero runs as compiled code between pipeline stages. The [[wiki-llm|agentic version]] asks the agent to follow conventions and trusts the output — which works for most use cases but fails when the wiki feeds downstream automation.

> "This is one of the few places where the programmatic version is not a heavier alternative — it's a different _capability_." — Bernardo

## Relevance to Agent Architecture

This pattern generalizes beyond markdown: any agent pipeline where structured output feeds another stage needs **output validation** between stages. This is the same principle as [[tool-use-in-agents|function calling]] requiring structured JSON — but applied to the agent's own internal outputs rather than external API calls.

## Related

- [[wiki-llm]] — The dual implementation that motivated markdown-hero
- [[wiki-compilation-pattern]] — Why compounding makes structural noise critical
- [[tool-use-in-agents]] — Structured output as a general agent capability
- [[reflection-in-agents]] — Self-critique could detect structural issues, but programmatic validation is more reliable

^[raw/articles/bernardo-llm-wiki-twice-2026.md]
