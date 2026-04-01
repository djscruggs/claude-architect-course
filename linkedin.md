Anthropic has a "Claude Certified Architect" exam. You can only take it if you're a partner.

So I pulled apart the entire curriculum and built a free study repo instead.

Each domain is a structured prompt file that turns Claude Code into an interactive instructor - it teaches the concepts, surfaces the exam traps, asks practice questions, and runs a final quiz. CLAUDE.md handles session startup automatically and saves your progress between sessions.

I just finished Domain 1 (Agentic Architecture & Orchestration - the biggest at 27%). The thing most developers get wrong: they assume subagents share memory with a coordinator. They don't. Every piece of context has to be passed explicitly. Miss this in production and your agent hallucinates with complete confidence.

Four domains left. Repo is free and open to clone.

https://github.com/djscruggs/claude-architect-course

#Claude #AgenticAI #ClaudeCode #LLM #AIEngineering
