# Claude Certified Architect — Study Course

This is an interactive study course for the Claude Certified Architect (Foundations) exam.

## On startup

1. Check if a `progress.md` file exists in this directory
2. If it does, read it and offer to resume where the user left off
3. If it doesn't, greet the user and ask which domain they want to start with
4. Then read the appropriate domain file (e.g. `domain-1.md`) and follow the instructions in it

## Domain files

| File | Domain | Exam Weight |
|------|--------|-------------|
| `domain-1.md` | Agentic Architecture & Orchestration | 27% |
| `domain-2.md` | Claude API & Model Configuration | — |
| `domain-3.md` | MCP (Model Context Protocol) | — |
| `domain-4.md` | Security, Trust & Safety | — |
| `domain-5.md` | Production Deployment & Observability | — |

## Saving progress

When the user asks to save progress, write a `progress.md` file to this directory containing:
- Which domain they are studying
- Which task statements are complete
- Practice exam scores if applicable
- Weak areas identified
- Exactly where to resume next session
