---
paths:
  - ".claude/rules/*.md"
---

# Steering File Standards

## Purpose

A steering file is a scoped instruction set that shapes agent behavior. It is consumed as context tokens on every matching interaction, so every line has a cost. Write steering files like you write production code: minimal, precise, and justified.

## When to Create a New Steering File

Create one when you observe the agent repeatedly making the same mistake or missing the same convention. A steering file is a fix for a recurring pattern, not a preemptive rulebook.

Do NOT create a steering file for:

- One-off instructions (use chat instead)
- General knowledge the model already has (Python syntax, pandas API)
- Rules that duplicate another steering file

## Structure

Every steering file must have:

1. **Front-matter** with `paths:` glob list if scoped (omit `paths:` for always-on rules)
2. **A single `#` title** that names the domain
3. **Sections** that group related rules, each ≤15 lines
4. **Examples** only when the rule is ambiguous without one (good vs bad pattern)

````markdown
---
paths:
  - "src/**/*.py"
---

# [Domain] Standards

## Rule Group

- Rule as imperative sentence
- Rule as imperative sentence

## Code Pattern (only if needed)

\```python

# Good

...

# Bad

...
\```
````

## Front-Matter Rules

| Mode        | Use When                                                                               |
| ----------- | -------------------------------------------------------------------------------------- |
| `always`    | Rule applies to every interaction regardless of files (use sparingly — one or two max) |
| `fileMatch` | Rule applies only when matching files are in context (preferred)                       |
| `manual`    | User must explicitly reference via `#name` in chat (checklists, reference docs)        |

Default to `fileMatch`. Use `always` only for behavioral guidelines that transcend file types. Every `always` file burns tokens on every single interaction.

## Sizing Guidelines

- **Target: 50–120 lines.** Enough to be useful, small enough to stay in context without crowding out the user's actual code.
- **Hard ceiling: 200 lines.** If a file exceeds this, split it by sub-domain or move examples to a `manual` reference file.
- **No filler.** Cut motivational preambles, obvious rules, and anything the agent already does correctly without prompting.

## Writing Rules

- **Imperative voice.** "Use lazy % formatting" not "You should consider using lazy % formatting."
- **One rule per bullet.** If a bullet has "and", split it.
- **No redundancy across files.** Before adding a rule, grep existing steering files. If it exists, don't duplicate — reference the file by name if needed.
- **Examples earn their space.** Include a good/bad pair only when the rule is genuinely ambiguous. Skip examples for obvious rules like "add type hints."
- **Domain-specific over generic.** "Log farm, variety, and season in WARNING messages" beats "Include context in log messages."

## Anti-Patterns

- **The encyclopedia.** A 500-line file that restates language docs. The agent already knows Python — tell it what's unique to this project.
- **The overlap.** Two files both defining docstring format. Pick one owner.
- **The always-on firehose.** Multiple `always` files totaling 800+ lines. Most rules should be scoped to the files they affect.
- **The aspirational rulebook.** Rules the team doesn't actually follow. Steering files enforce current practice, not wishful standards.

## Maintenance

- Review steering files when they stop preventing mistakes (the agent learned, or the rule is stale).
- Delete rules that duplicate what the model does by default.
- When a steering file grows past 200 lines, split it or prune examples.
