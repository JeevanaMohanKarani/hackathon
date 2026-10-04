# ANTIGRAVITY.md: start here (Antigravity agent, git actions)

Team: **Jothik** and **Jeevana**. 3-hour hackathon on 2026-10-04, project "Nova". You handle all git actions for the team.

## 1. Before and after any work
Before: read, in order, `team/RULES.md`, `team/CONTEXT.md`, `team/MEMORY.md`, `team/TASKS.md`.
After: update `team/TASKS.md` (move or update the task) and add an entry at the top of `team/MEMORY.md` (format is in that file).

## 2. Git workflow

### First-time setup (per machine)
`git init -b main` is already done. Then:
```bash
git remote add origin <TBD repo URL>
git config user.name "<Jothik or Jeevana>"
git config user.email "<that person's own email>"   # ask the human; never hardcode it here
```

### Start a task
```bash
git checkout main && git pull --rebase
git checkout -b <name>/<feature>        # e.g. jothik/critic, jeevana/voice
```

### Commit
- Run `git status` first. Never `git add -A` or `git add .` blindly.
- Stage specific files only: `git add <file1> <file2>`.
- Small commits. Message format `<Name>: <what>`, e.g. `Jothik: add critic retry loop`.
```bash
git status
git add agents/critic.py
git commit -m "Jothik: add critic retry loop"
```

### Sync and merge
```bash
git fetch origin
git rebase origin/main                  # on your feature branch
# check the app still runs: source .venv/bin/activate && streamlit run app.py
git checkout main && git pull --rebase
git merge --ff-only <name>/<feature>    # or open a PR instead
git push origin main                    # ask the human first
git branch -d <name>/<feature>          # only your own branch
```
`main` must always run.

### Conflicts
Stop. Run `git status` and show the conflicting files to the human. Do not guess on files owned by the other person; ask them. Abort with `git rebase --abort` / `git merge --abort` if unsure.

## 3. Hard rules
Never:
- commit `.env`, `.venv/`, `nova.db`, `team/`, `CLAUDE.md` or `ANTIGRAVITY.md` (commit `.env.example` only)
- force-push to `main`, run `git reset --hard`, or `git clean -fd`
- rewrite history that has been pushed
- delete branches belonging to the other person

Always ask the human before any destructive command and before every push.

## 4. File ownership (from team/RULES.md)
| Area | Owner | Files (planned) |
|---|---|---|
| Agents and backend | Jothik | `agents/`, `memory.py`, `tools.py` |
| UI, voice and demo | Jeevana | `app.py`, `voice.py`, `DEMO.md` |
| Shared | Both | `llm.py`, `requirements.txt`, `.env.example`, `*.md` |

Only stage and commit files owned by the human you work for. Shared files: the teammate must OK the change first.

## 5. After feature freeze (2:15)
Bug-fix commits only. Before the demo, tag the working state (ask the human before pushing):
```bash
git tag demo-v1
git push origin demo-v1
```

## 6. Quick reference
| Goal | Command |
|---|---|
| See state | `git status` / `git status --short` |
| Update main | `git checkout main && git pull --rebase` |
| New branch | `git checkout -b <name>/<feature>` |
| Stage file | `git add <file>` |
| Unstage file | `git restore --staged <file>` |
| Commit | `git commit -m "<Name>: <what>"` |
| See diff | `git diff` / `git diff --staged` |
| History | `git log --oneline -10` |
| Rebase on main | `git fetch origin && git rebase origin/main` |
| Abort rebase | `git rebase --abort` |
| Merge | `git checkout main && git merge --ff-only <branch>` |
| Push (ask first) | `git push origin <branch>` |
| Delete own branch | `git branch -d <name>/<feature>` |
| Demo tag | `git tag demo-v1` |

## 7. Communication
- Read `team/COMMS.md` before and after each task; handle open messages addressed to Antigravity (fill in the reply, set status to done).
- Report commit hashes, conflicts or questions back there; post your own requests at the bottom.
