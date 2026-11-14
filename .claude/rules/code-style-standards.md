---
paths:
  - "src/**/*.py"
---

# Code Style Standards

## Functional & Pure Style

- Write pure functions: never mutate arguments or globals in place; `.copy()` mutable inputs before modifying.
- Split the decision (pure function returning a verdict) from the action (side effects) so logic is testable without mocks.
- Keep functions around 30 body lines or fewer (excluding signature, docstring, comments, and blank lines).
- Break long pandas chains into named intermediate variables (one or two related operations per line).

## Readability & Signatures

- Use descriptive, pronounceable names; keep one name per concept across the codebase (`client` vs `customer`).
- Keep function signatures to `≤5` arguments; group related parameters in a `dict` or dataclass when larger.
- Use keyword arguments in calls passing more than two arguments.
- Avoid boolean flag parameters (`flag: bool`); split into two clearly named functions instead.
- Write Google-style docstrings for non-trivial functions, starting the summary on a new line after `"""`.

## Top-Down Function Ordering

- Place the public or entry-point function (e.g., the Kedro node) first.
- Place its helpers immediately after it in the order they are first called; a helper's own helpers follow it.
- Place a shared helper under its first consumer; do not duplicate or repeat it below later callers.

## Fail Loud & Data Integrity

- Put guard clauses first so the happy path is never buried inside nested `if` blocks.
- Read required config strictly (`params["key"]`, not `.get(key, default)`); let missing keys raise.
- Handle errors in three tiers: (1) catch specific exceptions when auto-fixable (never bare `except`); (2) `raise ValueError(...)` naming the dataset, columns, and offending values when unfixable; (3) `logger.warning(...)` for expected deviations.
- Add a custom exception subclass only when a caller branches on it.
- Avoid silent fallbacks (`fillna`, `drop(..., errors="ignore")`, `dropna`, truncating `.astype(int)`, inner joins, last-write-wins dedup); if a fallback is intentional, count and log affected rows.
- Pass `validate=...` to `pd.merge` (e.g., `validate="many_to_one"`) and run `ffill`, `bfill`, `shift`, and rolling windows inside `groupby` on entity keys.
- Return empty schema-compliant DataFrames (`Schema.empty()`) for empty inputs rather than crashing downstream.
- Pair `isocalendar().week` with `isocalendar().year`, never with calendar year.

## Constants & Performance

- Keep a constant local to its function until a second function reads it, then move it to module top or a constants module with `Final`.
- Use an `Enum` for closed sets of values callers must exhaustively handle.
- Profile before optimizing; prefer vectorized pandas/NumPy operations over `.iterrows()` or Python loops.

Full guide with examples: [docs/developer_guides/code_style.md](../../docs/developer_guides/code_style.md).
