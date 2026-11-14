# project_template

Project conventions and engineering rules live in `.claude/`:

- **Always-on rules** (`.claude/rules/` without `paths:` front-matter): `agent-defaults.md`, `coding-guidelines.md`.
- **Path-scoped rules** (`.claude/rules/` with `paths:` front-matter): load automatically when reading or editing matching files.
- **Skills** (`.claude/skills/`): on-demand workflows (`code-reviewer`, `code-review-checklist`, `worktrees`).
