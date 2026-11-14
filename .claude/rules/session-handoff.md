# Session Handoff

When starting a new session or picking up work from another machine/agent:

1. Read `changelogs/epics/<TICKET-ID>-short-title.md` — `## Brief` for intent and pass criteria, `## Progress` for current state and next steps, `## Decisions` for prior technical choices
2. Check `git log --oneline -10` for recent commits
3. Check `git status` for uncommitted work

This avoids re-reading the entire codebase on every session start.

## Multi-agent coordination

- Each agent works on its own branch (tied to a Jira epic)
- Each epic has its own `changelogs/epics/<TICKET-ID>-short-title.md` file
- Commit changelogs to the branch before switching agents

## Cross-machine workflow

1. Finish work → commit + push (including changelogs/)
2. Switch machine → git pull
3. Read `changelogs/epics/<TICKET-ID>-short-title.md` → resume where you left off
