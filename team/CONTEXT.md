# CONTEXT.md: project context

## Hackathon
- Length: 3 hours. Theme: **autonomous AI agents**.
- Judges value: AI agents, voice, persistent memory, several agents working together.
- Problem statement release: **2026-10-04, 10:00 AM**.
- Venue / submission link: `<TBD>`

## Problem statement
> `<TBD: paste the problem statement here when it is released>`

How Nova maps to it: `<TBD: new agent roles and tools>`

## Idea: Nova (fallback, adapt to the problem)
Voice-first, multi-agent assistant with memory.
**Pitch:** "Talk to Nova. A planner, an executor and a critic work together, check their own work, and remember you."

Adapting: change the agents' roles and tools to fit the problem; keep the loop, voice and memory.

## Architecture
```
 Mic --> Groq whisper-large-v3 (STT) --> text
                                          |
                                          v
           +------------- SQLite memory (user_facts, history)
           |                              |
           v                              v
     Planner (Gemini) --> Executor (Groq + tools) --> Critic (score 1-10)
                                ^                         |
                                +---- retry if < 7 -------+  (max 2 retries)
                                                          |
                                                          v
           Streamlit UI (live log per agent) --> browser speechSynthesis (TTS)
```

## Stack
Python 3 with `.venv`; `google-genai`, `groq`, `python-dotenv`, `streamlit`, `requests`. SQLite (stdlib).

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt   # or: pip install google-genai groq python-dotenv streamlit requests
cp .env.example .env              # then fill in GEMINI_API_KEY and GROQ_API_KEY
```
`.env.example`:
```
GEMINI_API_KEY=
GROQ_API_KEY=
```

## Run
```bash
source .venv/bin/activate
streamlit run app.py   # entry file name <TBD>
```
