# Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, archive, delete
> When this file exceeds 500 entries, rotate: rename to log-YYYY.md, start fresh.

## [2026-06-18] create | Wiki initialized
- Domain: LLM agent architectures
- Path: ./wiki/
- Structure: raw/ (articles, papers, transcripts, assets), entities/, concepts/, comparisons/, queries/
- Files created: SCHEMA.md, index.md, log.md

## [2026-06-18] ingest | "LLM Powered Autonomous Agents" — Lilian Weng (Jun 2023)
- Source: https://lilianweng.github.io/posts/2023-06-23-agent/
- Raw: raw/articles/lilian-weng-agent-survey-2023.md
- Created 9 wiki pages:
  - concepts/agent-system-overview.md — 3-component agent architecture model
  - concepts/planning-in-agents.md — Task decomposition (CoT, ToT, LLM+P) and self-reflection
  - concepts/memory-in-agents.md — Memory types, vector stores, MIPS/ANN algorithms
  - concepts/tool-use-in-agents.md — MRKL, Toolformer, HuggingGPT, API-Bank
  - concepts/reflection-in-agents.md — ReAct, Reflexion, Chain of Hindsight, Algorithm Distillation
  - entities/react-pattern.md — Reasoning + Acting interleaved pattern
  - entities/auto-gpt.md — Autonomous agent proof-of-concept
  - entities/generative-agents.md — 25-agent Simulacra sandbox
  - entities/hugging-gpt.md — ChatGPT + HuggingFace model orchestration
- Updated: index.md (9 entries), log.md (this entry)

## [2026-06-18] ingest | "LLM Wiki" — Andrej Karpathy (2026)
- Source: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- Raw: raw/articles/karpathy-llm-wiki-2026.md
- Created 2 wiki pages:
  - concepts/wiki-compilation-pattern.md — The Karpathy wiki pattern: compounding knowledge base vs. transient RAG
  - comparisons/rag-vs-compilation.md — Side-by-side comparison of RAG and wiki compilation approaches
- Updated:
  - concepts/memory-in-agents.md — Added "Structured Long-Term Memory: Wiki Compilation" section
- Updated: index.md (12 entries), log.md (this entry)

## [2026-06-18] ingest | "I Built Karpathy's LLM Wiki Twice" — Leandro Bernardo (May 2026)
- Source: https://pub.towardsai.net/i-built-karpathys-llm-wiki-twice-once-as-code-once-as-a-md-heres-what-each-one-gives-up-08b31170999a
- Raw: raw/articles/bernardo-llm-wiki-twice-2026.md
- Created 2 wiki pages:
  - entities/wiki-llm.md — Dual implementation (Python package + AGENTS.md) of the wiki compilation pattern
  - concepts/markdown-pipeline-integrity.md — Structural markdown validation in agent pipelines
- Updated:
  - concepts/wiki-compilation-pattern.md — Added "Programmatic vs. Agentic Implementation" section
- Updated: index.md (14 entries), log.md (this entry)

## [2026-06-19] ingest | "Introducing the Open Knowledge Format" — Google Cloud (Jun 2026)
- Source: https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing
- Raw: raw/articles/google-okf-introducing-2026.md
- Created 1 wiki page:
  - concepts/open-knowledge-format.md — OKF v0.1: formal spec standardizing the wiki pattern for interoperable agent context
- Updated:
  - concepts/wiki-compilation-pattern.md — Added "Standardization: Open Knowledge Format" section
- Updated: index.md (15 entries), log.md (this entry)

## [2026-06-19] query | "What trade-offs do you face when building a production wiki compilation pipeline?"
- Pages consulted: wiki-compilation-pattern, wiki-llm, markdown-pipeline-integrity, rag-vs-compilation, open-knowledge-format
- Synthesis: 4 trade-off dimensions surfaced (programmatic vs. agentic, markdown integrity, ingest/query cost inversion, standardization vs. flexibility)
- Filed: not filed (demonstration query)
- Updated: log.md (this entry)