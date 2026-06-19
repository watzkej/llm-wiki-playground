---
title: Memory in Agents
created: 2026-06-18
updated: 2026-06-18
type: concept
tags: [memory, framework]
sources: [raw/articles/lilian-weng-agent-survey-2023.md]
---

# Memory in Agents

Memory in LLM agents draws inspiration from human cognitive architecture and provides the agent with persistent context beyond the transformer's finite attention window.

## Memory Types

| Human Memory | Agent Mapping | Characteristics |
|---|---|---|
| **Sensory Memory** | Embedding representations | Raw input encoding (text, image, audio); lasts seconds |
| **Short-Term Memory (STM)** | In-context learning | ~7 items; limited by context window length of Transformer |
| **Long-Term Memory (LTM)** | External vector store | Unlimited capacity; explicit (facts/events) and implicit (skills) |

## Long-Term Memory: Vector Stores & MIPS

The standard implementation uses embedding vectors stored in a database supporting fast **Maximum Inner Product Search (MIPS)**. Approximate Nearest Neighbor (ANN) algorithms trade a small accuracy loss for large speedups:

| Algorithm | Approach |
|---|---|
| **LSH** | Hash similar items to same buckets |
| **ANNOY** | Random projection trees; binary search through half-spaces |
| **HNSW** | Hierarchical small-world graphs with shortcut layers |
| **FAISS** | Vector quantization; cluster partitioning then refinement |
| **ScaNN** | Anisotropic vector quantization optimized for inner product |

## Retrieval Quality Dimensions

In the [[generative-agents]] framework (Park et al. 2023), the retrieval model scores memories along three axes:
- **Recency** — recent events score higher
- **Importance** — distinguish mundane from core memories (ask the LLM directly)
- **Relevance** — embedding similarity to the current situation/query

## Structured Long-Term Memory: Wiki Compilation

Beyond vector stores, the [[wiki-compilation-pattern]] (Karpathy, 2026) offers a **structured alternative**: instead of retrieving raw chunks, the agent maintains a persistent, interlinked knowledge base of markdown files. This is a higher-order memory system where:
- Knowledge is compiled once, not re-derived per query
- Cross-references are built into every page
- Contradictions are explicitly flagged and tracked
- The knowledge base compounds with every source

See [[rag-vs-compilation]] for a detailed comparison.

## Related

- [[agent-system-overview]] — Memory's role in the 3-component model
- [[generative-agents]] — Memory stream architecture in practice
- [[tool-use-in-agents]] — Complementary external capability
- [[wiki-compilation-pattern]] — Structured long-term memory via compiled wiki

^[raw/articles/lilian-weng-agent-survey-2023.md]
^[raw/articles/karpathy-llm-wiki-2026.md]
