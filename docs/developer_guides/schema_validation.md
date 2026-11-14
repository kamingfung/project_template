# Schema Validation

Rules for Pandera schema definitions, validation boundaries, and dtype safety. For testing strategy around schemas, see [unit_test.md](unit_test.md).

## Schema Usage

Use explicit `Schema.validate(df, lazy=True)` (or `.pipe(SCHEMA.validate)`) or `@pa.check_types(lazy=True)` with `PaDataFrame[Schema]` hints at node boundaries. Do **not** use bare schema classes as return type hints with `@pa.check_types` — Pandera silently skips validation.

| Pattern | Validates? | Coercion propagates? |
| --- | --- | --- |
| `@pa.check_types` + `PaDataFrame[Schema]` | Yes | Yes |
| `@pa.check_types` + bare `Schema` | No (silent skip) | No |
| `@pa.check_types` + `tuple[PaDataFrame[A], ...]` | Yes | No (`pandera <= 0.30.x` bug) |
| Explicit `Schema.validate(df, lazy=True)` | Yes | Yes |

When a node returns multiple DataFrames, always use explicit `Schema.validate(df, lazy=True)` on each output and type the return as `tuple[pd.DataFrame, pd.DataFrame]`.

## Division by Zero and `NaN` Dtype Propagation

When dividing columns where the denominator can be zero:

- `.replace(0, np.nan)` on an `int64` column produces an `object`-dtype Series (because `int64` cannot hold `NaN`), which can cause `TypeError` downstream.
- CSV files load integers as `float64` when nulls exist, while Parquet preserves `int64`, hiding this bug until Parquet is used.

```python
# Bad — .replace() on int64 produces object dtype
ratio = numerator / denominator.replace(0, np.nan)

# Good — .where() returns float64 with NaN where condition is False
ratio = numerator / denominator.where(denominator != 0)
```

## Save Intermediate Files as Parquet Locally

Prefer Parquet over CSV for intermediate catalog datasets (`02_intermediate` through `05_model_input`) so column dtypes (`int64`, `bool`, `datetime64`) are preserved between nodes without silent type coercion.
