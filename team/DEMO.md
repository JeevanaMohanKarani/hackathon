# DEMO.md: pitch, demo, backup, submission

## Pitch script (60-90 s)
1. **Hook (10 s):** "`<TBD: problem in one sentence>`. What if you could just say it out loud?"
2. **What (15 s):** "Nova is a voice-first team of AI agents. A Planner breaks the task down, an Executor does it with real tools, and a Critic scores the result and sends it back if it's not good enough."
3. **Live demo (40 s):** see steps below.
4. **Memory (10 s):** "Nova remembers you across sessions, so it gets better the more you use it."
5. **Close (10 s):** "Autonomous, self-checking, voice-first agents with memory. That's Nova." 

## Demo steps
1. Open the app (`streamlit run app.py`), logs visible.
2. Speak a request: `<TBD: demo prompt>`.
3. Point at the live logs: Planner plan -> Executor tool calls -> Critic score (show a retry if possible).
4. Nova answers out loud.
5. Tell Nova a fact ("I prefer ..."), refresh/restart, ask again: it remembers.

## Backup plan (APIs fail or Wi-Fi drops)
- Recorded demo video: `<TBD: path/link>` (record at 2:15-2:30).
- Screenshots of each step: `<TBD: folder>`.
- Pre-typed text input if the mic fails.
- Hotspot ready as backup network.

## Submission checklist
- [ ] `main` runs from a fresh clone (setup steps in CONTEXT.md)
- [ ] `.env` NOT committed; `.env.example` present
- [ ] README / description with problem, solution, architecture
- [ ] Demo video link: `<TBD>`
- [ ] Repo link: `<TBD>`
- [ ] Submitted on: `<TBD: platform>` before 3:00
