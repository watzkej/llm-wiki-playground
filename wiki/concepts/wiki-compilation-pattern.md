---
title: Wiki Compilation Pattern
created: 2026-06-18
updated: 2026-06-18
type: concept
tags: [memory, pattern, emerging, survey]
sources: [raw/articles/karpathy-llm-wiki-2026.md]
---

# Wiki Compilation Pattern

The **wiki compilation pattern** (Karpathy, 2026) is an alternative to RAG for LLM-based knowledge management. Instead of retrieving raw document chunks at query time, the LLM incrementally builds and maintains a persistent, interlinked knowledge base.

## Core Idea

> "The LLM incrementally builds and maintains a persistent wiki — a structured, interlinked collection of markdown files that sits between you and the raw sources."

**The key difference from RAG:** Knowledge is compiled once and kept current, not re-derived on every query. The cross-references are already there. The contradictions have already been flagged. The synthesis already reflects everything ingested.

## Three Layers

| Layer | Description | Maintained By |
|---|---|---|
| **Raw Sources** | Immutable source documents — articles, papers, transcripts | Human curator |
| **Wiki Pages** | Interlinked markdown files — entities, concepts, comparisons | LLM agent |
| **Schema** | Conventions, tag taxonomy, page thresholds | Human + LLM |

The division of labor: the human curates sources and directs analysis; the LLM summarizes, cross-references, files, and maintains consistency.

## vs. RAG

| Dimension | RAG | Wiki Compilation |
|---|---|---|
| Knowledge state | Re-derived per query | Persists and compounds |
| Cross-references | None (chunks are isolated) | Built into every page |
| Contradictions | Silently returned | Flagged and tracked |
| Synthesis | Shallow (chunk-level) | Deep (all sources integrated) |
| Query cost | Per-query retrieval + synthesis | Per-query: read pre-built pages |

## Use Cases

- **Research** — going deep on a topic over weeks, building an evolving thesis
- **Reading a book** — filing chapters, building character/theme/plot pages
- **Personal knowledge** — journal entries, articles, podcast notes into structured self-knowledge
- **Business/team** — internal wiki fed by Slack, meetings, documents; LLM does the maintenance
- **Competitive analysis, due diligence, trip planning, course notes**

## Relevance to Agent Architecture

The wiki compilation pattern has implications for [[memory-in-agents]]: it's a **structured long-term memory system** where the agent doesn't just retrieve facts — it actively maintains a knowledge base, resolving contradictions and updating syntheses. This is a higher bar than vector-store retrieval and represents a more agentic approach to knowledge management.

## Programmatic vs. Agentic Implementation

The [[wiki-llm|same pattern can be implemented two ways]] (Bernardo, 2026):

- **Programmatic (Python package):** Deterministic, reproducible, production-grade. Pydantic contracts between stages, content-addressable IDs, markdown structural validation. Best for large corpora and scheduled pipelines where token cost and audit trails matter.
- **Agentic (AGENTS.md):** Single file, drop-in, no infrastructure. The agent follows the same Writer → Evaluator → Editor → Lint → Repair loop, but all enforcement is by convention rather than code. Best for small wikis and rapid iteration.

Both produce comparable output quality — Karpathy's loop is robust enough either way. The trade-off is in infrastructure, determinism, and [[markdown-pipeline-integrity|structural reliability]].

## Tooling

The wiki directory works as an Obsidian vault — `[[wikilinks]]` render as clickable links, Graph View shows the knowledge network, and YAML frontmatter powers Dataview queries. Karpathy's workflow: "LLM agent open on one side, Obsidian open on the other."

## Standardization: Open Knowledge Format

In June 2026, Google Cloud published the [[open-knowledge-format|Open Knowledge Format (OKF) v0.1]], formalizing the wiki compilation pattern into an interoperable standard. OKF specifies a directory of markdown files with standardized YAML frontmatter fields (`type`, `title`, `description`, `resource`, `tags`, `timestamp`) — making wikis built by different producers consumable by different agents without translation.

This represents the pattern's evolution from an idea file into a formal spec, with three design principles: minimally opinionated, producer/consumer independence, and format-not-platform.

## Related

- [[memory-in-agents]] — Wiki compilation as structured long-term memory
- [[agent-system-overview]] — Where knowledge management fits in agent architecture
- [[rag-vs-compilation]] — Side-by-side comparison of the two approaches
- [[open-knowledge-format]] — The formal standard based on this pattern
- [[wiki-llm]] — Dual implementation of the wiki compilation pipeline

^[raw/articles/karpathy-llm-wiki-2026.md]
^[raw/articles/google-okf-introducing-2026.md]
