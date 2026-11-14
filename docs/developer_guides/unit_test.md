# Unit Test Guide

Actionable standards for writing fast, deterministic unit tests in this repository.

## Test File Structure

- Name test functions `test_[function_name]_[scenario]` and annotate return types with `-> None`.
- Add concise docstrings to fixtures and test functions stating what behavior and edge case are under test.
- Structure every test with `# Arrange`, `# Act`, and `# Assert` comments.
- Pass keyword arguments when calling the function under test.
- Keep fixtures in the test file alongside the tests that use them.

```python
def test_calculate_ratio_zero_denominator(sample_df: pd.DataFrame) -> None:
    """Test calculate_ratio raises ValueError when denominator contains zero."""
    # Arrange
    data = sample_df.copy()
    data.loc[0, "denominator"] = 0

    # Act & Assert
    with pytest.raises(ValueError, match="denominator"):
        calculate_ratio(
            df=data, numerator_col="numerator", denominator_col="denominator"
        )
```

## Fixtures & Edge Cases

- **Cover all boundaries:** empty inputs, single-row inputs, `NaN` values, and boundary conditions (one test per new branch).
- **Schema-compliant empty DataFrames:** define explicit column dtypes with `pd.Series([], dtype=...)`.
- **Derive expected values:** run the function on the fixture and inspect the output; never guess expected values.
- **Protect regression tests:** never edit an existing test's expected values, delete it, or mark it `skip`/`xfail` unless the old expectation was demonstrably wrong (document why in the commit message).

## Logic vs. Schema & Mocking

Unit tests verify computation logic; Pandera schemas verify data contracts. Both are required and neither replaces the other.

| Test type | Fixture | Schema involved |
| --- | --- | --- |
| Logic unit test | Minimal — only relevant columns | No |
| Schema validation test | Factory with defaults | Yes |
| Integration / pipeline test | Full schema-valid fixture | Yes |

### Mocking Rules

- **Never mock a DataFrame.** It replaces real computation with a fake.
- **Never mock a Pandera schema check** (except when specifically testing schema-error handling).
- **Do mock real I/O boundaries:** database reads, file I/O, MLflow calls, and HTTP requests.
- **Reset singletons:** add an `autouse` fixture resetting `ClassName._instance = None` so tests remain order-independent.

## Running Tests

```zsh
uv run pytest -n auto
```
