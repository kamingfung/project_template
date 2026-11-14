# Unit Test Guide

Actionable standards for writing fast, deterministic unit tests in this repository.

## 1. Test File Structure & Naming

- Add a module docstring at the top of each test file summarizing `Coverage:`, `Impacts:`, and `Strategy:`.
- Require a docstring on every `@pytest.fixture`.
- Every test function requires:
  - Naming: `test_[function_name]_[scenario]`
  - Return annotation: `-> None`
  - Docstring with `Tests:`, `Expected:`, and `Edges:` fields (or a concise 1-line summary for simple tests)
  - `# Arrange`, `# Act`, and `# Assert` comments
  - Keyword arguments only when calling the function under test
- Keep fixtures in the test file alongside the tests that use them; readability outweighs DRY in tests.

```python
def test_create_model_input_table_duplicate_company_raises(
    sample_companies: pd.DataFrame,
    sample_shuttles: pd.DataFrame,
) -> None:
    """
    Test create_model_input_table raises MergeError on duplicate company IDs.

    Tests: Many-to-one merge validation on company_id -> id
    Expected: pandas.errors.MergeError raised
    Edges: Duplicate primary key in right table
    """
    # Arrange
    companies_clean = preprocess_companies(companies=sample_companies)
    duplicated = pd.concat(
        [companies_clean, companies_clean.iloc[[0]]], ignore_index=True
    )
    shuttles_clean = preprocess_shuttles(shuttles=sample_shuttles)

    # Act & Assert
    with pytest.raises(pd.errors.MergeError):
        create_model_input_table(shuttles=shuttles_clean, companies=duplicated)
```

## 2. Production-Data-Driven Fixtures & Edge Cases

Synthetic fixtures invented from guesswork miss real data quirks. When building fixtures for pipeline nodes, inspect real catalog data in a scratch script or notebook (`KedroSession.create()`), profile it, and extract a 10–50 row representative subset:

| Dimension to profile | What to include in fixture |
| --- | --- |
| Shape & dtypes | Exact column names and dtypes (`int64`, `float64`, `string`, `bool`) |
| Null patterns | Actual `NaN` combinations that appear in raw inputs |
| Extremes & boundaries | Min/max numeric values, zero denominators, ISO week 53 / year boundaries |
| Groups | `>=3` distinct entity groups so `groupby` leakage is caught |

- Mark real-data fixtures with `# Derived from catalog data YYYY-MM-DD`.
- Build schema-compliant empty DataFrames using explicit `pd.Series([], dtype=...)` columns.

### Standard Test Ordering Per Function

1. `test_{func}_realistic_happy_path` — representative input -> verify shape, columns, dtypes.
2. `test_{func}_nan_handling` — realistic `NaN` rows -> verify graceful handling (no silent corruption).
3. `test_{func}_boundary_values` — empty input, single-row input, zero/extreme values.
4. `test_{func}_output_correctness` — run function on fixture, inspect output, lock exact expected values.

### Deriving & Protecting Expected Values

- **New tests:** run the function on the fixture first, inspect the result, then write the assertion. Never guess expected numbers.
- **Existing tests:** never edit an existing test's expected values, delete it, or mark it `skip`/`xfail` unless the old expectation was demonstrably wrong (explain why in the commit message).
- **Bug-to-test loop:** when a bug is reported, first write a failing test that reproduces it, then fix the code and verify the test passes.

## 3. Assertion Best Practices

- **Assert values, not just shape:** check specific output values (`pytest.approx` or `pd.testing.assert_frame_equal(..., check_exact=False)`) alongside row counts.
- **Assert dtypes explicitly:** `assert result["shuttle_id"].dtype == "int64"`, `assert pd.api.types.is_datetime64_any_dtype(result["date"])`.
- **Descriptive failure messages:** include context in loop assertions (`assert col in result.columns, f"Missing column: {col}"`).

## 4. Pandera vs. Unit Tests & Mocking Rules

Unit tests verify computation logic; Pandera schemas verify data contracts ([schema_validation.md](schema_validation.md)). Neither substitutes for the other.

| Test type | Fixture | Schema involved? | What it catches |
| --- | --- | --- | --- |
| Logic unit test | Minimal — only relevant columns | No | Wrong aggregation, join, or filter math |
| Schema validation test | Factory with defaults | Yes | Wrong dtypes, nulls in non-nullable cols, out-of-range values |
| Integration / pipeline test | Full schema-valid fixture | Yes | End-to-end wiring and missing columns after transforms |

### Mocking Rules

- **Never mock a DataFrame.**
- **Never mock a Pandera schema check** (except when testing a schema-error handler itself).
- **Do mock real I/O boundaries:** database queries, external file I/O, MLflow calls (`monkeypatch`), and HTTP requests.
- **Reset singletons:** use an `autouse` fixture to reset any singleton state so tests pass in any order under `pytest -n auto`.

### Smell Signals

| Smell | Fix |
| --- | --- |
| Fixture has 20 unused columns | Test pure logic helper with only the columns it reads |
| Schema check makes unit test setup painful | Push schema validation to the node boundary; test `_logic()` separately |
| Function requires 5 mocks to test | Split pure decision logic from I/O side effects ([code_style.md](code_style.md)) |

## 5. Running Tests

```zsh
just test        # Fast parallel run: uv run pytest -n auto --no-cov
just test_ci     # CI run with 90% coverage gate: uv run pytest -n auto --cov=src/project_template --cov-report=term-missing
```
