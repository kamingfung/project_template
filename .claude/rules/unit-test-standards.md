---
paths:
  - "tests/**/*.py"
---

# Unit Test Standards

## Structure & Naming

- Name test functions `test_[function_name]_[scenario]` and annotate return types with `-> None`.
- Structure every test with `# Arrange`, `# Act`, and `# Assert` sections.
- Pass keyword arguments when calling the function under test.
- Add concise docstrings to fixtures and test functions explaining what behavior and edge case are under test.
- Keep fixtures in the test file alongside the tests that use them; readability outweighs DRY in tests.

## Fixtures & Edge Cases

- Cover empty inputs, single-row inputs, `NaN` values, and boundary cases (one test per new branch).
- Build schema-compliant empty DataFrames with explicit column dtypes (`pd.Series([], dtype=...)`).
- Derive expected values for new tests by running and inspecting the actual output; never guess expected values.
- Never edit an existing test's expected values, delete it, or mark it `skip`/`xfail` unless the old expectation was demonstrably wrong (state why in the commit message).

## Logic vs. Schema & Mocking

- Test pure logic with minimal DataFrames containing only the relevant columns; test Pandera schemas at I/O boundaries.
- Never mock a DataFrame or a Pandera schema check (except when testing schema-error handling itself).
- Mock only real I/O boundaries (database reads, file I/O, MLflow calls, HTTP requests).
- Reset any module-level singletons in an `autouse` fixture so tests stay order-independent.

## Execution

- Run the suite via `uv run pytest -n auto` (with `pytest-cov` / `pytest-xdist` configured in `pyproject.toml`).

Full guide with examples: [docs/developer_guides/unit_test.md](../../docs/developer_guides/unit_test.md).
