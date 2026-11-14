# Modern Kedro Project Template Design

**Date:** 2026-11-13
**Status:** Draft for review

## Summary

Modernize `project_template` into a general-purpose Kedro 1.x data science and analytics template modeled on `/Users/fkm/GitHub/pe-analytics-pipelines` and `kedro-starters/spaceflights-pandas`. The template standardizes on `uv`, `just`, `ruff`, `ty`, `pytest`, `kedro`, and `mlflow`, and includes a unified Kiro + Claude steering system.

## Goals and Scope

### In Scope

1. **Toolchain modernization (`pyproject.toml`, `Justfile`, `.pre-commit-config.yaml`, `.gitignore`)**
   - Python: latest version supported by the Kedro + MLflow stack (target `>=3.14,<3.15`, verified via `uv sync`; upgradeable to `3.15` if all core dependencies resolve).
   - Package & environment management: `uv` exclusively (remove `environment.yml`, `requirements.txt`, and `src/utils/config.py`).
   - Formatting & linting: `ruff` (remove `black`).
   - Static type checking: `ty`.
   - Testing: `pytest` with `pytest-cov`, `pytest-xdist`, `pytest-sugar`, and `pytest-mock` (`fail_under = 90` on node/logic modules).
   - Task runner: `Justfile` with `init`, `lint`, `lint_check`, `typecheck`, `test`, `test_ci`, `run`, `viz`, `mlflow-local`, `check_merge_conflicts`, and `check_secrets`.
   - Pre-commit: `pre-commit-hooks`, `ruff-pre-commit`, `nbstripout`, `uv-pre-commit`, `yamllint`, `taplo-format`, and `gitleaks`.
2. **Kedro 1.x + MLflow project structure (`conf/`, `data/`, `src/project_template/`, `tests/`, `notebooks/`)**
   - Standard Kedro layout: `__init__.py`, `__main__.py`, `pipeline_registry.py`, `settings.py`, `hooks.py`.
   - Lightweight synthetic two-stage example pipeline (`data_processing` -> `reporting`, inspired by `spaceflights-pandas`) reading local CSV/Parquet in `data/01_raw/`, producing intermediate/reporting artifacts, and logging metrics/parameters to local MLflow (`sqlite:///mlflow.db`).
   - `conf/base/` (`catalog.yml`, `parameters.yml`, `globals.yml`), `conf/local/` (`mlflow.yml`), and `conf/logging.yml`.
   - Unit tests in `tests/` covering node logic and pipeline assembly using Arrange / Act / Assert and keyword arguments.
3. **Kiro + Claude steering and safety setup (`CLAUDE.md`, `.kiro/`, `.claude/`)**
   - `.kiro/steering/` as the single source of truth for general-purpose engineering rules: `agent-defaults.md`, `coding-guidelines.md`, `code-style-standards.md`, `logging-standards.md`, `unit-test-standards.md`, `writing-standards.md`, `docs-figures-and-maths.md`, `experiment-figures.md`, `visualization.md`, `progress-tracking.md`, `session-handoff.md`, `steering-file-standards.md`, `code-review-checklist.md`, and `worktrees.md`.
   - `.claude/rules/` path-scoped wrappers, `.claude/skills/` (`code-review-checklist`, `code-reviewer`, `experiment-figures`, `worktrees`), `.claude/hooks/kiro_hooks.py`, and `.claude/settings.json` (git `main` force-push protection and hook wiring, with AWS/Bitbucket rules removed).
   - `CLAUDE.md` importing always-on `.kiro/steering/` files and documenting the sync rule.
4. **Documentation (`README.md`)**
   - Updated setup, `just` commands, Kedro + MLflow workflow, and steering overview.

### Out of Scope

- Cloud/production infrastructure from `pe-analytics-pipelines`: AWS Batch, SageMaker MLflow, S3 buckets, Airflow DAG templates (`templates/`), Bitbucket Pipelines, Docker/Aikido scanning, and `bitbucket-api` steering/skills.
- Domain-specific geospatial packages (`cartopy`, `geopandas`, `rasterio`, `rioxarray`, `xarray-spatial`, `numba`, `dask`) — users add domain dependencies per project.
- Repo-specific `blueberry_forecast_kedro` references.

## Architecture and File Layout

```text
project_template/
├── .claude/
│   ├── hooks/kiro_hooks.py
│   ├── rules/*.md
│   ├── skills/{code-review-checklist,code-reviewer,experiment-figures,worktrees}/
│   └── settings.json
├── .kiro/
│   └── steering/*.md
├── conf/
│   ├── base/
│   │   ├── catalog.yml
│   │   ├── globals.yml
│   │   └── parameters.yml
│   ├── local/
│   │   └── mlflow.yml
│   └── logging.yml
├── data/
│   └── 01_raw/ ... 08_reporting/ (with tiny synthetic sample CSVs in 01_raw/)
├── docs/
├── notebooks/
├── src/
│   └── project_template/
│       ├── __init__.py
│       ├── __main__.py
│       ├── hooks.py
│       ├── pipeline_registry.py
│       ├── settings.py
│       └── pipelines/
│           ├── data_processing/
│           │   ├── __init__.py
│           │   ├── nodes.py
│           │   └── pipeline.py
│           └── reporting/
│               ├── __init__.py
│               ├── nodes.py
│               └── pipeline.py
├── tests/
│   ├── conftest.py
│   └── pipelines/
│       ├── data_processing/test_nodes.py
│       └── reporting/test_nodes.py
├── .gitignore
├── .pre-commit-config.yaml
├── .yamllint.yml
├── CLAUDE.md
├── Justfile
├── pyproject.toml
└── README.md
```

## Key Design Decisions

1. **Single source of truth for steering:** `.kiro/steering/` holds all rule content. `CLAUDE.md` imports always-on rules via `@.kiro/steering/...`, and `.claude/rules/` uses `paths:` front-matter to load matching `.kiro/steering/` files only when relevant files are touched.
2. **Local-first MLflow:** `conf/local/mlflow.yml` configures `sqlite:///mlflow.db` (gitignored alongside `mlruns/` and `mlartifacts/`), and `just mlflow-local` launches the UI on a free port.
3. **Pure, testable Kedro nodes:** Example nodes are pure functions with explicit type annotations, keyword-friendly signatures, and unit tests in `tests/pipelines/` that pass without external services.
4. **Legacy cleanup:** Remove `environment.yml`, `requirements.txt`, `src/utils/config.py`, and untracked scratch files (`passwords.txt`, `quickstart_tutorial.ipynb`) so the template starts clean.

## Verification Criteria

After implementation:
- `uv sync --all-groups` succeeds and generates a clean `uv.lock`.
- `just lint_check` passes (`ruff check`, `ruff format --check`).
- `just typecheck` passes (`uv run ty check`).
- `just test_ci` passes with >= 90% coverage.
- `just run` (`uv run kedro run`) executes the example pipeline end-to-end and logs a run to `mlflow.db`.
