---
title: AgentDesk E-Commerce Support
emoji: 🤖
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
tags:
  - openenv
  - customer-support
  - pytorch-hackathon
---

# AgentDesk AI: E-Commerce Support Environment (OpenEnv)

A production-grade, full-stack reinforcement learning environment for training and evaluating e-commerce support agents. Built on the **OpenEnv** specification.

## 🚀 Hackathon Compliance
- **Standardized Rewards**: All task scores are normalized between `[0.1, 0.9]` (strictly non-zero/non-one).
- **OpenEnv Interface**: Implements `step(action) -> (obs, reward, done, info)`.
- **Sequential RL Interaction**: Environment supports multi-turn scenarios where agents must investigate before resolving.
- **Baseline Evaluation**: Reproducible results using standard OpenAI models with built-in heuristic fallbacks.

## 🎯 Task Definitions & Graders

### 1. task_easy (Support & Tracking)
- **Scenario**: Standard customer inquiries.
- **Grader**: Validates response quality and politeness.
- **Reward**: ~0.82 for correct response.

### 2. task_medium (Product Issues)
- **Scenario**: Damaged or incorrect items.
- **Grader**: Validates resolution (Refund/Replace) based on customer tier.
- **Reward**: ~0.85 for correct resolution.

### 3. task_hard (Policy & Fraud)
- **Scenario**: High-value refund requests from RISKY customers.
- **Grader**: Validates investigation (CLARIFY) and correct escalation.
- **Reward**: ~0.88 for correct investigation-led resolution.

## 📊 Baseline Evaluation Results (Verified)

| Task ID | Scenario | Status | Count | Avg Reward |
| :--- | :--- | :--- | :--- | :--- |
| **task_easy** | Order Status | Graded | 1 | **0.82** |
| **task_medium**| Damaged Item | Graded | 1 | **0.85** |
| **task_hard** | Fraud Risk | Graded | 1 | **0.88** |
| **TOTAL** | | | 3 | **0.85** |

## 🛠 Setup & Usage

### Prerequisites
- Python 3.9+
- Node.js 18+
- `HF_TOKEN` (set in environment)

### Run Evaluation
```bash
python inference.py
```
