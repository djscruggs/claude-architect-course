import asyncio
import json
import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv(Path(__file__).parent.parent / ".env")

client = Anthropic()

# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------

class EnforcementType(Enum):
    LAW_ENFORCEMENT = "law_enforcement"
    PRIVATE_CIVIL_SUIT = "private_civil_suit"


@dataclass
class Source:
    name: str
    url: str


@dataclass
class EnforcementAction:
    date: str  # ISO 8601
    type: EnforcementType
    description: str
    source: Source


@dataclass
class StateResult:
    state: str
    summary: str
    sources: list[Source]
    enforcement_actions: list[EnforcementAction]


@dataclass
class LawContext:
    canonical_name: str
    alternative_names: list[str]
    federal_analogues: list[str]
    search_terms: list[str]
    novel_theory_terms: list[str]


@dataclass
class SearchResult:
    title: str
    url: str


@dataclass
class DocumentAnalysis:
    url: str
    action_type: Optional[EnforcementType]
    docket_id: Optional[str]
    action_name: Optional[str]
    key_dates: list[str]
    summary: str


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------

VALID_STATES = {name.lower() for name in [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
    "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
    "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
    "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
    "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
    "New Hampshire", "New Jersey", "New Mexico", "New York",
    "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
    "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
    "West Virginia", "Wisconsin", "Wyoming",
]}

STATE_ABBREVIATIONS: dict[str, str] = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware",
    "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
    "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas",
    "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi",
    "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
    "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York",
    "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma",
    "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah",
    "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
    "WI": "Wisconsin", "WY": "Wyoming",
}


def normalise_states(states: list[str]) -> list[str]:
    result = []
    for s in states:
        s = s.strip()
        canonical = STATE_ABBREVIATIONS.get(s.upper())
        if canonical:
            result.append(canonical)
        elif s.lower() in VALID_STATES:
            result.append(s.title())
    return result


def extract_json(text: str) -> str:
    match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if match:
        return match.group(1).strip()
    return text.strip()


# ---------------------------------------------------------------------------
# Signal detection
# ---------------------------------------------------------------------------

def check_law_exists(results: list[dict]) -> bool:
    law_indicators = {
        "act", "statute", "law", "legislation", "bill", "code", "regulation",
        "enacted", "signed", "effective",
    }
    return any(
        word in result["title"].lower()
        for result in results
        for word in law_indicators
    )


def check_ag_signal(results: list[dict]) -> bool:
    ag_indicators = {
        "attorney general", "ag ", " ag ", "department of justice", "doj",
        "state v.", "state vs.", "commonwealth v.", "people v.",
        "enforcement action", "consent decree", "civil investigative demand",
    }
    return any(
        indicator in result["title"].lower()
        for result in results
        for indicator in ag_indicators
    )


def check_civil_suit_signal(results: list[dict]) -> bool:
    civil_indicators = {
        "lawsuit", "sued", "class action", "plaintiff", "complaint filed",
        "v.", "vs.", "litigation", "novel theory", "privacy tort",
        "consumer protection", "negligence",
    }
    return any(
        indicator in result["title"].lower()
        for result in results
        for indicator in civil_indicators
    )


# ---------------------------------------------------------------------------
# Tool stubs
# ---------------------------------------------------------------------------

async def web_search(
    query: str,
    date_range: Optional[dict] = None,
) -> list[SearchResult]:
    # TODO: wire to search API (Brave, Serper, Tavily, Exa)
    return [
        SearchResult(
            title="Texas Age Verification Act signed into law",
            url="https://example.com/texas-ava",
        ),
    ]


async def enforcement_search(
    query: str,
    date_range: Optional[dict] = None,
    law_exists: bool = False,
) -> list[SearchResult]:
    # TODO: wire to search API
    # law_exists=False should shift query toward novel theory terms
    return [
        SearchResult(
            title="State v. ExampleCorp — AG enforcement action",
            url="https://example.com/ag-action",
        ),
    ]


async def document_analysis(url: str) -> DocumentAnalysis:
    # TODO: fetch URL content and extract structured fields via Claude call
    return DocumentAnalysis(
        url=url,
        action_type=None,
        docket_id=None,
        action_name=None,
        key_dates=[],
        summary="Stub summary",
    )


