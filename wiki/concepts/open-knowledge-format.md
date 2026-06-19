---
title: Open Knowledge Format (OKF)
created: 2026-06-18
updated: 2026-06-18
type: concept
tags: [framework, pattern, deployment, survey]
sources: [raw/articles/google-okf-introducing-2026.md]
---

# Open Knowledge Format (OKF)

**OKF v0.1** (Google Cloud, June 2026) is an open specification that formalizes the [[wiki-compilation-pattern|LLM-wiki pattern]] into a portable, interoperable standard. It's a vendor-neutral, agent- and human-friendly format for representing the metadata, context, and curated knowledge that modern AI systems need.

## What It Is

> "A format, not another service."

OKF represents knowledge as a directory of markdown files with YAML frontmatter — no compression schemes, no new runtime, no required SDK. A bundle is:

- **Just markdown** — readable in any editor, renderable on GitHub
- **Just files** — shippable as a tarball, hostable in any git repo
- **Just YAML frontmatter** — standardized fields: `type`, `title`, `description`, `resource`, `tags`, `timestamp`

## Why It Exists

Organizational knowledge is fragmented across incompatible systems: metadata catalogs, wikis, shared drives, code comments, notebooks. When an AI agent needs context ("How do I compute weekly active users?"), it has to assemble the answer from these scattered surfaces. Every vendor has its own API, schema, and SDK.

**The wiki compilation pattern solves this for individual teams, but each instance is bespoke.** OKF makes these instances interoperable by standardizing the small set of conventions — file naming, frontmatter fields, cross-linking rules — so a wiki built by one agent can be consumed by another without translation.

## Three Design Principles

| Principle | Meaning |
|---|---|
| **Minimally opinionated** | Only `type` is required. Content model is producer-defined. The spec defines the interoperability surface, not the content. |
| **Producer/consumer independence** | Human-written → agent-consumed. Pipeline-generated → visualizer-browsed. LLM-synthesized → LLM-queried. The format is the contract. |
| **Format, not platform** | No cloud, database, model provider, or agent framework lock-in. No proprietary SDK. "The value of a knowledge format comes from how many parties speak it, not from who owns it." |

## Structure

```
bundle/
├── index.md              # Progressive disclosure for agents
├── log.md                # Chronological change history
├── datasets/
│   ├── index.md
│   └── orders_db.md      # One concept per file
├── tables/
│   ├── index.md
│   ├── orders.md
│   └── customers.md
└── metrics/
    ├── index.md
    └── weekly_active_users.md
```

Concepts link via normal markdown links → richer graph than filesystem hierarchy alone.

## Reference Implementations

Google Cloud shipped three proofs of concept with the spec:

1. **Enrichment agent** — walks a BigQuery dataset, drafts OKF concept documents, runs a second LLM pass for citations/schemas/joins
2. **Static HTML visualizer** — turns any OKF bundle into an interactive graph view in a single file; no backend, no install
3. **Sample bundles** — GA4 e-commerce, Stack Overflow, Bitcoin public datasets

These demonstrate producer/consumer independence: the agent is one way to produce OKF; the visualizer is one way to consume it. Neither is required by the format.

## Relevance to Agent Architecture

OKF matters for agent design because it provides **a standard knowledge interchange format** — analogous to how JSON Schema standardized API contracts. An agent that reads/writes OKF can:

- Consume knowledge produced by any other OKF-compliant system
- Produce knowledge that survives beyond its own runtime
- Participate in multi-agent workflows where agents exchange curated context

This addresses one of the [[agent-system-overview|core challenges in agent systems]]: context assembly. Instead of every agent solving the fragmentation problem from scratch, OKF provides a shared substrate.

## Related

- [[wiki-compilation-pattern]] — The pattern OKF formalizes
- [[wiki-llm]] — Implementations that could adopt OKF output
- [[rag-vs-compilation]] — OKF as the compilation side's interchange format
- [[agent-system-overview]] — Context assembly as a core agent capability
- [[markdown-pipeline-integrity]] — Structural validation; OKF conformance is a related concern

^[raw/articles/google-okf-introducing-2026.md]
