# project_template

The coding specs for this repo are the Kiro steering files in `.kiro/steering/`. Claude Code loads them as follows, so each rule has one source:

- Always-on steering is imported below.
- Steering that Kiro loads per file pattern is a path-scoped rule in `.claude/rules/`, which loads when Claude reads or edits a matching file.
- Manual steering (`#name` in Kiro) and the `code-reviewer` agent are skills in `.claude/skills/`.

When you add, remove or rename a steering file, or change its `inclusion` or `fileMatchPattern`, update the matching import, rule or skill in the same PR.

@.kiro/steering/agent-defaults.md
@.kiro/steering/coding-guidelines.md
@.kiro/steering/session-handoff.md
