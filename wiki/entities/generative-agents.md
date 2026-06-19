---
title: Generative Agents
created: 2026-06-18
updated: 2026-06-18
type: entity
tags: [multi-agent, memory, planning, reflection, communication, benchmark]
sources: [raw/articles/lilian-weng-agent-survey-2023.md]
---

# Generative Agents

**Generative Agents** (Park et al. 2023) is a landmark paper demonstrating 25 LLM-powered agents living and interacting in a sandbox environment inspired by The Sims. It combines LLMs with memory, planning, and reflection to produce believable simulacra of human behavior.

## Architecture

### Memory Stream
A long-term memory module that records all agent experiences as natural language observations. Inter-agent communication can trigger new observations.

### Retrieval Model
Surfaces relevant context along three scored dimensions:
- **Recency** — recent events score higher
- **Importance** — LLM evaluates whether a memory is mundane or core
- **Relevance** — embedding similarity to current situation/query

### Reflection Mechanism
Synthesizes memories into higher-level inferences over time:
- Feed the 100 most recent observations to the LLM
- Generate the 3 most salient high-level questions
- Ask the LLM to answer those questions
- These reflections guide future behavior

### Planning & Reacting
Translates reflections and environment information into actions. Plans are generated daily ("Here is X's plan today in broad strokes: 1)...") and consider relationships between agents and observations.

## Emergent Behaviors

The simulation produced surprising emergent social phenomena:
- **Information diffusion** — news spread naturally through the agent community
- **Relationship memory** — agents continued conversations across multiple interactions
- **Social coordination** — agents organized events (parties) and invited others

## Significance

This paper demonstrated that LLM agents with persistent memory and social awareness can produce emergent collective behavior — not just individual task completion.

## Related

- [[memory-in-agents]] — The memory stream and retrieval model
- [[multi-agent-systems]] — Multi-agent interaction patterns
- [[agent-system-overview]] — Maps to the 3-component architecture

^[raw/articles/lilian-weng-agent-survey-2023.md]