# ---------------------------------------------------------------------------
# Tool dispatch
# ---------------------------------------------------------------------------

async def dispatch_tool(
    name: str,
    input: dict,
    law_exists: bool = False,
) -> str:
    if name == "web_search":
        results = await web_search(
            query=input["query"],
            date_range=input.get("date_range"),
        )
        return json.dumps([{"title": r.title, "url": r.url} for r in results])

    elif name == "document_analysis":
        result = await document_analysis(input["url"])
        return json.dumps({
            "url": result.url,
            "action_type": result.action_type.value if result.action_type else None,
            "docket_id": result.docket_id,
            "action_name": result.action_name,
            "key_dates": result.key_dates,
            "summary": result.summary,
        })

    elif name == "enforcement_search":
        results = await enforcement_search(
            query=input["query"],
            date_range=input.get("date_range"),
            law_exists=law_exists,
        )
        return json.dumps([{"title": r.title, "url": r.url} for r in results])

    else:
        raise ValueError(f"Unknown tool: {name}")


# ---------------------------------------------------------------------------
# Tool schema
# ---------------------------------------------------------------------------

def build_tools(state: str, law: LawContext) -> list[dict]:
    date_range_schema = {
        "type": "object",
        "properties": {
            "start": {"type": "string", "description": "ISO 8601 date"},
            "end": {"type": "string", "description": "ISO 8601 date"},
        },
        "required": [],
    }

    return [
        {
            "name": "web_search",
            "description": f"Search the web for {law.canonical_name} and related laws in {state}. Use search terms: {', '.join(law.search_terms)}",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "date_range": date_range_schema,
                },
                "required": ["query"],
            },
        },
        {
            "name": "document_analysis",
            "description": "Fetch and analyse a document at a given URL. Returns structured fields including action type, docket ID, key dates, and summary.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "url": {"type": "string"},
                },
                "required": ["url"],
            },
        },
        {
            "name": "enforcement_search",
            "description": f"Search for enforcement actions related to {law.canonical_name} in {state}, including novel theory cases. Use terms: {', '.join(law.novel_theory_terms)}",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "date_range": date_range_schema,
                },
                "required": ["query"],
            },
        },
    ]


# ---------------------------------------------------------------------------
# Result parsing
# ---------------------------------------------------------------------------

def parse_state_result(state: str, content: list) -> StateResult:
    text = " ".join(
        block.text for block in content
        if hasattr(block, "text")
    )

    text = extract_json(text)

    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"parse_state_result returned invalid JSON for {state}: {e}\nRaw: {text}")

    return StateResult(
        state=state,
        summary=data["summary"],
        sources=[
            Source(name=s["name"], url=s["url"])
            for s in data.get("sources", [])
        ],
        enforcement_actions=[
            EnforcementAction(
                date=ea["date"],
                type=EnforcementType(ea["type"]),
                description=ea["description"],
                source=Source(name=ea["source"]["name"], url=ea["source"]["url"]),
            )
            for ea in data.get("enforcement_actions", [])
        ],
    )


# ---------------------------------------------------------------------------
# Law resolution
# ---------------------------------------------------------------------------

RESOLVE_LAW_SYSTEM = """You are a US legal research assistant.

Given a vague law description, return a JSON object with exactly these fields:
- canonical_name: the most precise legal name for this law or category
- alternative_names: list of other names this law goes by across states
- federal_analogues: list of relevant federal laws (e.g. COPPA, FERPA)
- search_terms: list of search queries to find this law and related legislation
- novel_theory_terms: list of search queries for cases pursued without a dedicated statute

Return only valid JSON. No commentary."""


async def resolve_law(law: str) -> LawContext:
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        system=RESOLVE_LAW_SYSTEM,
        messages=[{"role": "user", "content": f"Resolve: {law}"}],
    )

    text = extract_json(response.content[0].text)

    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"resolve_law returned invalid JSON: {e}\nRaw response: {text}")

    return LawContext(
        canonical_name=data["canonical_name"],
        alternative_names=data.get("alternative_names", []),
        federal_analogues=data.get("federal_analogues", []),
        search_terms=data.get("search_terms", []),
        novel_theory_terms=data.get("novel_theory_terms", []),
    )


