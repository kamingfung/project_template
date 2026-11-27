# project_template

Stack-agnostic Python project template. It sets up the tooling only: **uv**, **just**, **ruff**, **ty**, **pytest**, **pre-commit**, and CI. It has no framework, data, or ML dependencies. Add your own stack on top.

## Quickstart

1. Install prerequisites:

   ```bash
   brew install uv just
   ```

2. Initialize the Python environment and pre-commit hooks:

   ```bash
   just init
   ```

3. Run the quality gates:

   ```bash
   just lint_check && just typecheck && just test_ci
   ```

## Common Commands

| Command | Purpose |
| --- | --- |
| `just init` | Install Python 3.14, sync `uv` dependencies, and install pre-commit hooks |
| `just test` | Run unit tests in parallel without coverage |
| `just test_ci` | Run unit tests with coverage report (90% minimum) |
| `just lint` | Auto-fix lint issues and format code with `ruff` |
| `just lint_check` | Verify `ruff` lint/format and stripped notebook outputs |
| `just typecheck` | Run static type checking with `ty` |
| `just audit` | Audit locked dependencies with `pip-audit` |

## Adding Dependencies

```bash
uv add <package>          # runtime dependency
uv add --dev <package>    # dev dependency
uv lock --upgrade         # upgrade within constraints
uv run pre-commit autoupdate
```

## Folder Structure

```text
├── src/project_template/   # Package code
├── tests/                  # Unit tests mirroring src/project_template/
├── docs/                   # Project docs
├── Justfile                # Task runner recipes
└── pyproject.toml          # Metadata, dependencies, and tool config
```

## Starting a New Project

Rename `project_template` in `pyproject.toml`, `src/`, `README.md`, and the `Justfile` coverage path. Then add your stack (for example Kedro, Dagster, or plain scripts) and its CI job.
