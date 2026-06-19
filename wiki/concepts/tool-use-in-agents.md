---
title: Tool Use in Agents
created: 2026-06-18
updated: 2026-06-18
type: concept
tags: [tool-use, framework, evaluation]
sources: [raw/articles/lilian-weng-agent-survey-2023.md]
---

# Tool Use in Agents

Equipping LLMs with external tools significantly extends model capabilities beyond static weights — enabling code execution, API calls, web browsing, and domain-specific computation.

## Key Frameworks

### MRKL (Karpas et al. 2022)
**Modular Reasoning, Knowledge and Language** — A neuro-symbolic architecture where the LLM acts as a **router**, directing inquiries to the most suitable expert module (neural or symbolic). Key finding: it's harder for LLMs to solve verbal math problems than explicitly stated ones, because extracting correct arguments for arithmetic is unreliable.

### Toolformer (Schick et al. 2023)
Fine-tunes an LM to autonomously learn when and how to call external APIs. The training dataset is expanded when API call annotations improve output quality.

### HuggingGPT (Shen et al. 2023)
A 4-stage pipeline using ChatGPT as task planner:
1. **Task Planning** — Parse user request into subtasks with dependencies
2. **Model Selection** — Distribute tasks to HuggingFace expert models
3. **Task Execution** — Expert models execute and log results
4. **Response Generation** — LLM summarizes execution results

### API-Bank (Li et al. 2023)
A benchmark for tool-augmented LLMs with 53 APIs and 264 annotated dialogues. Evaluates at three levels:
- **Level 1**: Can the model call a given API correctly?
- **Level 2**: Can the model find the right API from a catalog?
- **Level 3**: Can the model plan multi-step API sequences for ambiguous requests?

## Practical Deployments

- **ChatGPT Plugins** — Third-party APIs surfaced through a plugin marketplace
- **OpenAI Function Calling** — Developer-defined tool schemas; LLM generates structured JSON calls
- **ChemCrow** — Domain-specific: 13 chemistry tools for synthesis and drug discovery

## Related

- [[agent-system-overview]] — Tool use as one of three core components
- [[planning-in-agents]] — Planning often involves tool selection
- [[hugging-gpt]] — Deep dive on the HuggingGPT framework

^[raw/articles/lilian-weng-agent-survey-2023.md]
