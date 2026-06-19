---
title: HuggingGPT
created: 2026-06-18
updated: 2026-06-18
type: entity
tags: [framework, orchestration, tool-use, planning]
sources: [raw/articles/lilian-weng-agent-survey-2023.md]
confidence: medium
---

# HuggingGPT

**HuggingGPT** (Shen et al. 2023) is a framework that uses ChatGPT as a task planner to orchestrate HuggingFace's model ecosystem. It routes user requests to the most appropriate expert models.

## Four-Stage Pipeline

1. **Task Planning** — LLM parses user requests into multiple tasks, each with: task type, ID, dependencies, and arguments. Few-shot examples guide the parsing.

2. **Model Selection** — LLM selects from available HuggingFace models framed as a multiple-choice question. Task-type filtering narrows candidates to fit context length.

3. **Task Execution** — Expert models execute tasks; results are logged with file paths and metadata.

4. **Response Generation** — LLM receives all execution results and synthesizes a coherent response, including file paths and analysis.

## Real-World Challenges

- **Efficiency** — Multiple LLM inference rounds + external model calls slow things down
- **Context length** — Complex task content strains the context window
- **Stability** — LLM outputs and external model services can be unreliable

## Related

- [[tool-use-in-agents]] — HuggingGPT as a tool orchestration pattern
- [[react-pattern]] — The Thought/Action/Observation format used
- [[agent-system-overview]] — Maps planning + tool use components

^[raw/articles/lilian-weng-agent-survey-2023.md]
