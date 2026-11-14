---
paths:
  - "changelogs/**/*.md"
---

# Progress Tracking & Changelog Convention

## Overview

One file per epic. No folders, no ceremony.

```
changelogs/
├── DECISIONS.md                    ← Repo-wide (shared, append-only)
└── epics/
    └── <TICKET-ID>-short-title.md     ← Brief + Progress + Decisions in one file
```

---

## Epic File Template

Always in this section order: **Brief → Progress → Decisions**.

```markdown
# <TICKET-ID> — <Short Title>

## Brief

<!-- Written at epic creation. Do not edit. -->

**Spec:** `.kiro/specs/<spec-dir>/` ← omit if no spec exists
**Goal:** <distilled from spec Introduction OR manual motivation>
**Pass criteria:** <condensed from spec acceptance criteria OR manual pass/fail>
**Links:** [<TICKET-ID>](url) | PR #NNN

---

## Progress

Status: On track / At risk / Blocked / Done ✓

### Last completed

- <completed item>

### Next: start here

- [ ] <next item — include file paths if relevant>

### Blockers

- None

---

## Decisions

### YYYY-MM-DD: <Short description>

**Chose:** <what was decided>
**Over:** <what was rejected>
**Because:** <the actual reason>
```

---

## Section Rules

| Section   | Who writes                      | When                                 | Editable?             |
| --------- | ------------------------------- | ------------------------------------ | --------------------- |
| Brief     | Epic owner (or agent from spec) | At epic start, before implementation | No — write once       |
| Progress  | Agent (stop hook)               | Every session                        | Yes — update in place |
| Decisions | Any contributor                 | At each decision point               | Append-only           |

**Populating Brief from a spec:** If a `.kiro/specs/` entry exists for the epic, search for
the spec by grepping for the Jira ticket number in `requirements.md`. Extract the Introduction
as **Goal** and condense the key acceptance criteria as **Pass criteria**. Add a **Spec**
pointer. If no spec exists, write manually and mark unknowns with `[TODO]`.

---

## Repo-wide DECISIONS.md

Same format as per-epic Decisions section but scoped to decisions that affect the whole
repo — architecture, platform, tooling, data contracts. Lives at `changelogs/DECISIONS.md`.

---

## Rules

1. **One file per Jira ticket** — named `<TICKET-ID>-short-title.md`
2. **Commit changelogs with your feature branch** — not on a separate branch
3. **Brief is written before implementation** — not after
4. **Progress is updated every session** — by the stop hook, not manually
5. **Decisions are append-only** — never edit past entries
6. **Files stay after merge** — they are historical record
7. **Focus on Why, not What** — code shows What; changelogs explain Why

---

## Agent Behavior

- **Session start:** `.kiro/steering/session-handoff.md` (auto-loaded) — read the epic file
- **Session end:** `.kiro/hooks/update-progress-on-stop.json` (auto) — updates `## Progress`,
  scaffolds a new epic file if missing (populating Brief from spec if found), and appends a
  `### Drift Warning` to Progress if the session deviated from Brief's Goal or Pass criteria
