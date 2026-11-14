# Modern Kedro Project Template Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Modernize `project_template` into a general-purpose Kedro 1.x + MLflow + `uv` + `just` + `ruff` + `ty` + `pytest` template with unified Kiro and Claude steering.

**Architecture:** Clean-room Kedro 1.x package (`src/project_template/`) with a lightweight two-stage synthetic pipeline (`data_processing` -> `reporting`) backed by local CSV/Parquet datasets and local SQLite MLflow tracking. `.kiro/steering/` serves as the single source of truth for agent rules, imported by `CLAUDE.md` and path-scoped `.claude/rules/`.

**Tech Stack:** Python 3.14 (`>=3.14,<3.15`), `uv`, `just`, `kedro`, `kedro-datasets`, `kedro-mlflow`, `mlflow`, `kedro-viz`, `pandas`, `ruff`, `ty`, `pytest`, `pytest-cov`, `pytest-xdist`, `pytest-sugar`.

## Global Constraints

- Package name: `project_template` (`src/project_template/`).
- No AWS, Airflow, SageMaker, Bitbucket, or `blueberry_forecast_kedro` references.
- Use `uv` exclusively for Python environments and `ruff` + `ty` + `pytest` for quality gates.
- Coverage floor: `fail_under = 90` on node/logic modules.
- No AI `Co-Authored-By:` trailers in commit messages.

---

### Task 1: Modernize Toolchain & Repository Config

**Files:**
- Modify: `pyproject.toml`, `.gitignore`, `.pre-commit-config.yaml`
- Create: `Justfile`, `.yamllint.yml`
- Remove: `environment.yml`, `requirements.txt`, `src/utils/config.py`, `passwords.txt`, `quickstart_tutorial.ipynb`

- [ ] **Step 1: Update `.gitignore`**
  Merge Kedro, MLflow (`mlflow.db`, `mlruns/`, `mlartifacts/`), `uv`, `pytest`, `ruff`, `ty`, `.venv/`, and local scratch ignores from `/Users/fkm/GitHub/pe-analytics-pipelines/.gitignore`, keeping `!data/01_raw/*.csv` if sample raw CSVs are tracked (or track sample CSVs explicitly with `git add -f`).

- [ ] **Step 2: Write `pyproject.toml`, `.pre-commit-config.yaml`, `.yamllint.yml`, and `Justfile`**
  Configure `requires-python = ">=3.14,<3.15"`, core deps (`kedro[jupyter]`, `kedro-datasets[pandas]`, `kedro-mlflow`, `mlflow`, `pandas`, `pyarrow`), `dev` group (`pytest`, `pytest-cov`, `pytest-xdist`, `pytest-sugar`, `pytest-mock`, `ruff`, `ty`, `pre-commit`, `kedro-viz`, `jupyter`), and `[tool.kedro]`, `[tool.pytest.ini_options]`, `[tool.coverage.*]`, `[tool.ruff]`.
  Configure `Justfile` with `init`, `lint`, `lint_check`, `typecheck`, `test`, `test_ci`, `run`, `viz`, `mlflow-local`, `check_merge_conflicts`, and `check_secrets`.

- [ ] **Step 3: Remove legacy files**
  Delete `environment.yml`, `requirements.txt`, `src/utils/config.py`, `passwords.txt`, `quickstart_tutorial.ipynb`.

- [ ] **Step 4: Sync environment**
  Run `uv sync --all-groups` and verify `uv.lock` updates cleanly.

- [ ] **Step 5: Commit**
  Commit toolchain and config updates.

---

### Task 2: Scaffold Kedro 1.x + MLflow Config & Core Package

**Files:**
- Create: `conf/base/catalog.yml`, `conf/base/parameters.yml`, `conf/base/globals.yml`, `conf/local/mlflow.yml`, `conf/logging.yml`
- Create: `data/01_raw/companies.csv`, `data/01_raw/shuttles.csv`
- Create: `src/project_template/__init__.py`, `src/project_template/__main__.py`, `src/project_template/settings.py`, `src/project_template/hooks.py`, `src/project_template/pipeline_registry.py`

