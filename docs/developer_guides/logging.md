# Logging Guide

Standards for structured, actionable logging across Kedro pipelines.

## 1. Key Rules

- Use `logging.getLogger(__name__)` consistently at module top.
- Never log secrets, passwords, API keys, tokens, or PII.
- Only log what Kedro does not already emit.

## 2. What Kedro Already Logs (Do Not Duplicate)

Kedro's runner and `DataCatalog` automatically emit:

- **Node start and finish:** `Running node: ...` / `Completed node: ...`
- **Dataset loading and saving:** `Loading data from ...` / `Saving data to ...`
- **Task progress:** `Completed N out of M tasks`
- **Pipeline completion time:** `Pipeline execution completed successfully in ...`

Do not add `logger.info("Starting node X")` or `logger.info("Saving output")`.

## 3. Mandatory Context (The 3 a.m. Actionability Test)

Every `WARNING` and `ERROR` log must tell an on-call engineer what happened without opening a debugger:

- **Entity:** dataset, node, or group identifier (`company_id`, `shuttle_type`)
- **Time window:** date range or period affected (formatted as `YYYY-MM-DD`)
- **Volume:** count of affected rows or groups

```python
# Good — identifies entity, clean dates, and row count with a capped sample
logger.warning(
    "Missing %d week(s) in %s between %s and %s (sample: %s)",
    len(missing_dates),
    group_id,
    start_date.strftime("%Y-%m-%d"),
    end_date.strftime("%Y-%m-%d"),
    ", ".join(d.strftime("%Y-%m-%d") for d in missing_dates[:5]),
)
```

Log `merged.shape` at `DEBUG` after `pd.merge` to catch unintended Cartesian explosions early:

```python
merged = pd.merge(left_df, right_df, on=keys, how="left", validate="many_to_one")
logger.debug("Merged result shape: %s", merged.shape)
```

## 4. Log Levels & Exception Logging

| Level | When to use |
| --- | --- |
| `DEBUG` | Diagnostic details (shapes, intermediate counts) needed only when troubleshooting |
| `INFO` | Meaningful pipeline milestones not already emitted by Kedro |
| `WARNING` | Unexpected condition or expected data deviation where execution continues |
| `ERROR` | Operation failed or data contract violated; include input context and exception |
| `CRITICAL` | Fatal error preventing the program from continuing |

Never swallow exceptions with bare `except:` or log a vague message without input context:

```python
# Bad — bare except, deprecated warn(), no inputs or error details
try:
    compute_metrics(df, threshold)
except:
    logger.warn("compute_metrics failed")

# Good — specific exception, inputs and error included
try:
    compute_metrics(df, threshold)
except ValueError as err:
    logger.error(
        "compute_metrics failed for threshold=%s (rows=%d): %s",
        threshold,
        len(df),
        err,
    )
    raise
```

## 5. String Formatting & Anti-Patterns

| Context | Format | Reason |
| --- | --- | --- |
| `logger.*()` calls | Lazy `%`: `logger.info("val: %s", val)` | Avoids formatting when disabled; groups log templates |
| `raise` / exceptions | f-string: `raise ValueError(f"bad: {val}")` | Ruff `UP031` enforces f-strings outside logging |
| General strings | f-string | Readability; Ruff `UP031` |

- **No f-strings in log calls** — always use lazy `%` formatting.
- **No raw `Timestamp` objects** — format dates as `YYYY-MM-DD` strings.
- **No unbounded lists** — cap logged collections to 5–10 items with an `(and N more)` suffix.
- **No "I am here" logs** — never write `logger.info("Step 1")`.
