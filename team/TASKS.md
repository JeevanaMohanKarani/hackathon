# TASKS.md: task board

Times are hackathon elapsed time (0:00 = start). Move tasks between sections; keep owner and slot.

## Timeline
| Slot | Goal |
|---|---|
| 0:00-0:20 | Read problem, adapt Nova idea, update CONTEXT.md |
| 0:20-0:40 | Setup: repo, venv, `.env`, skeleton files |
| 0:40-1:30 | Core: agent loop + memory / UI + voice |
| 1:30-2:15 | Integrate, end-to-end flow, polish |
| **2:15** | **Feature freeze** |
| 2:15-2:30 | Bug fixes, record backup video |
| 2:30-3:00 | Demo rehearsal, submission |
| **3:00** | **Submit** |

## Todo
- [ ] Polish + memory demo scenarios ("remembers you") | Both | 2:00-2:15
- [ ] Record backup video / screenshots | Jeevana | 2:15-2:30
- [ ] Bug fixes only | Jothik | 2:15-2:30
- [ ] Demo rehearsal (DEMO.md) | Both | 2:30-2:50
- [ ] Submit (checklist in DEMO.md) | Both | 2:50-3:00

## Doing
- [ ] Demo rehearsal and end-to-end voice loop testing | Both | 1:30-2:00

## Done
- [x] Streamlit dashboard with live agent cards & memory inspector (`app.py`) | Jeevana | 0:20-0:40
- [x] `llm.py`: Gemini + Groq multi-provider connectors | Jothik | 0:40-1:00
- [x] SQLite memory: `user_facts`, `tasks`, `execution_history` (`memory.py`) | Jothik | 0:40-1:00
- [x] Planner -> Executor (tools) -> Critic loop with self-reflection retries (`agents/`) | Jothik | 1:00-1:30
- [x] Mic input + Groq whisper-large-v3 STT & browser TTS (`voice.py`) | Jeevana | 0:40-1:30
- [x] Wire UI to multi-agent orchestrator loop | Both | 1:30-2:00
- [x] Adapt idea to problem statement, update CONTEXT.md (Voice-to-Task Assistant) | Both | 0:00-0:20
- [x] Team coordination files created | Jothik | pre-hackathon
- [x] Create GitHub repo + add Jothik1506-ai as collaborator; post URL in COMMS.md | Jeevana | before 0:00
