project := justfile_directory()

# Initialize Python environment and pre-commit hooks
init:
    export UV_LINK_MODE=copy
    uv python install 3.14
    uv sync --all-groups
    uv run pre-commit install

# Symlink local agent plugin (data-scientist) into ~/.gemini/config/plugins
plugins:
    #!/usr/bin/env sh
    set -e
    mkdir -p "$HOME/.gemini/config/plugins"
    parent_dir=$(dirname "{{project}}")
    src="$parent_dir/data-scientist"
    dest="$HOME/.gemini/config/plugins/data-scientist"
    if [ -d "$src" ]; then
        ln -sfn "$src" "$dest"
        echo "Linked data-scientist -> $dest"
    else
        echo "Missing $src; clone data-scientist next to {{project}} or install via Plugins Manager." >&2
        exit 1
    fi

# Remove sample spaceflights data, pipelines, tests, and config to start fresh
reset-example:
    #!/usr/bin/env sh
    set -e
    rm -f \
        data/01_raw/companies.csv \
        data/01_raw/shuttles.csv \
        data/02_intermediate/preprocessed_companies.pq \
        data/02_intermediate/preprocessed_shuttles.pq \
        data/03_primary/model_input_table.pq \
        data/08_reporting/fleet_summary.csv
    rm -rf \
        src/project_template/pipelines/data_processing \
        src/project_template/pipelines/reporting \
        tests/pipelines/data_processing \
        tests/pipelines/reporting
    printf '# Add Kedro datasets here.\n{}\n' > conf/base/catalog.yml
    printf '# Add pipeline parameters here.\n{}\n' > conf/base/parameters.yml
    printf '"""Shared pytest fixtures for project_template tests."""\n' > tests/conftest.py
    echo "Example data, pipelines, tests, and config removed."

# Run Kedro pipeline
run *args:
    uv run kedro run {{args}}

# Launch Kedro-Viz
viz:
    uv run kedro viz run

# Internal: print a free TCP port
_free-port:
    @python3 -c "import socket; s=socket.socket(); s.bind(('',0)); print(s.getsockname()[1]); s.close()"

# Launch MLflow UI against local sqlite backend
mlflow-local:
    #!/usr/bin/env sh
    PORT=$(just _free-port)
    echo "Starting MLflow UI on http://localhost:$PORT"
    uv run mlflow ui --backend-store-uri sqlite:///mlflow.db --port "$PORT"

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
