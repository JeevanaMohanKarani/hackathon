# MEMORY.md: shared log of decisions and learnings

Add new entries at the **top**. Keep each one short.

## Format
```
### YYYY-MM-DD HH:MM | <who> | <decision or learning>
Why: <one line>
```

## Entries
 
### 2026-10-04 11:25 | Both | Configured live NVIDIA NIM Meta Llama model
Why: Integrated NVIDIA NIM API endpoint for Meta Llama with 10/10 Critic score on live multi-agent task planning and execution.

### 2026-10-04 11:08 | Both | Built & Launched Nova Voice-to-Task Application on Streamlit
Why: Core multi-agent pipeline (Planner, Executor, Critic with automated retry loop), SQLite memory, Whisper voice STT & TTS, and interactive task board are live and running at http://localhost:8501.

### 2026-10-04 10:31 | Both | Confirmed problem statement: Voice-to-Task Assistant
Why: Perfect fit for Nova's voice STT -> multi-agent planner/executor/critic -> SQLite memory -> TTS pipeline; naturally showcases agency, reflection, voice, and persistent memory.

### 2026-10-04 00:17 | Antigravity | Git author and credentials locked to Jothik1506-ai
Why: ensures all commits and pushes are authored and authenticated exclusively as Jothik1506-ai (vanamjothik@gmail.com).

### 2026-10-03 | Jothik | Jeevana creates the GitHub repo; Jothik is added as a collaborator
Why: Jeevana owns the remote; Jothik (GitHub: Jothik1506-ai) needs push access. URL to be posted in COMMS.md.

### 2026-10-03 | Jothik | Claude and Antigravity communicate via team/COMMS.md
Why: a file-based channel lets the agents hand off git requests and flag shared-file edits.

### 2026-10-03 | Jothik | Antigravity handles git actions; created ANTIGRAVITY.md
Why: one agent owns git so commits, branches and merges follow team/RULES.md consistently.

### 2026-10-03 | Jothik | Folder reset to empty
Why: start clean before the hackathon; set up these coordination files first.

### 2026-10-03 | Jothik and Jeevana | Chose "Nova" as the fallback idea
Why: a voice-first multi-agent assistant with memory (Planner, Executor, Critic) hits every judging point and can be adapted to the real problem statement by changing roles and tools.
