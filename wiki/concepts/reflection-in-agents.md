---
title: Reflection in Agents
created: 2026-06-18
updated: 2026-06-18
type: concept
tags: [reflection, pattern, planning]
sources: [raw/articles/lilian-weng-agent-survey-2023.md]
---

# Reflection in Agents

Reflection is the agent's ability to critique its own outputs and behavior, learn from mistakes, and iteratively improve. It's what separates a single-pass LLM call from an autonomous agent that gets better over time.

## Reflection Frameworks

### ReAct (Yao et al. 2023)
**Reasoning + Acting** — Extends the action space to include both task-specific actions AND natural language reasoning. The template cycles through Thought → Action → Observation, enabling the agent to interleave thinking with doing. ReAct outperforms Act-only baselines on both knowledge-intensive (HotpotQA, FEVER) and decision-making tasks (AlfWorld, WebShop).

See [[react-pattern]] for a full deep dive.

### Reflexion (Shinn & Labash 2023)
A framework adding **dynamic memory and self-reflection** to agents. Built on an RL setup:
- Reward model provides simple binary reward
- Heuristic function detects inefficient trajectories (too long without success) or hallucination (consecutive identical actions with same observation)
- Self-reflection is created via two-shot examples showing (failed trajectory, ideal reflection) pairs
- Up to 3 reflections stored in working memory for context

### Chain of Hindsight (CoH; Liu et al. 2023)
Trains the model to **improve by seeing its own past outputs with human feedback**. The training data is sequences of (output, rating, feedback) ordered from worst to best. The model is fine-tuned to predict only the final, best output — learning to self-reflect through the feedback sequence. Key techniques:
- Regularization term to maximize pre-training log-likelihood (prevents overfitting)
- Random masking of 0-5% of past tokens (prevents shortcutting/copying)

### Algorithm Distillation (AD; Laskin et al. 2023)
Applies the hindsight principle to **reinforcement learning across episodes**. Multi-episode histories are concatenated and fed to the model, so it learns the process of RL improvement itself rather than any specific task policy. Requires 2-4 episodes in context for near-optimal in-context RL.

## Common Failure Modes Detected by Reflection

- **Inefficient planning** — trajectories that take too long without success
- **Hallucination** — consecutive identical actions producing the same observation
- **Format errors** — malformed tool calls or response structures

## Related

- [[planning-in-agents]] — Reflection as a planning sub-capability
- [[react-pattern]] — The ReAct pattern in detail
- [[agent-system-overview]] — Where reflection fits in the architecture

^[raw/articles/lilian-weng-agent-survey-2023.md]
