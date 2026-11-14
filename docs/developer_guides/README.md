# Developer Guidelines

Engineering standards for Python code, Kedro pipelines, parallelism, tests, logging, visualization, and documentation in this repository.

| Guide | Audience & Scope | Rule File |
| --- | --- | --- |
| [code_style.md](code_style.md) | Pure functions, readability, top-down order, fail-loud error handling, pandas/time-series rules | [code-style-standards.md](../../.claude/rules/code-style-standards.md) |
| [logging.md](logging.md) | Logger usage, 3 a.m. actionability test, levels, exception logging, lazy `%` formatting | [logging-standards.md](../../.claude/rules/logging-standards.md) |
| [unit_test.md](unit_test.md) | Test structure, data-driven fixtures, Pandera vs. unit tests, mocking rules, smell signals | [unit-test-standards.md](../../.claude/rules/unit-test-standards.md) |
| [pipeline.md](pipeline.md) | Kedro `01_raw`–`08_reporting` layers, package layout, `create_pipeline()`, tags, CLI runs | — |
| [parameters.md](parameters.md) | Parameter nesting, narrow slicing, strict `params["key"]` access, YAML quoting | — |
| [schema_validation.md](schema_validation.md) | Pandera boundaries, tuple-coercion bug, `int64` zero-division safety, Parquet, schema-derived columns | — |
| [parallelism.md](parallelism.md) | `ThreadRunner` vs. OpenMP segfaults, `OMP_NUM_THREADS`, `fit_n_jobs` vs. estimator `n_jobs=1` | — |
| [visualization.md](visualization.md) | Okabe–Ito colorblind-safe palette, paired encodings, Mermaid vs. Graphviz | [visualization.md](../../.claude/rules/visualization.md) |
| [writing_standards.md](writing_standards.md) | Self-contained docs, terminology, ASD-STE100 prose, front/body/back matter, figures/tables/math | [writing-standards.md](../../.claude/rules/writing-standards.md) |
