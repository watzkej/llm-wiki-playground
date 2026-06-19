# Wiki Schema

## Domain
LLM agent architectures — design patterns, frameworks, components, and techniques
for building autonomous agents powered by large language models. Covers
orchestration, tool-use, memory, planning, reflection, multi-agent systems, and
evaluation.

## Conventions
- File names: lowercase, hyphens, no spaces (e.g., `react-pattern.md`)
- Every wiki page starts with YAML frontmatter (see below)
- Use `[[wikilinks]]` to link between pages (minimum 2 outbound links per page)
- When updating a page, always bump the `updated` date
- Every new page must be added to `index.md` under the correct section
- Every action must be appended to `log.md`
- **Provenance markers:** On pages that synthesize 3+ sources, append `^[raw/articles/source-file.md]`
  at the end of paragraphs whose claims come from a specific source. This lets a reader trace each
  claim back without re-reading the whole raw file. Optional on single-source pages where the
  `sources:` frontmatter is enough.

## Frontmatter
```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: [from taxonomy below]
sources: [raw/articles/source-name.md]
# Optional quality signals:
confidence: high | medium | low        # how well-supported the claims are
contested: true                        # set when the page has unresolved contradictions
contradictions: [other-page-slug]      # pages this one conflicts with
---
```

`confidence` and `contested` are optional but recommended for opinion-heavy or fast-moving
topics. Lint surfaces `contested: true` and `confidence: low` pages for review so weak claims
don't silently harden into accepted wiki fact.

### raw/ Frontmatter

Raw sources ALSO get a small frontmatter block so re-ingests can detect drift:

```yaml
---
source_url: https://example.com/article   # original URL, if applicable
ingested: YYYY-MM-DD
sha256: <hex digest of the raw content below the frontmatter>
---
```

The `sha256:` lets a future re-ingest of the same URL skip processing when content is unchanged,
and flag drift when it has changed. Compute over the body only (everything after the closing
`---`), not the frontmatter itself.

## Tag Taxonomy

### Architecture Patterns
- `pattern` — architectural patterns (ReAct, Plan-Execute, Tree-of-Thought)
- `planning` — planning strategies and algorithms
- `reflection` — self-critique, error recovery, iterative improvement
- `orchestration` — coordinating multiple agents or sub-tasks

### Agent Components
- `memory` — short-term, long-term, working memory, retrieval
- `tool-use` — function calling, API integration, tool selection
- `reasoning` — chain-of-thought, step-by-step reasoning, logic

### Multi-Agent
- `multi-agent` — multi-agent systems, swarms, teams
- `communication` — inter-agent messaging, protocols, shared context
- `role-assignment` — agent specialization, role-based architectures

### Frameworks & Tools
- `framework` — libraries and frameworks (LangChain, CrewAI, AutoGen, etc.)
- `evaluation` — benchmarks, metrics, evaluation methodologies
- `deployment` — production serving, observability, guardrails

### Meta
- `survey` — survey papers, landscape reviews
- `comparison` — side-by-side analyses
- `benchmark` — performance comparisons, leaderboards
- `controversy` — debates, competing claims
- `emerging` — new/experimental ideas (reviewed for promotion quarterly)

Rule: every tag on a page must appear in this taxonomy. If a new tag is needed,
add it here first, then use it. This prevents tag sprawl.

## Page Thresholds
- **Create a page** when an entity/concept appears in 2+ sources OR is central to one source
- **Add to existing page** when a source mentions something already covered
- **DON'T create a page** for passing mentions, minor details, or things outside the domain
- **Split a page** when it exceeds ~200 lines — break into sub-topics with cross-links
- **Archive a page** when its content is fully superseded — move to `_archive/`, remove from index

## Entity Pages
One page per notable entity. Include:
- Overview / what it is
- Key facts and dates
- Relationships to other entities ([[wikilinks]])
- Source references

Entity types in this domain: frameworks, models, tools, companies, labs, researchers.

## Concept Pages
One page per concept or topic. Include:
- Definition / explanation
- Current state of knowledge
- Open questions or debates
- Related concepts ([[wikilinks]])

## Comparison Pages
Side-by-side analyses. Include:
- What is being compared and why
- Dimensions of comparison (table format preferred)
- Verdict or synthesis
- Sources

## Update Policy
When new information conflicts with existing content:
1. Check the dates — newer sources generally supersede older ones
2. If genuinely contradictory, note both positions with dates and sources
3. Mark the contradiction in frontmatter: `contradictions: [page-name]`
4. Flag for user review in the lint report