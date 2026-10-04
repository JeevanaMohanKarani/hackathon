# RULES.md: team rules

## Git
- `main` must always run.
- Use short feature branches (`jothik/critic`, `jeevana/voice`), or `git pull --rebase` before every push.
- Keep commits small. Start the message with your name, e.g. `Jothik: add critic retry loop`.
- **Never commit `.env`.** Commit `.env.example` only.

## File ownership (<adjustable>)
| Area | Owner | Files (planned) |
|---|---|---|
| Agents and backend | Jothik | `agents/`, `memory.py`, `tools.py` |
| UI, voice and demo | Jeevana | `app.py`, `voice.py`, `DEMO.md` |
| Shared | Both | `llm.py`, `requirements.txt`, `.env.example`, `*.md` |

So the two of you never edit the same file at once.

## Communication
- Check in every 30 minutes (0:30, 1:00, 1:30, 2:00, 2:30).
- Post a message **before** changing a shared file.
- Ask your teammate before deleting anything.

## Time
- **Feature freeze at 2:15.** After that: bug fixes and demo rehearsal only.

## AI agents
- Stay within your human owner's files.
- If a change is needed in someone else's file, stop and say so; do not make it.
- Update `TASKS.md` and `MEMORY.md` after finishing a task.
