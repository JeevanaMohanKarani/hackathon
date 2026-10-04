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
- [ ] Repo init, `.gitignore`, `.env.example`, `requirements.txt` | Jothik | 0:20-0:40
- [ ] Streamlit skeleton `app.py` with log panel per agent | Jeevana | 0:20-0:40
- [ ] `llm.py`: Gemini + Groq client wrappers (shared) | Jothik | 0:40-1:00
- [ ] SQLite memory: `user_facts`, `history`, `tasks` | Jothik | 0:40-1:00
- [ ] Planner -> Executor (tools) -> Critic loop, max 2 retries if score < 7 | Jothik | 1:00-1:30
- [ ] Mic input + Groq whisper-large-v3 STT | Jeevana | 0:40-1:10
- [ ] Spoken replies with browser speechSynthesis | Jeevana | 1:10-1:30
- [ ] Wire UI to agent loop, show live agent logs | Both | 1:30-2:00
- [ ] Polish + memory demo ("remembers you") | Both | 2:00-2:15
- [ ] Record backup video / screenshots | Jeevana | 2:15-2:30
- [ ] Bug fixes only | Jothik | 2:15-2:30
- [ ] Demo rehearsal (DEMO.md) | Both | 2:30-2:50
- [ ] Submit (checklist in DEMO.md) | Both | 2:50-3:00

## Doing
- [ ] Setup core environment: `.env.example`, `requirements.txt`, `llm.py`, `memory.py` | Both | 0:20-0:40

## Done
- [x] Adapt idea to problem statement, update CONTEXT.md (Voice-to-Task Assistant) | Both | 0:00-0:20
- [x] Team coordination files created | Jothik | pre-hackathon
- [x] Create GitHub repo + add Jothik1506-ai as collaborator; post URL in COMMS.md | Jeevana | before 0:00 (repo: https://github.com/JeevanaMohanKarani/hackathon; Jothik1506-ai confirmed as collaborator 2026-10-04)
