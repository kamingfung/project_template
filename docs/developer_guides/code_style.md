# Code Style Guide

Practical Python and Kedro coding standards for this repository.

## Before You Write

Stop at the first rung that holds. Only descend when the rung above genuinely does not fit:

1. **Does this need to exist at all?** Speculative need -> skip it (YAGNI).
2. **Does stdlib cover it?** Use it instead of hand-rolling.
3. **Does an already-installed dependency cover it?** Use it; never add a dependency for what a few lines can do.
4. **Can it be one line?** Write one line.
5. **Only then:** write the minimum code that works — no scaffolding, no "for later".

If you consciously stop above a full implementation because a simpler form holds for now, leave a plain-words comment naming the limit and the upgrade path:

```python
# Linear scan; fine below ~10k rows. Switch to an index lookup above that.
match = next((r for r in records if r["id"] == target_id), None)
```

## Functional & Pure Style

- **Pure functions:** same inputs produce the same outputs; never mutate arguments or globals in place. Always `.copy()` mutable DataFrames, dicts, or lists before modifying.
- **Split the decision from the action:** write a pure function that returns a verdict, and a separate function that executes side effects. The decision function is testable without mocks.
- **Keep functions small:** aim for ~30 body lines or fewer (excluding signature, docstring, comments, and blank lines).
- **Readable pandas:** break long chains into named intermediate variables with one or two related operations per line.

```python
# Bad — mutates input in place
def add_ratio(df: pd.DataFrame) -> pd.DataFrame:
    df["ratio"] = df["num"] / df["den"]
    return df


# Good — pure, explicit copy
def add_ratio(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    result["ratio"] = result["num"] / result["den"]
    return result
```

## Readability & Signatures

- **Descriptive, pronounceable names:** `current_date` instead of `ymdstr`; `company` instead of `item` in loops.
- **One concept, one name:** do not alternate between `client`, `customer`, and `account` for the same entity.
- **Keep signatures small (`≤5` arguments):** group related parameters into a `dict` or dataclass when the list grows.
- **Keyword arguments for `>2` arguments:** use keyword arguments in both `src/` and `tests/` so signature reordering cannot silently swap values.
- **No boolean flag parameters:** split `f(x, flag=True)` into two clearly named functions.
- **Google-style docstrings:** start on a new line after `"""` and include types in the function signature.

## Top-Down Function Ordering

Arrange functions so readers encounter callers before callees:

1. Public or entry-point function first (e.g., the Kedro node registered in `pipeline.py`).
2. Its helpers immediately after, ordered by first appearance in the entry-point body.
3. Helpers of helpers follow their parent helper.
4. Shared helpers sit under their first consumer; do not duplicate or repeat them below later callers.

## Fail Loud & Data Integrity

- **Guard clauses first:** validate preconditions and return or raise at the top so the happy path is never nested.
- **Strict config reads:** read required config with `params["key"]`, never `.get(key, default)`.
- **Three-tier error handling:**
  1. Anticipated + auto-fixable -> `try`/`except` with a specific exception type (never bare `except`).
  2. Anticipated + unfixable -> `raise ValueError(...)` naming the dataset, columns, and offending values.
  3. Expected deviation -> `logger.warning(...)` with entity, window, and row count.
- **Custom exceptions:** add a subclass only when a caller branches on it.
- **No silent fallbacks:** avoid `fillna`, `drop(..., errors="ignore")`, `dropna`, truncating `.astype(int)`, inner joins that drop rows, or last-write-wins dedup without counting and logging touched rows.
- **Validate joins and grouped ops:** pass `validate=...` to `pd.merge` (e.g., `validate="many_to_one"`) and run `ffill`, `bfill`, `shift`, and rolling windows inside `groupby` on entity keys.
- **Empty in, empty out:** return an empty schema-compliant DataFrame (`Schema.empty()`) for empty inputs.
- **ISO year with ISO week:** pair `isocalendar().week` with `isocalendar().year`, never with calendar year.

## Constants & Performance

- Keep a constant local to its function until a second function reads it; then move it to module top or a constants module annotated `Final`.
- Use `Enum` for closed sets of values callers must exhaustively handle.
- Profile before optimizing; prefer vectorized pandas/NumPy operations over `.iterrows()`.

## Where explanation belongs

When a name alone is not enough, follow the cascade and stop at the first level that suffices:

1. **Descriptive name** — rename the variable or function; no comment needed.
2. **Concise inline comment** — one short phrase if the name still leaves ambiguity.
3. **Docstring** — when the _why_ behind a function needs a paragraph.
4. **External doc** — when detail exceeds the scope of a single function. Route by stability:

| Content type | Reproducible & stable? | Where it goes |
| --- | --- | --- |
| Design decisions, parameter semantics, architecture | Yes | `docs/` |
| Experiment tables, backtest numbers, arm comparisons | No (branch-specific) | `changelogs/` or PR description |
| Branch rationale that may change before merge | No | `changelogs/` or PR description |

## See also

- [logging.md](logging.md) — logger setup, log levels, 3 a.m. actionability test
- [unit_test.md](unit_test.md) — test structure, fixtures, Pandera boundaries, mocking rules
- [visualization.md](visualization.md) — colorblind-safe palettes and diagramming
- [writing_standards.md](writing_standards.md) — ASD-STE100 prose and documentation structure
