# CONTEXT.md: project context

## Hackathon
- Length: 3 hours. Theme: **autonomous AI agents**.
- Judges value: AI agents, voice, persistent memory, several agents working together.
- Problem statement release: **2026-10-04, 10:00 AM**.
- Venue / submission link: `<TBD>`

## Problem statement
> **Voice-to-Task Assistant**: An intelligent voice-first agentic system that transforms spoken requests into structured, actionable, and self-improving tasks with persistent memory and multi-agent validation.

How VoxFlow maps to it:
- **Voice STT**: Mic input captured and transcribed via Groq Whisper (`whisper-large-v3`).
- **Memory Layer**: SQLite persistent memory for storing user facts, recurring tasks, task states, context history, and follow-ups.
- **Multi-Agent Core**:
  - **Planner Agent (Meta Llama / Gemini)**: Deconstructs voice commands, identifies user intent, checks previous memory/context, and formulates step-by-step task plans.
  - **Executor Agent (Multi-Tool Engine)**: Executes task actions, queries external APIs/tools, manages calendar/reminders/todos.
  - **Critic Agent (Reflection & Scoring)**: Evaluates the execution quality (score 1-10), reviews criteria compliance, and triggers automated retries (max 2) if score < 7.
- **Voice TTS**: Browser `speechSynthesis` / audio output speaking concise status updates and conversational confirmations.
- **Live Agent UI**: Streamlit dashboard with real-time agent chain breakdown, task cards, and memory inspector.

## Idea: VoxFlow (Voice-to-Task Assistant)
Voice-first, multi-agent assistant with memory.
**Pitch:** "Talk to VoxFlow. A planner, an executor and a critic work together, check their own work, and remember you."

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
