---
title: RAG vs Wiki Compilation
created: 2026-06-18
updated: 2026-06-18
type: comparison
tags: [comparison, memory, pattern]
sources: [raw/articles/karpathy-llm-wiki-2026.md]
---

# RAG vs Wiki Compilation

Two fundamentally different approaches to LLM knowledge management.

## Comparison

| Dimension | RAG (Retrieval-Augmented Generation) | Wiki Compilation (Karpathy) |
|---|---|---|
| **Knowledge state** | Transient — re-derived on every query | Persistent — compounds over time |
| **Storage** | Vector database of document chunks | Interlinked markdown files |
| **Cross-references** | None — chunks are isolated fragments | Rich — every page links to 2+ others |
| **Contradictions** | Silently returned; no tracking | Explicitly flagged in frontmatter |
| **Synthesis depth** | Shallow — chunk-level recombination | Deep — all sources integrated into coherent pages |
| **Query cost** | Retrieval + synthesis every query | Read pre-built pages; synthesis already done |
| **Ingest cost** | Low — embed and store | High — LLM reads, extracts, cross-references, writes |
| **Aging** | Chunks never stale but never updated | Pages actively maintained; contradictions surfaced |
| **Maintainer** | System (indexing pipeline) | LLM agent (active curation) |
| **Best for** | Large corpora, fast-changing content, simple fact lookup | Deep research, long-term projects, complex synthesis |

## When to Use Which

**Choose RAG when:**
- You have a massive corpus (thousands of documents)
- Content changes frequently and re-indexing is cheap
- Queries are simple fact-retrieval ("What is X?")
- You don't need cross-document synthesis

**Choose Wiki Compilation when:**
- You're going deep on a bounded domain (dozens to hundreds of sources)
- You need cross-document synthesis and contradiction detection
- Knowledge should compound over time
- You want human-browsable, linkable artifacts
- You're building a thesis, not just answering questions

## Hybrid Approaches

The two aren't mutually exclusive. A hybrid could:
- Use RAG for initial discovery ("find me papers about X")
- Use wiki compilation for deep integration ("ingest these 5 papers into the wiki")
- Use RAG as a fallback when the wiki has no relevant pages

## Related

- [[wiki-compilation-pattern]] — Full concept deep dive
- [[memory-in-agents]] — Both approaches as memory systems
- [[agent-system-overview]] — Knowledge management in agent architecture

^[raw/articles/karpathy-llm-wiki-2026.md]
