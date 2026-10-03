from google.adk.agents.llm_agent import Agent
from google.adk.models.google_llm import Gemini
from google.adk.models.lite_llm import LiteLlm
from .fallback_llm import FallbackLlm

from .tools import fetch_url, web_search

# Check the exact name on Groq's model list; it must support tool calling.
PRIMARY = "groq/llama-3.3-70b-versatile"
FALLBACK = "gemini-3.5-flash"
llm = FallbackLlm(
    model="fallback-llm",
    primary=LiteLlm(model=PRIMARY),
    fallback=Gemini(model=FALLBACK),
)
INSTRUCTION = """You are a research assistant helping a curious developer understand topics quickly and accurately.

How to answer:
- Start with a 2-3 sentence summary, then give details in short sections.
- Use web_search for anything recent, changing, or that you are not certain about. Do not search for stable, well-known facts.
- Use fetch_url when the user gives a URL or you need to read a specific page.
- State where key claims come from (site or publication name).
- If sources disagree or the evidence is thin, say so plainly instead of picking a side.
- If you are unsure, say that you are unsure. Never invent sources, numbers or quotes.

What not to do:
- Do not give long answers when a short one covers the question.
- Do not present a guess as a fact."""

root_agent = Agent(
    model=llm,
    name="research_assistant",
    description="Answers research questions using web search and returns structured, source-aware summaries",
    instruction=INSTRUCTION,
    tools=[web_search, fetch_url],
)