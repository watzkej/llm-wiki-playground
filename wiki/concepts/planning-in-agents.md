---
title: Planning in Agents
created: 2026-06-18
updated: 2026-06-18
type: concept
tags: [planning, reasoning, pattern]
sources: [raw/articles/lilian-weng-agent-survey-2023.md]
---

# Planning in Agents

Planning enables an LLM agent to decompose complex tasks into smaller, manageable steps — and to reflect on its own performance to improve.

## Task Decomposition

### Chain of Thought (CoT)
**Wei et al. 2022** — The foundational technique. The model is prompted to "think step by step," using test-time computation to break hard tasks into simpler steps. CoT transforms big tasks into multiple manageable ones and provides interpretability into the model's reasoning process.

### Tree of Thoughts (ToT)
**Yao et al. 2023** — Extends CoT by exploring **multiple** reasoning paths at each step. Creates a tree structure of thoughts and searches via BFS or DFS. Each state is evaluated by a classifier (prompt) or majority vote. This is more powerful than linear CoT for problems with branching solution spaces.

### LLM+P
**Liu et al. 2023** — Outsources planning to a classical planner. The workflow:
1. LLM translates the problem into PDDL (Planning Domain Definition Language)
2. A classical planner generates a PDDL plan
3. LLM translates the PDDL plan back into natural language

This assumes domain-specific PDDL and a suitable planner are available — common in robotics, rare elsewhere.

### Decomposition Strategies
Task decomposition can be triggered by:
1. Simple LLM prompting ("Steps for XYZ...")
2. Task-specific instructions ("Write a story outline.")
3. Human inputs

## Self-Reflection

Self-reflection allows agents to **improve iteratively** by learning from past mistakes. This is critical for real-world tasks where trial and error are inevitable. See [[reflection-in-agents]] for the full taxonomy of reflection approaches.

## Related

- [[agent-system-overview]] — How planning fits in the 3-component model
- [[reflection-in-agents]] — Self-reflection frameworks (ReAct, Reflexion, CoH)
- [[chain-of-thought]] — Deep dive on CoT and its variants

^[raw/articles/lilian-weng-agent-survey-2023.md]
