---
inclusion: manual
---

# Code Review Checklist

Manual checklist for PR review. Reference with `#code-review-checklist`.
The detailed rules behind each item live in the other steering files
(`code-style-standards.md`, `unit-test-standards.md`, `logging-standards.md`).

## Reviewer conduct

Applies to PRs and to Confluence experiment reports. Adapted from "The good referee", Nat. Methods 15, 91 (2018), doi:10.1038/nmeth.4603.

- [ ] Access blockers (unpushed branch, missing data or permissions) raised first, and the parts you cannot judge named up front
- [ ] Value: the work addresses a real problem and places itself against prior work (earlier tickets, changelogs, existing code)
- [ ] Soundness: baseline or control, statistics, benchmark against the current approach, conclusions backed by the data, limitations stated
- [ ] Reproducible from the PR or page alone: pushed branch and commit, data pull date, MLflow run ids, the command to rerun (`docs/dev_guidelines/writing_standards.md` Body and Back Matter)
- [ ] Code, config and data the work describes were read; the author's run evidence (the backtest item under Behavior) was rerun when missing or when a result is surprising, and otherwise a finding from reading code only says so
- [ ] Design and logic findings come before style and edge cases
- [ ] Essentials only, not a wish list; findings numbered and labeled must-fix, should-fix or nit
- [ ] A repeated issue is flagged once, inline at its first instance, asking for every instance to be fixed
- [ ] Grammar raised only when it hides what was done; the tone critiques the work, never the author's competence

## Behavior

- [ ] Assumptions stated explicitly
- [ ] Simplest viable solution chosen
- [ ] No speculative features or unrequested abstractions
- [ ] Changes are surgical — only touch what is necessary
- [ ] Success criteria defined and verified
- [ ] Model-affecting change (features, inputs, params, pipeline bug fix) has a before/after backtest on `main` vs branch, with metrics and run ids in the changelog. Before opening the PR, publish both runs as in `docs/dev_guidelines/running-pipelines.md` "Publishing a run to dev" (manual path: `notebooks/log_in_season_accuracy_metrics.ipynb`), and cite both dev run ids in the PR description and the changelog
- [ ] Deletions leave no orphans: param keys, catalog entries, test fixtures, `utils/` helpers and doc links with no remaining reader are removed

## Code style

- [ ] Functions around 30 body lines or fewer (soft limit; longer ones state a reason)
- [ ] One pandas operation per line
- [ ] Pure functions, no in-place mutation
- [ ] Descriptive names, no mental mapping
- [ ] ≤5 arguments (or grouped into a dict / namedtuple)
- [ ] No flag parameters
- [ ] Helper functions placed after the node function that calls them
- [ ] Type hints on every signature, and an inline hint on every new local variable
- [ ] Keyword arguments in calls that pass more than two arguments
- [ ] A value read by one function is local to it; module level only once a second function reads it
- [ ] Single return statement at end

## Documentation

- [ ] Google-style docstrings on all functions
- [ ] `Args:`, `Returns:` filled in
- [ ] DataFrame returns list output columns: `|col1|col2|`
- [ ] Docstring explains _why_, code shows _what_
- [ ] Model and dataset docs updated when behavior, params or datasets change, including how a config value is set and how to update it
- [ ] New terms in docstrings, comments and the PR description reuse existing ones or are defined at first use (`docs/dev_guidelines/writing_standards.md` Terminology)
- [ ] Inline comments are concise — no multi-line explanations; detailed context goes to `docs/` (if stable/reproducible) or `changelogs/epics/` (if branch-specific or may change)
- [ ] Experiment results, backtest tables, and arm comparisons are in `changelogs/epics/`, not in `docs/model_documentation/` or YAML — including dated or "illustrative" snapshots; the doc states the rule and links to the changelog
- [ ] No ticket ids (`<TICKET-ID>`) or dates in code comments, docstrings, tests or doc headings
- [ ] Comments, docstrings, docs and the PR description match the code: every named reader or behavior was checked by reading the code or `git grep`
- [ ] Each ticket has its own `changelogs/epics/<TICKET-ID>-*.md` in Brief → Progress → Decisions order, with no placeholder links

## Data integrity

- [ ] Pandera schemas applied at pipeline node boundaries
- [ ] `@pa.check_types` uses `PaDataFrame[Schema]` return hint (not bare Schema)
- [ ] `pd.merge` has explicit `on`, `how`, `validate`
- [ ] Empty or off-season input returns an empty frame with the output schema's columns
- [ ] ISO week paired with ISO year; fills, shifts and "latest" picks run within entity groups
- [ ] Shared datasets read no downstream params, and downstream pipelines don't write to them

## Testing

- [ ] Tests follow AAA pattern (Arrange / Act / Assert)
- [ ] Keyword arguments when calling the function under test
- [ ] Required edge cases: empty DataFrame, single row, NaN, boundary values
- [ ] Realistic domain data (varieties: POP, BEAUTY, BIANCA; farms: A9, C5, C6, LN)
- [ ] No mocking of DataFrames or Pandera schema checks
- [ ] `pd.testing.assert_frame_equal` for DataFrame comparison
- [ ] No existing test edited to match new output, deleted, or marked `xfail`/`skip` without the reason in the commit message
- [ ] Each new branch (fallback, empty input, boundary) has its own test

## Error handling and logging

- [ ] Specific `except` clauses, no bare `except:`
- [ ] Error messages include context (dataset name, inputs, offending rows)
- [ ] No silent fallbacks (`fillna` substitute, `errors="ignore"`, `dropna`, last-write-wins); a deliberate one logs how many rows it touched
- [ ] Uses `kedro_logger` from `global_utils`
- [ ] WARNING/ERROR logs include farm, variety, season where applicable
- [ ] No `f-strings` in log calls — use lazy `%` formatting
- [ ] No secrets or PII in logs

## YAML parameters

- [ ] No quotes around keys
- [ ] Quotes around string values
- [ ] Related parameters grouped under a common parent
- [ ] Node receives parent dict, not each leaf separately

## Best practices

- [ ] Sort before groupby for numeric aggregations
- [ ] No mutable default arguments (use `None` and bind inside)
- [ ] Shared constants in `utils/constants.py`, annotated `Final`
- [ ] Pre-commit passes (`pre-commit run --all-files`)

## Pre-merge

- [ ] `ruff check --fix` clean
- [ ] `ruff format` clean
- [ ] `uv run pytest` passes
- [ ] No unrelated refactors mixed into the PR
- [ ] Pushes batched per finished unit of work, and review replies posted as one round with a single summary comment
