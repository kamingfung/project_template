---
inclusion: always
---

# Coding Guidelines

Behavioral rules that apply to every interaction. File-specific rules live in
the other steering files (`code-style-standards.md`, `unit-test-standards.md`,
`logging-standards.md`).

## 1. Think Before Coding

- State assumptions explicitly. If uncertain, ask.
- Present multiple interpretations when options exist; do not pick silently.
- Suggest simpler approaches when warranted.
- Stop when unclear. Name what is confusing and ask for clarification.

Examples of good questions:

- "Should I handle missing values here, or assume they're cleaned upstream?"
- "I see two approaches: (1) vectorized pandas, (2) iterative with validation.
  Which fits better?"

## 2. Simplicity First

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that was not requested.
- No error handling for impossible scenarios.
- If you wrote 200 lines and it could be 50, rewrite it.

Self-check: "Would a senior engineer say this is overcomplicated?" If yes,
simplify.

Stop and simplify when you notice:

- A parameter you're not using
- Infrastructure for "future needs"
- Edge cases that cannot happen
- Configuration for a single use case

## 3. Surgical Changes

- Every changed line must trace directly to the user's request.
- Do not "improve" adjacent code, comments, or formatting.
- Do not refactor things that are not broken.
- Match existing style even if you would do it differently.
- Mention unrelated dead code — do not delete it.

When your changes create orphans:

- Remove imports/variables/functions that YOUR changes made unused.
- After deleting a node or function, `git grep` each name, param key, dataset and helper it used across `src/`, `conf/`, `tests/` and `docs/`; delete every one left with no reader (YAML blocks, catalog entries, test fixtures, shared `utils/` helpers, doc links).
- Delete code your change turns into a no-op (a dedup that can no longer find duplicates, a fallback that can no longer trigger).
- Do NOT remove pre-existing dead code unless asked.

## 4. Comments and Documentation Placement

Follow the explanation cascade — stop at the first level that is sufficient:

1. **Descriptive name** — rename; no comment needed.
2. **Concise inline comment** — one short phrase if the name isn't enough.
3. **Docstring** — when the _why_ needs a paragraph.
4. **External doc** — route by stability: reproducible/stable → `docs/`; branch-specific/may-change → `changelogs/epics/<TICKET-ID>.md`.

Full routing table: [`code_style.md` — Where explanation belongs](../../docs/dev_guidelines/code_style.md#where-explanation-belongs).

- Keep ticket ids (`<TICKET-ID>`) and dates out of code comments, docstrings, test names and docstrings, YAML comments and doc headings; they belong in the changelog and the commit message.
- Before a comment, docstring, doc or PR description states what code does or who reads a column, dataset or param, check it: read the code path and `git grep` the name across `src/` and `conf/`. Name the reader you found, not the one you expect.
- Do not describe behavior the code does not implement (a gate, a fallback, a consumer).

## 5. Goal-Driven Execution

Transform vague tasks into verifiable goals before starting:

| Vague Request         | Verifiable Goal                                       |
| --------------------- | ----------------------------------------------------- |
| "Add validation"      | "Write tests for invalid inputs, then make them pass" |
| "Fix the bug"         | "Write a test that reproduces it, then make it pass"  |
| "Refactor X"          | "Tests pass before and after"                         |
| "Improve performance" | "Reduce execution time from X to Y seconds"           |

A change that can move model outputs (features, model inputs, model params, a bug fix in a pipeline the models read) is verified by a backtest, not by tests alone: run the affected model's backtest on `main` and on the branch, and record both metrics and run ids in the changelog before requesting review. A pure refactor or deletion of unread code instead shows that outputs are unchanged.

For multi-step tasks, state a brief plan with verifiable checkpoints before
implementing.

## 6. American English

Write American English everywhere: prose, docstrings, comments, commit messages, new identifiers, Jira and Confluence text.

- `-ize` / `-ization`, not `-ise` / `-isation`: minimize, optimize, normalize, regularize, summarize, initialize, visualize, organization.
- `-or`, not `-our`: behavior, color, favor, neighbor.
- Single `l` before a suffix: modeled, labeled, canceled.
- `-er`, not `-re`: center, meter.
- Unchanged either way, do not "fix" these: analysis, analyses, basis, exercise, advertise, supervise, surprise.
- Match an existing identifier's spelling even when it is British; renaming a symbol is a separate change from writing prose.
