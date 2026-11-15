# project_template

Modern data science and analytics project template built on **Kedro**, **MLflow**, **uv**, **just**, **ruff**, **ty**, and **pytest**, with **Claude Code** rules and skills.

## Stack

- **Environment & packaging:** `uv` (Python 3.14)
- **Task runner:** `just` (`Justfile`)
- **Pipeline framework:** `kedro` + `kedro-datasets` + `kedro-viz`
- **Data contracts & compute:** `pandera` (schema validation), `ray` (multiprocessing)
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
| `just plugins` | Symlink the `data-scientist` plugin into `~/.gemini/config/plugins/` |
| `just run` | Run the default Kedro pipeline |
| `just test` | Run unit tests in parallel without coverage |
| `just test_ci` | Run unit tests with coverage report (90% minimum on node modules) |
| `just lint` | Auto-fix lint issues and format code with `ruff` |
| `just lint_check` | Verify `ruff` lint/format and stripped notebook outputs |
| `just typecheck` | Run static type checking with `ty` |
| `just audit` | Audit locked dependencies with `pip-audit` |
| `just viz` | Launch Kedro-Viz |
| `just mlflow-local` | Launch MLflow UI against `sqlite:///mlflow.db` |

## Updating Packages

Use `uv` to add, upgrade, and re-lock dependencies in `pyproject.toml` and `uv.lock`:

```bash
# Add a runtime or dev dependency
uv add <package>
uv add --dev <package>

# Upgrade a single package and sync the environment
uv lock --upgrade-package <package>
uv sync --all-groups

# Upgrade all packages within pyproject.toml constraints
uv lock --upgrade
uv sync --all-groups

# Update pre-commit hook versions
uv run pre-commit autoupdate
```

After updating packages, verify the lockfile and quality gates:

```bash
just audit && just lint_check && just typecheck && just test_ci
```

## Folder Structure

```text
├── .claude/             # Claude Code project safety settings
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
├── CLAUDE.md            # Project agent notes
├── Justfile             # Task runner recipes
└── pyproject.toml       # Project metadata, dependencies, and tool config
```

## Agent Rules & Skills

Engineering standards, MBB problem solving/slide creation, and HK sharp execution skills are packaged in the `data-scientist` agent plugin. Run `just plugins` to link it from the sibling repo into `~/.gemini/config/plugins/`. Project-specific safety settings remain in `.claude/settings.json`.
