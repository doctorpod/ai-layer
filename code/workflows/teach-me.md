---
name: teach-me
description: Teach a topic by probing what you already know and using the codebase as the learning material.
---

# Workflow: Teach Me

Teach the user about a topic by probing what they already know, then building on it using the actual codebase as the learning material.

## Example usage

> [!quote] Teach me how this app works with a view to learning React

## Before you start

1. Read the relevant source files so your questions are grounded in real code
2. Open each file in VS Code with `code --goto <path>` when it becomes the focus

## How to teach

- Ask **one question at a time** — never a list
- Do **not** pre-fill the answer or hint at it in the question wording
- After the user answers:
  - If correct: confirm it briefly, then deepen or extend
  - If wrong or "I don't know": explain clearly, ground it in the actual file/line, then move on
- Move from fundamentals toward the specific patterns in this codebase
- When switching to a new file, open it in VS Code before asking about it

## Pacing

- Don't rush to cover everything — depth beats breadth
- If the user is clearly confident on a topic, skip ahead
- If they're struggling, slow down and use analogies

## When to stop

When the user says they've had enough, or asks to move on to something else.
