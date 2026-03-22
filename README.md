# Claude Certified Architect — Study Course

This repo is based on a [thread by @hooeem](https://x.com/hooeem/article/2033198345045336559) covering the Claude Certified Architect (Foundations) exam curriculum. I converted it into a repo of structured prompt files so it's easy to use with Claude Code as an interactive instructor.

## How to use

Each domain is a self-contained prompt file that turns Claude into an expert instructor for that domain. It teaches concepts, presents exam traps, asks practice questions, and runs a final quiz.

### Quick start

1. Clone this repo
2. Launch Claude Code in the project directory
3. Tell Claude to read the domain file and follow the instructions:

```
read @domain-1.md and follow the instructions
```

Claude will ask about your experience level and adapt accordingly.

## Domains

| File | Domain | Exam Weight |
|------|--------|-------------|
| `domain-1.md` | Agentic Architecture & Orchestration | 27% |
| `domain-2.md` | Claude API & Model Configuration | — |
| `domain-3.md` | MCP (Model Context Protocol) | — |
| `domain-4.md` | Security, Trust & Safety | — |
| `domain-5.md` | Production Deployment & Observability | — |

Start with Domain 1 — it's worth the most on the exam.

## Tips

- Work through one domain per session
- Answer the practice questions before reading ahead
- At the end of a session, ask Claude to save a progress summary to a local file (e.g. `save my progress to progress.md`). At the start of your next session, tell Claude to read it: `read @progress.md and pick up where we left off`
