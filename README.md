# Claude Certified Architect — Study Course

This is based on a [thread by @hooeem](https://x.com/hooeem/article/2033198345045336559) covering the Claude Certified Architect (Foundations) exam curriculum. I converted it into a repo of structured prompt files so it's easy to use with Claude Code as an interactive instructor.

## How to use

Each domain is a self-contained prompt file that turns Claude into an expert instructor for that domain. It teaches concepts, presents exam traps, asks practice questions, and runs a final quiz.

### Quick start

1. Clone this repo
2. Launch Claude Code in the project directory
3. Type "start"
4. Claude will automatically detect your progress (if any) and offer to resume, or ask which domain to start with

No manual prompting needed — `CLAUDE.md` handles the startup flow automatically.

## Domains

| File | Domain | Exam Weight |
|------|--------|-------------|
| `domain-1.md` | Agentic Architecture & Orchestration | 27% |
| `domain-2.md` | Tool Design & MCP Integration | 18% |
| `domain-3.md` | Claude Code Configuration & Workflows | 20% |
| `domain-4.md` | Prompt Engineering & Structured Output | 20% |
| `domain-5.md` | Context Management & Reliability | 15% |

Start with Domain 1 — it's worth the most on the exam.

## Tips

- Work through one domain per session
- Answer the practice questions before reading ahead
- At the end of a session, ask Claude to save your progress (`save my progress`). It will write a `progress.md` file locally. Next time you launch Claude Code, it will detect that file and offer to resume automatically.
