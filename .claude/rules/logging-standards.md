---
paths:
  - "src/**/*.py"
---

# Logging Standards

## Logger & Hygiene

- Use `logging.getLogger(__name__)` (or the project's shared logger helper) consistently.
- Never log secrets, credentials, tokens, or PII.
- Do not duplicate logs Kedro already emits (node start/finish, dataset load/save, task progress, pipeline completion time).

## Actionability (3 a.m. Test)

- Include the entity identifier, time window, and count of affected rows in every `WARNING` and `ERROR` log.
- Log `merged.shape` at `DEBUG` after `pd.merge` to surface unintended Cartesian explosions.
- Include input values and error context when logging caught exceptions.

## Log Levels

- `DEBUG`: Diagnostic details (shapes, intermediate counts) useful only when troubleshooting.
- `INFO`: Meaningful milestones not already covered by Kedro.
- `WARNING`: Unexpected condition or expected data deviation where execution continues.
- `ERROR`: Operation failed or data contract violated; include exception context.
- `CRITICAL`: Fatal condition preventing the pipeline from continuing.

## String Formatting

- Use lazy `%` formatting in `logger.*()` calls (`logger.warning("Missing %d rows in %s", count, name)`) — never f-strings.
- Use f-strings in `raise` statements and general strings (Ruff `UP031`).
- Format timestamps as `YYYY-MM-DD` strings before logging.
- Cap logged collections to 5–10 items with an `(and N more)` suffix.

Full guide with examples: [docs/developer_guides/logging.md](../../docs/developer_guides/logging.md).
