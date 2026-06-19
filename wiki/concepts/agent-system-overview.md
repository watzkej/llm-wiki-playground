---
title: Agent System Overview
created: 2026-06-18
updated: 2026-06-18
type: concept
tags: [pattern, planning, memory, tool-use]
sources: [raw/articles/lilian-weng-agent-survey-2023.md]
---

# Agent System Overview

The standard architectural model for LLM-powered autonomous agents centers on three components:

## The Three-Component Model

1. **Planning** — The agent decomposes complex tasks into manageable subgoals and can reflect on past actions to refine future steps. See [[planning-in-agents]].

2. **Memory** — The agent maintains both short-term memory (in-context learning) and long-term memory (external vector stores with fast retrieval). See [[memory-in-agents]].

3. **Tool Use** — The agent calls external APIs and tools to access information beyond its model weights, execute code, and interact with environments. See [[tool-use-in-agents]].

The LLM functions as the "brain" or central controller, orchestrating all three components.

## Key Insight

This decomposition has become the de facto reference architecture for agent frameworks. Most modern agent systems ([[auto-gpt]], HuggingGPT, Generative Agents) map to this model, though they emphasize different components.

## Related

- [[planning-in-agents]] — Deep dive on decomposition and self-reflection
- [[memory-in-agents]] — Memory types and retrieval strategies
- [[tool-use-in-agents]] — External API integration patterns
- [[react-pattern]] — A specific instantiation combining reasoning and acting

^[raw/articles/lilian-weng-agent-survey-2023.md]
