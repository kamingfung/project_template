# Initialize Python environment and pre-commit hooks
init:
    export UV_LINK_MODE=copy
    uv python install 3.14
    uv sync --all-groups
    uv run pre-commit install

# Run formatting and lint fixes
lint:
    uv run ruff check --fix
    uv run ruff format

# Run read-only lint, format, and notebook output checks
lint_check:
    #!/usr/bin/env sh
    set -e
    uv run ruff check
    uv run ruff format --check
    if [ -d notebooks ]; then
        files=$(find notebooks -name '*.ipynb')
        if [ -n "$files" ]; then
            echo "$files" | xargs uvx nbstripout --verify
        fi
    fi

# Run static type checking with ty
typecheck:
    uv run ty check

# Run fast unit tests without coverage
test *args:
    uv run pytest -n auto --no-cov {{args}}

# Run unit tests with coverage report (CI)
test_ci:
    uv run pytest -n auto --cov=src/project_template --cov-report=term-missing

# Check for merge conflict markers
check_merge_conflicts:
    ! git grep -n '<<<<<<<' -- ':!*.lock' ':!Justfile'

# Scan working tree for secrets
check_secrets:
    gitleaks detect --source . --no-git --exit-code 2

# Audit locked dependencies for known vulnerabilities
audit:
    uv export --frozen --no-hashes --no-emit-project | uvx pip-audit -r /dev/stdin --no-deps --disable-pip