- [ ] **Step 1: Create `conf/` files and tiny synthetic `data/01_raw/` CSVs**
  Create minimal synthetic `companies.csv` and `shuttles.csv` (~5 rows each) and wire `conf/base/catalog.yml`, `conf/base/parameters.yml`, `conf/base/globals.yml`, `conf/local/mlflow.yml` (`sqlite:///mlflow.db`), and `conf/logging.yml`.

- [ ] **Step 2: Create core `src/project_template/` package files**
  Create `__init__.py` (`__version__ = "0.1.0"`), `__main__.py`, `settings.py`, `hooks.py` (with MLflow logging hook or `kedro-mlflow` integration), and `pipeline_registry.py`.

- [ ] **Step 3: Verify Kedro CLI recognizes the project**
  Run `uv run kedro info` and confirm no import or config errors.

- [ ] **Step 4: Commit**

---

### Task 3: Implement `data_processing` and `reporting` Pipelines (TDD)

**Files:**
- Create: `tests/conftest.py`
- Create: `tests/pipelines/data_processing/test_nodes.py`
- Create: `tests/pipelines/reporting/test_nodes.py`
- Create: `src/project_template/pipelines/data_processing/{__init__.py,nodes.py,pipeline.py}`
- Create: `src/project_template/pipelines/reporting/{__init__.py,nodes.py,pipeline.py}`
- Modify: `src/project_template/pipeline_registry.py`

- [ ] **Step 1: Write failing unit tests for `data_processing` and `reporting` nodes**
  Follow Arrange / Act / Assert with keyword arguments, covering normal, empty, and edge-case inputs.

- [ ] **Step 2: Run `uv run pytest` to confirm tests fail (modules not yet implemented)**

- [ ] **Step 3: Implement `data_processing` and `reporting` nodes and pipelines, and register in `pipeline_registry.py`**
  Pure, typed functions with concise docstrings; `reporting` logs summary metrics to MLflow.

- [ ] **Step 4: Run `just test_ci`, `just typecheck`, `just lint_check`, and `just run`**
  Confirm >= 90% coverage, zero ruff/ty errors, and successful `kedro run` creating `mlflow.db`.

- [ ] **Step 5: Commit**

---

### Task 4: Port Kiro & Claude Steering, Rules, Skills, and Hooks

**Files:**
- Create: `CLAUDE.md`
- Create: `.kiro/steering/*.md` (14 general-purpose steering files from `pe-analytics-pipelines`, generalized)
- Create: `.claude/rules/*.md`, `.claude/skills/**`, `.claude/hooks/kiro_hooks.py`, `.claude/settings.json`

- [ ] **Step 1: Port `.kiro/steering/` general-purpose files**
  Copy and generalize `agent-defaults.md`, `coding-guidelines.md`, `code-style-standards.md`, `logging-standards.md`, `unit-test-standards.md`, `writing-standards.md`, `docs-figures-and-maths.md`, `experiment-figures.md`, `visualization.md`, `progress-tracking.md`, `session-handoff.md`, `steering-file-standards.md`, `code-review-checklist.md`, `worktrees.md` (replace `blueberry_forecast_kedro` with `project_template`, remove AWS/Bitbucket specifics).

- [ ] **Step 2: Port `CLAUDE.md`, `.claude/rules/`, `.claude/skills/`, `.claude/hooks/kiro_hooks.py`, and `.claude/settings.json`**
  Keep `git push --force* origin main*` deny rules and PreToolUse/PostToolUse hooks; remove AWS/Bitbucket rules and skills.

- [ ] **Step 3: Commit**

---

### Task 5: Update `README.md` and Final Verification

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Rewrite `README.md`**
  Document `uv` + `just` setup, `just run` / `just test_ci` / `just lint_check` / `just typecheck` / `just mlflow-local`, Kedro folder structure, and Kiro/Claude steering layout.

- [ ] **Step 2: Run full verification suite**
  Run `just lint_check`, `just typecheck`, `just test_ci`, and `just run`. Verify `git status` is clean of unintended artifacts.

- [ ] **Step 3: Commit**
