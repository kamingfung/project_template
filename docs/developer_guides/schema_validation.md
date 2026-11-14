# Schema Validation

Rules for Pandera schema definitions, validation boundaries, and dtype safety. For testing strategy around schemas, see [unit_test.md](unit_test.md).

## 1. Pandera Decorator & `validate()` Usage

Use explicit `Schema.validate(df, lazy=True)` (or `.pipe(SCHEMA.validate)`) or `@pa.check_types(lazy=True)` with `PaDataFrame[Schema]` hints at node boundaries. Do **not** use bare schema classes as return type hints with `@pa.check_types` — Pandera silently skips validation.

| Pattern | Validates? | Coercion propagates? |
| --- | --- | --- |
| `@pa.check_types` + `PaDataFrame[Schema]` | Yes | Yes |
| `@pa.check_types` + bare `Schema` | No (silent skip) | No |
| `@pa.check_types` + `tuple[PaDataFrame[A], ...]` | Yes | No (`pandera <= 0.30.x` bug) |
| Explicit `Schema.validate(df, lazy=True)` | Yes | Yes |

- **Tuple returns (`pandera <= 0.30.x`):** `@pa.check_types` validates tuple elements internally but discards the coerced copies. When returning multiple DataFrames, call `Schema.validate(df, lazy=True)` explicitly on each output and annotate the return as `tuple[pd.DataFrame, pd.DataFrame]`.
- **Node input validation:** validate inputs on nodes that perform division, rounding, or clipping on columns whose dtypes could drift across storage formats.

## 2. Division by Zero & `NaN` Dtype Propagation

When dividing columns where the denominator can be zero:

- `.replace(0, np.nan)` on an `int64` column produces an `object`-dtype Series in pandas, causing downstream `TypeError` on `.round()`, `.clip()`, or arithmetic.
- CSV loads numeric columns with nulls as `float64`, whereas Parquet preserves `int64`, hiding this bug until Parquet is used.

```python
# Bad — .replace() on int64 can produce object dtype
ratio = numerator / denominator.replace(0, np.nan)

# Good — .where() returns float64 with NaN where condition is False
ratio = numerator / denominator.where(denominator != 0)
```

## 3. Save Intermediate Datasets as Parquet

Use `pandas.ParquetDataset` (not `CSVDataset`) for intermediate catalog entries (`02_intermediate` through `05_model_input`) so column dtypes (`int64`, `bool`, `datetime64`) are preserved without CSV serialization loss:

```yaml
model_input_table:
  type: pandas.ParquetDataset
  filepath: data/03_primary/model_input_table.parquet
```

## 4. Schema-Derived Column Selection

Derive output column lists directly from the Pandera schema instead of maintaining a parallel `cols_to_keep` list in YAML parameters:

```python
# Good — single source of truth from the schema
output_columns = list(MODEL_INPUT_SCHEMA.columns)
return cleaned_df[output_columns]
```

Keep column lists in YAML only when:

1. Selecting a proper subset of a schema's columns for a specific view.
2. Exporting to an external consumer format that has no internal schema.
3. Filtering which columns to request from an upstream API or query before ingestion.

## 5. Shared Validation Constants

Store reusable validation bounds and regex patterns in a shared constants module (`Final`) rather than scattering magic numbers across schemas, and prefer declarative checks (`pa.Check.ge(...)`, `pa.Check.str_matches(...)`) over custom validation functions when the column is a single type.
