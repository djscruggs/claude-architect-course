The coordinator takes a query like "What is the current status of age verification legislation in Texas, Florida, and Oklahoma?" and decomposes it by state + dimension (legislative status, industry opposition activity, enforcement history).

Three subagents:
- Web search agent - finds current bill status, news, lobbying filings
- Document analysis agent - reads and extracts from PDFs (actual bill text, legislative testimony)
- Synthesis agent - assembles the final brief with claim-source mappings

Where Domain 1 shows up for real:
- Isolated context trap - your synthesis agent will hallucinate the first time you forget to pass the web search findings explicitly. Let it happen, screenshot it, fix it. That's your best paragraph.
- Programmatic prerequisite gate - fact-check must complete before synthesis fires. You're dealing with policy claims that could embarrass you publicly if wrong. This is the exact "financial/security-critical" scenario where prompt instructions alone aren't enough.
- PostToolUse hook - different web sources return dates in wildly different formats. The hook normalizes them before the synthesis agent ever sees them.
- Multi-pass decomposition - one pass per state (avoids attention dilution), then a cross-state integration pass that spots patterns (e.g., "four states used nearly identical industry-drafted language").
- fork_session - use it to explore two different synthesis approaches from the same research baseline and compare outputs.

The Writing Angle

Title: "I Built a Multi-Agent AI to Track Age Verification Laws - Here's What Broke First"

The structure writes itself:
1. The motivation - you're building Cardless ID, you needed to track legislation across 50 states, you decided to build the agent instead of reading every state legislature website yourself
2. What I thought would be hard (wasn't) - setting up the coordinator, basic tool calls
3. What actually broke first - subagent context isolation. Your synthesis agent confidently summarized research it had never actually seen because you assumed memory was shared. This is the post's "aha moment" for most developers reading it.
4. The thing I almost got wrong - prompt-based enforcement for fact-checking vs. programmatic gate. Why "always fact-check before synthesizing" in the system prompt isn't good enough when you're producing public policy content.
5. What it produced - show an actual output brief. Real states, real bills, real citations.
That last point matters a lot. Ending with a concrete artifact - an actual one-page policy brief the agent produced - is what separates a technical post from a tutorial. It proves the thing works.
