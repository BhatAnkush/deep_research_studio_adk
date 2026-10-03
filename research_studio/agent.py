from google.adk.agents.llm_agent import Agent
from google.adk.tools.google_search_tool import GoogleSearchTool
from google.genai import types

from .tools import fetch_url

MODEL = "gemini-3.5-flash-lite"

INSTRUCTION = """You are a research assistant helping a curious developer understand topics quickly and accurately.

How to answer:
- Start with a 2-3 sentence summary, then give details in short sections.
- Use Google Search for anything recent, changing, or that you are not certain about. Do not search for stable, well-known facts.
- Use fetch_url when the user gives a URL or you need to read a specific page.
- State where key claims come from (site or publication name).
- If sources disagree or the evidence is thin, say so plainly instead of picking a side.
- If you are unsure, say that you are unsure. Never invent sources, numbers or quotes.

What not to do:
- Do not give long answers when a short one covers the question.
- Do not present a guess as a fact."""

root_agent = Agent(
    model=MODEL,
    name="research_assistant",
    description="Answers research questions using web search and returns structured, source-aware summaries",
    instruction=INSTRUCTION,
    tools=[GoogleSearchTool(bypass_multi_tools_limit=True), fetch_url],
    generate_content_config=types.GenerateContentConfig(
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(initial_delay=1, attempts=3)
        )
    ),
)