# ---------------------------------------------------------------------------
# State coordinator
# ---------------------------------------------------------------------------

RESULT_JSON_SCHEMA = """{
  "summary": "prose summary of findings",
  "sources": [{"name": "...", "url": "..."}],
  "enforcement_actions": [
    {
      "date": "ISO 8601",
      "type": "law_enforcement | private_civil_suit",
      "description": "...",
      "source": {"name": "...", "url": "..."}
    }
  ]
}"""


async def state_coordinator(state: str, law: LawContext) -> StateResult:
    law_exists = False
    ag_enforcement_signal = False
    civil_suit_signal = False

    system_prompt = f"""You are researching {law.canonical_name} in {state}.

Law context:
- Alternative names: {', '.join(law.alternative_names)}
- Federal analogues: {', '.join(law.federal_analogues)}
- Search terms: {', '.join(law.search_terms)}
- Novel theory terms: {', '.join(law.novel_theory_terms)}

Pipeline:
1. web_search using the provided search terms
2. If law exists: document_analysis on the law URL
3. If law_exists OR ag_enforcement_signal OR civil_suit_signal: enforcement_search
4. document_analysis on each enforcement result

When you have completed your research, return a JSON object with exactly this structure:
{RESULT_JSON_SCHEMA}"""

    messages = [
        {
            "role": "user",
            "content": f"Research {law.canonical_name} (and related laws/actions) in {state}. Find the law, key dates, compliance requirements, and any enforcement actions including novel theory cases.",
        }
    ]

    while True:
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=4096,
            system=system_prompt,
            tools=build_tools(state, law),
            messages=messages,
        )

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            return parse_state_result(state, response.content)

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type != "tool_use":
                    continue

                # programmatic gate enforcement
                if block.name == "document_analysis" and not law_exists:
                    result = json.dumps({"error": "document_analysis blocked: web_search must confirm law exists first"})
                elif block.name == "enforcement_search" and not (law_exists or ag_enforcement_signal or civil_suit_signal):
                    result = json.dumps({"error": "enforcement_search blocked: requires law_exists, ag_enforcement_signal, or civil_suit_signal"})
                else:
                    result = await dispatch_tool(block.name, block.input, law_exists=law_exists)

                    # update gate state after successful web_search
                    if block.name == "web_search":
                        data = json.loads(result)
                        law_exists = check_law_exists(data)
                        ag_enforcement_signal = check_ag_signal(data)
                        civil_suit_signal = check_civil_suit_signal(data)

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                })

            messages.append({"role": "user", "content": tool_results})


# ---------------------------------------------------------------------------
# Master coordinator
# ---------------------------------------------------------------------------

async def master_coordinator(
    states: list[str],
    law: str,
) -> dict[str, StateResult]:
    valid_states = normalise_states(states)
    if not valid_states:
        raise ValueError("No valid US states found in input")

    law_context = await resolve_law(law)
    print(f"Resolved law: {law_context.canonical_name}")
    print(f"States: {valid_states}")

    tasks = [state_coordinator(state, law_context) for state in valid_states]
    results = await asyncio.gather(*tasks)

    return {state: result for state, result in zip(valid_states, results)}


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

process_exit_on_unhandled = True


import sys

def handle_unhandled_rejection(loop, context):
    print(f"Unhandled error: {context['message']}", file=sys.stderr)
    sys.exit(1)


async def main():
    results = await master_coordinator(
        states=["TX", "FL", "Oklahoma"],
        law="age verification legislation for social media",
    )

    for state, result in results.items():
        print(f"\n{'='*60}")
        print(f"STATE: {state}")
        print(f"{'='*60}")
        print(f"Summary: {result.summary}")
        print(f"Sources ({len(result.sources)}):")
        for s in result.sources:
            print(f"  - {s.name}: {s.url}")
        print(f"Enforcement actions ({len(result.enforcement_actions)}):")
        for ea in result.enforcement_actions:
            print(f"  - [{ea.type.value}] {ea.date}: {ea.description}")
            print(f"    Source: {ea.source.name} ({ea.source.url})")


if __name__ == "__main__":
    asyncio.run(main())
