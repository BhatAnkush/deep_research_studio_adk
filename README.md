# Deep Research Studio

A multi-agent research assistant built with Google ADK (Python). It plans research, gathers sources, critiques its own draft, and writes a cited report.

**Status:** Milestone 2 (one agent with Google Search and a custom `fetch_url` tool).

## Requirements

- Python 3.10+
- A Gemini API key from https://aistudio.google.com/app/apikey
- Git

## Environment variables

Create `research_studio/.env` (inside the agent package, next to `agent.py`). Never commit it.

```
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=your_key_here
GROQ_API_KEY=your_key_here
```

Optional later:

```
MAX_RESEARCHERS=3
MAX_CRITIC_LOOPS=2
```

## Setup

macOS / Linux / WSL:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first.

## Run

Run from the project root (the parent of `research_studio/`):

```bash
adk web .
```

Open http://127.0.0.1:8000 and pick `research_studio`.

Other commands:

- `adk run research_studio` (chat in the terminal)
- `adk eval research_studio evals/research.evalset.json` (later milestone)

## Project structure

```
deep-research-studio/
├── README.md
├── requirements.txt
├── .gitignore
├── research_studio/        # the agent package adk points at
│   ├── .env                # API key (not committed)
│   ├── __init__.py
│   ├── agent.py            # exposes root_agent
│   ├── config.py           # model names, limits
│   ├── agents/             # planner, researcher, synthesizer, critic, writer
│   ├── workflows/          # parallel / loop / sequential wiring
│   ├── tools/              # custom tools (web_fetch)
│   ├── prompts/            # instruction text as .md files
│   ├── schemas/            # structured output models
│   └── callbacks/          # guardrails, logging, budgets
├── evals/                  # evalsets and eval config
├── tests/                  # unit tests for tools
└── scripts/                # deploy helpers
```

## Rules

- The variable in `agent.py` must be named `root_agent`.
- Run `adk` from the parent folder of `research_studio/`.
- Keep the model name in one constant so it is easy to change.
- Cap every loop and every parallel fan-out.

## Roadmap

1. One agent with built-in search ✅
2. Custom tool: `fetch_url` ⌛
3. Planner then researcher, with state via `output_key`
4. Parallel researchers
5. Critic loop with an exit condition
6. Structured outputs
7. Callbacks and guardrails
8. Evals
9. Persistence and Cloud Run deploy
10. TypeScript piece connected via A2A or MCP

## Troubleshooting

| Error | Meaning | Fix |
|---|---|---|
| `ModuleNotFoundError: bs4` | Dependencies missing in the venv | `pip install -r requirements.txt` |
| 404 NOT_FOUND on the model | The model was retired | Change `MODEL` in `agent.py` |
| 429 RESOURCE_EXHAUSTED | Free-tier quota reached | Wait, switch model, or check https://ai.dev/rate-limit |
| 503 UNAVAILABLE | Google's servers are busy | Retry, or switch model |
| Agent missing in the dropdown | Wrong folder or `root_agent` misspelled | Run from the project root and check the name |