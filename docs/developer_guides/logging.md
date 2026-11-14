# Logging Guide

Standards for structured, actionable logging across Kedro pipelines.

## Key Rules

- Use `logging.getLogger(__name__)` (or the project's shared logger helper) consistently.
- Never log secrets, passwords, tokens, or PII.
- Only log what Kedro does not already emit.

## What Kedro Already Logs

Kedro's runner and `DataCatalog` automatically emit:

- Node start and finish (`Running node: ...` / `Completed node: ...`)
- Dataset loading and saving (`Loading data from ...` / `Saving data to ...`)
- Task progress (`Completed N out of M tasks`)
- Pipeline completion time (`Pipeline execution completed successfully in ...`)

Do not add `logger.info("Starting node X")` or `logger.info("Saving output")`.

## Actionability (The 3 a.m. Test)

Every `WARNING` and `ERROR` log must tell an on-call engineer what happened without opening a debugger:

- **Entity:** dataset, node, or group identifier
- **Time window:** date range or period affected (formatted as `YYYY-MM-DD`)
- **Volume:** count of affected rows or items

```python
# Good — identifies entity, clean dates, and row count
logger.warning(
    "Missing %d rows in %s between %s and %s (sample: %s)",
    len(missing_dates),
    dataset_name,
    start_date.strftime("%Y-%m-%d"),
    end_date.strftime("%Y-%m-%d"),
    ", ".join(d.strftime("%Y-%m-%d") for d in missing_dates[:5]),
)
```

Log `merged.shape` at `DEBUG` after `pd.merge` to catch unintended Cartesian explosions early.

## Log Levels

| Level | When to use |
| --- | --- |
| `DEBUG` | Diagnostic details (shapes, intermediate counts) needed only when troubleshooting |
| `INFO` | Meaningful milestones not already emitted by Kedro |
| `WARNING` | Unexpected condition or expected data deviation where execution continues |
| `ERROR` | Operation failed or data contract violated; include inputs and exception |
| `CRITICAL` | Fatal error preventing the program from continuing |

## String Formatting Rules

| Context | Format | Reason |
| --- | --- | --- |
| `logger.*()` calls | Lazy `%`: `logger.info("val: %s", val)` | Avoids formatting when disabled; groups log templates |
| `raise` / exceptions | f-string: `raise ValueError(f"bad: {val}")` | Ruff `UP031` enforces f-strings outside logging |
| General strings | f-string | Readability; Ruff `UP031` |

Cap logged collections to 5–10 items with an `(and N more)` suffix.
