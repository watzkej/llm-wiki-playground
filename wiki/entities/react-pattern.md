---
title: ReAct Pattern
created: 2026-06-18
updated: 2026-06-18
type: entity
tags: [pattern, reasoning, tool-use, reflection, benchmark]
sources: [raw/articles/lilian-weng-agent-survey-2023.md]
---

# ReAct Pattern

**ReAct** (Reasoning + Acting) is a prompting pattern introduced by Yao et al. (2023, ICLR) that interleaves reasoning traces with environment actions.

## How It Works

The agent operates in a loop with three phases:

```
Thought: [Reason about the current state and what to do next]
Action: [Execute a tool call or environment action]
Observation: [Receive feedback from the environment]
... (repeat)
```

The action space is extended to include both:
- **Task-specific discrete actions** (e.g., Wikipedia search API call)
- **Language space actions** (natural language reasoning traces)

## Key Results

ReAct outperforms **Act-only baselines** (where the Thought step is removed) on:
- **Knowledge-intensive tasks**: HotpotQA, FEVER
- **Decision-making tasks**: AlfWorld Env, WebShop

The interleaving of reasoning and acting allows the agent to dynamically adjust its plan based on observations, rather than committing to a static plan upfront.

## Influence

ReAct has become one of the most influential agent patterns, directly inspiring:
- [[reflection-in-agents|Reflexion]] — adds RL-based self-reflection on top of ReAct's action space
- [[hugging-gpt]] — uses Thought/Action/Observation format in its pipeline
- ChemCrow — domain-specific ReAct for chemistry (see [[tool-use-in-agents]])
- Most modern agent frameworks incorporate some form of the ReAct loop

## Related

- [[reflection-in-agents]] — Reflexion builds on ReAct's action space
- [[planning-in-agents]] — ReAct as a planning+execution strategy
- [[agent-system-overview]] — Where ReAct fits in agent architecture

^[raw/articles/lilian-weng-agent-survey-2023.md]
