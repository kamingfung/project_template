# project_template

Modern data science and analytics project template built on **Kedro**, **MLflow**, **uv**, **just**, **ruff**, **ty**, and **pytest**, with unified **Kiro** and **Claude Code** steering.

## Stack

- **Environment & packaging:** `uv` (Python 3.14)
- **Task runner:** `just` (`Justfile`)
- **Pipeline framework:** `kedro` + `kedro-datasets` + `kedro-viz`
- **Experiment tracking:** `mlflow` + `kedro-mlflow` (local SQLite backend by default)
- **Code quality:** `ruff` (lint + format), `ty` (type check), `pre-commit`
- **Testing:** `pytest` with `pytest-cov`, `pytest-xdist`, `pytest-sugar`, and `pytest-mock`

## Quickstart

1. Install prerequisites (`uv` and `just`):

   ```bash
   brew install uv just
   ```

2. Initialize the Python environment and pre-commit hooks:

   ```bash
   just init
   ```

3. Run the example Kedro pipeline (processes sample CSVs in `data/01_raw/` and logs metrics to `mlflow.db`):

   ```bash
   just run
   ```

4. Inspect the pipeline or MLflow runs:

   ```bash
   just viz           # launch Kedro-Viz
   just mlflow-local  # launch MLflow UI on a free port
   ```

## Common Commands

| Command | Purpose |
| --- | --- |
| `just init` | Install Python 3.14, sync `uv` dependencies, and install pre-commit hooks |
| `just run` | Run the default Kedro pipeline |
| `just test` | Run unit tests in parallel without coverage |
| `just test_ci` | Run unit tests with coverage report (90% minimum on node modules) |
| `just lint` | Auto-fix lint issues and format code with `ruff` |
| `just lint_check` | Verify `ruff` lint/format and stripped notebook outputs |
| `just typecheck` | Run static type checking with `ty` |
| `just viz` | Launch Kedro-Viz |
| `just mlflow-local` | Launch MLflow UI against `sqlite:///mlflow.db` |

## Folder Structure

```text
├── .claude/             # Claude Code rules, skills, hooks, and safety settings
├── .kiro/steering/      # Single source of truth for agent steering rules
├── conf/
│   ├── base/            # Catalog, parameters, and globals
│   ├── local/           # Local overrides (e.g., mlflow.yml)
│   └── logging.yml      # Kedro logging configuration
├── data/                # Kedro data layers (01_raw -> 08_reporting)
├── docs/                # Design specs, plans, and project docs
├── notebooks/           # Exploratory notebooks (outputs stripped by pre-commit)
├── src/project_template/
│   ├── pipelines/       # Modular Kedro pipelines (data_processing, reporting)
│   ├── pipeline_registry.py
│   └── settings.py
├── tests/               # Unit tests mirroring src/project_template/
├── CLAUDE.md            # Imports always-on steering from .kiro/steering/
├── Justfile             # Task runner recipes
└── pyproject.toml       # Project metadata, dependencies, and tool config
```

## Steering & Agent Rules

Coding, testing, and documentation rules live in `.kiro/steering/` as the single source of truth:

- Always-on rules are imported by `CLAUDE.md`.
- File-scoped rules are mapped in `.claude/rules/` via `paths:` front-matter.
- On-demand workflows live in `.claude/skills/`.
