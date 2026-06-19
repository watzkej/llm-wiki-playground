---
source_url: https://lilianweng.github.io/posts/2023-06-23-agent/
ingested: 2026-06-18
sha256: e9ec19d1f8c5ca3c49f0e35ac6709996886c9800b1c682f783ada4b58ad73102
---

# LLM Powered Autonomous Agents — Lilian Weng

> Published: 2023-06-23 | Estimated Reading Time: 31 min | Author: Lilian Weng

Building agents with LLM (large language model) as its core controller is a cool concept. Several proof-of-concepts demos, such as AutoGPT, GPT-Engineer and BabyAGI, serve as inspiring examples. The potentiality of LLM extends beyond generating well-written copies, stories, essays and programs; it can be framed as a powerful general problem solver.

## Agent System Overview

In a LLM-powered autonomous agent system, LLM functions as the agent's brain, complemented by several key components:

- **Planning**
  - Subgoal and decomposition: The agent breaks down large tasks into smaller, manageable subgoals.
  - Reflection and refinement: The agent can do self-criticism and self-reflection over past actions.
- **Memory**
  - Short-term memory: In-context learning as utilizing short-term memory of the model.
  - Long-term memory: Retain and recall information over extended periods via external vector store.
- **Tool use**
  - The agent learns to call external APIs for extra information missing from model weights.

## Component One: Planning

### Task Decomposition

**Chain of thought** (CoT; Wei et al. 2022) has become a standard prompting technique. The model is instructed to "think step by step" to utilize more test-time computation to decompose hard tasks into smaller steps.

**Tree of Thoughts** (Yao et al. 2023) extends CoT by exploring multiple reasoning possibilities at each step. It decomposes the problem into multiple thought steps and generates multiple thoughts per step, creating a tree structure. The search process can be BFS or DFS with each state evaluated by a classifier or majority vote.

Task decomposition can be done: (1) by LLM with simple prompting, (2) by using task-specific instructions, or (3) with human inputs.

**LLM+P** (Liu et al. 2023) involves relying on an external classical planner to do long-horizon planning. This approach utilizes PDDL as an intermediate interface. The LLM translates the problem into PDDL, requests a planner to generate a plan, and translates the PDDL plan back into natural language.

### Self-Reflection

Self-reflection is a vital aspect that allows autonomous agents to improve iteratively by refining past action decisions and correcting previous mistakes.

**ReAct** (Yao et al. 2023) integrates reasoning and acting within LLM by extending the action space to be a combination of task-specific discrete actions and the language space. The ReAct prompt template: Thought: ... / Action: ... / Observation: ...

**Reflexion** (Shinn & Labash 2023) is a framework to equip agents with dynamic memory and self-reflection capabilities. It has a standard RL setup where the reward model provides a simple binary reward. The heuristic function determines when the trajectory is inefficient or contains hallucination.

**Chain of Hindsight** (CoH; Liu et al. 2023) encourages the model to improve on its own outputs by presenting it with a sequence of past outputs annotated with feedback. The model is finetuned to produce better output based on feedback sequences.

**Algorithm Distillation** (AD; Laskin et al. 2023) applies the same idea to cross-episode trajectories in RL tasks, where an algorithm is encapsulated in a long history-conditioned policy. Multi-episodic contexts of 2-4 episodes are necessary to learn near-optimal in-context RL.

## Component Two: Memory

### Types of Memory

- **Sensory Memory**: Earliest stage, retains impressions for a few seconds (iconic, echoic, haptic).
- **Short-Term Memory (STM)**: Capacity of ~7 items, lasts 20-30 seconds.
- **Long-Term Memory (LTM)**: Unlimited storage; explicit (episodic + semantic) and implicit (procedural).

Mappings to LLM agents:
- Sensory memory → embedding representations for raw inputs
- Short-term memory → in-context learning (limited by context window)
- Long-term memory → external vector store with fast retrieval

### Maximum Inner Product Search (MIPS)

External memory via vector store databases supporting fast MIPS. Common ANN algorithms:

- **LSH**: Hashing function maps similar items to same buckets
- **ANNOY**: Random projection trees; searches through half closest to query
- **HNSW**: Hierarchical layers of small-world graphs with shortcuts
- **FAISS**: Vector quantization by partitioning vector space into clusters
- **ScaNN**: Anisotropic vector quantization for better inner product preservation

## Component Three: Tool Use

**MRKL** (Karpas et al. 2022): Neuro-symbolic architecture. A collection of expert modules with LLM as router to route inquiries to the best module. Experiments showed it was harder to solve verbal math problems than explicitly stated ones.

**TALM** (Parisi et al. 2022) and **Toolformer** (Schick et al. 2023): Fine-tune a LM to learn to use external tool APIs.

**HuggingGPT** (Shen et al. 2023): Uses ChatGPT as task planner to select HuggingFace models. Four stages: (1) Task planning, (2) Model selection, (3) Task execution, (4) Response generation.

**API-Bank** (Li et al. 2023): Benchmark for tool-augmented LLMs with 53 API tools, 264 annotated dialogues, 568 API calls. Evaluates at three levels: call API, retrieve API, plan API.

## Case Studies

### Scientific Discovery Agent

**ChemCrow** (Bran et al. 2023): LLM augmented with 13 expert-designed tools for organic synthesis, drug discovery, and materials design. Human evaluations showed ChemCrow outperforms GPT-4 by a large margin.

**Boiko et al. (2023)**: Agent for autonomous design, planning, and performance of complex scientific experiments. Can browse Internet, read documentation, execute code, call robotics APIs. When asked to synthesize chemical weapons, 4/11 requests were accepted.

### Generative Agents Simulation

**Generative Agents** (Park et al. 2023): 25 virtual characters controlled by LLM-powered agents in a sandbox environment. Combines LLM with memory, planning, and reflection. Memory stream is a long-term memory module. Retrieval model surfaces context by relevance, recency, and importance. Results in emergent social behavior.

### Proof-of-Concept Examples

**AutoGPT**: Drawn attention to autonomous agents with LLM as main controller. Uses a comprehensive system message with goals, constraints, and commands. Reliability issues due to natural language interface.

**GPT-Engineer**: Creates a whole repository of code given a task in natural language. Instructed to think over components and ask for user input to clarify questions.

## Challenges

1. **Finite context length**: Restricted context capacity limits historical information, detailed instructions, API call context. Vector stores provide access but with less representation power than full attention.

2. **Challenges in long-term planning and task decomposition**: LLMs struggle to adjust plans when faced with unexpected errors, making them less robust compared to humans.

3. **Reliability of natural language interface**: LLMs may make formatting errors and occasionally exhibit rebellious behavior. Much agent demo code focuses on parsing model output.

## Key References

- Wei et al. "Chain of thought prompting elicits reasoning in large language models." NeurIPS 2022
- Yao et al. "Tree of Thoughts." arXiv 2305.10601 (2023)
- Yao et al. "ReAct: Synergizing reasoning and acting in language models." ICLR 2023
- Shinn & Labash. "Reflexion." arXiv 2303.11366 (2023)
- Laskin et al. "In-context Reinforcement Learning with Algorithm Distillation." ICLR 2023
- Karpas et al. "MRKL Systems." arXiv 2205.00445 (2022)
- Shen et al. "HuggingGPT." arXiv 2303.17580 (2023)
- Park et al. "Generative Agents." arXiv 2304.03442 (2023)

