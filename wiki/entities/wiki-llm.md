---
title: wiki_llm
created: 2026-06-18
updated: 2026-06-18
type: entity
tags: [framework, pattern, memory, deployment]
sources: [raw/articles/bernardo-llm-wiki-twice-2026.md, raw/articles/karpathy-llm-wiki-2026.md]
confidence: medium
---

# wiki_llm

**wiki_llm** (Leandro Bernardo, 2026) is a dual implementation of Karpathy's [[wiki-compilation-pattern]] — available as both a Python package (`wiki-llm`) and a single `AGENTS.md` file. It's a case study in the **programmatic vs. agentic** trade-off for knowledge compilation pipelines.

## Two Implementations, One Pattern

Both implement the same eight-stage pipeline derived from Karpathy's gist:

```
Writer → Evaluator → Editor → Lint → Repair → (loop)
```

### Programmatic Version (`wiki-llm` Python package)

- **Pydantic v2 contracts** between stages — typed inputs/outputs enforced, not hoped for
- **Deterministic content-addressable IDs** — UUIDs derived from SHA-256 of page body; same content, same ID regardless of filename
- **Multi-backend LLM** via `instructor` — OpenRouter, OpenAI, Bedrock, Ollama; structured outputs with automatic retries
- **Repair agent** built with LangGraph — fan-out and review for lint findings
- **BM25 retrieval** instead of vector store — lexical search is fast, transparent, and sufficient for wiki-scale corpora
- **markdown-hero layer** — type-checked, section-aware markdown processing (see [[markdown-pipeline-integrity]])
- **Production-ready**: Kubernetes CronJob, Docker, single `WikiConfig` module

### Agentic Version (`AGENTS.md`)

- Single file dropped into any project root — works with Claude Code, Codex, Cursor, VS Code Agent Mode
- Same eight stages, same conventions, same `[[wikilinks]]`
- **What's removed**: Pydantic models, Docker, CI, LangGraph repair agent, deterministic UUIDs, chat UI
- **What's kept**: Writer → Evaluator → Editor loop, lint rules, repair behavior, consolidation step
- Config lives in the file itself — agent fills it during a first-run wizard

## When to Use Which

| Scenario | Use |
|---|---|
| Personal/small-team wiki (<200 docs) | `AGENTS.md` |
| Still discovering wiki shape | `AGENTS.md` |
| Large corpus (token cost matters) | Python package |
| Need deterministic outputs | Python package |
| Downstream automation (search, dashboards) | Python package |
| Production scheduled runs | Python package |
| Audit trail required | Python package |

Key insight from Bernardo: **output quality is comparable in both** — Karpathy's Writer → Evaluator → Editor loop is robust enough that it produces good pages whether it runs as Python or as agent instructions. The difference is _everything around the loop, not the loop itself._

## Related

- [[wiki-compilation-pattern]] — The Karpathy pattern both implementations derive from
- [[markdown-pipeline-integrity]] — The structural markdown problem that the programmatic version solves
- [[rag-vs-compilation]] — The broader knowledge management trade-off
- [[agent-system-overview]] — Where knowledge compilation pipelines fit in agent architecture

^[raw/articles/bernardo-llm-wiki-twice-2026.md]
^[raw/articles/karpathy-llm-wiki-2026.md]
