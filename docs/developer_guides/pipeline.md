# Kedro Pipeline Conventions

Rules for adding, wiring, and naming pipelines and nodes. For parameter injection, see [parameters.md](parameters.md). For schema validation at node boundaries, see [schema_validation.md](schema_validation.md).

## 1. Pipeline & Data Layers

Each pipeline layer has a single responsibility and writes to a specific Kedro `data/` directory. Layers `01_raw`–`04_feature` are shared infrastructure; `05_model_input` onward are scoped to a specific model or report.

| Layer | Responsibility | Data directory | Granularity |
| --- | --- | --- | --- |
| **Ingestion** | Standardize column names, cast types, parse strings, remove invalid rows; no reshaping | `01_raw` -> `02_intermediate` | Source grain |
| **Preprocessing** | Align grains, join cleaned sources, validate core contracts | `03_primary` | Entity / time grain |
| **Feature Engineering** | Derive ratios, lags, rolling stats, and interactions from `03_primary` | `04_feature` | Same as preprocessing |
| **Modeling Input** | Assemble and filter model-specific training/inference tables | `05_model_input` | Model-specific |
| **Modeling** | Train/evaluate models and generate predictions | `06_models` + `07_model_output` | Predictions |
| **Reporting** | Aggregate and format outputs for dashboards, exports, and tracking | `08_reporting` | Consumer-specific |

## 2. Pipeline Package Structure

Each domain lives in its own package under `src/project_template/pipelines/`:

```text
src/project_template/
├── pipeline_registry.py  ← registers all domain pipelines
└── pipelines/
    ├── data_processing/
    │   ├── __init__.py
    │   ├── nodes.py      ← pure functions, one per node
    │   ├── pipeline.py   ← create_pipeline() wiring only
    │   └── schemas.py    ← Pandera schemas
    └── reporting/
        ├── __init__.py
        ├── nodes.py
        └── pipeline.py
```

- **Node functions live in `nodes.py`; wiring lives in `pipeline.py`.** Never put transformation logic inside `pipeline.py`.
- **Node functions are pure:** Kedro injects all datasets and parameters; never call `catalog.load()` inside a node or log node start/finish (see [logging.md](logging.md)).

## 3. `create_pipeline()`, Naming & Tags

- Every `pipeline.py` exposes `create_pipeline(**kwargs) -> Pipeline`.
- Name every node after its function (`name="preprocess_companies_node"` or `name="preprocess_companies"`) so runner logs, `ProfileHook` tables, and Kedro-Viz stay unambiguous. Never use generic names like `"step_1"`.
- Use a list for `inputs` when positional order matches the function signature, or a dict to bind arguments explicitly by name.
- Tag nodes with their domain (`tags=["data_processing"]`) so slices can be executed via `kedro run --tags=...`.

## 4. Adding a New Pipeline

1. Create `src/project_template/pipelines/<domain>/` with `__init__.py`, `nodes.py`, `pipeline.py`, and `schemas.py` (if introducing new contracts).
2. Add catalog entries in `conf/base/catalog.yml` (using `ParquetDataset` for intermediate tables).
3. Add parameters in `conf/base/parameters.yml` (nested under `<domain>:`).
4. Register the pipeline in `src/project_template/pipeline_registry.py`.
5. Add unit tests under `tests/pipelines/<domain>/test_nodes.py`.

## 5. Running Pipelines

```zsh
just run                                    # Run default pipeline (uv run kedro run)
just run --pipeline=data_processing         # Run one registered pipeline
just run --nodes=preprocess_companies_node  # Run a single node
just run --tags=data_processing             # Run nodes matching a tag
just run --runner=ThreadRunner              # Run independent nodes concurrently
just viz                                    # Launch interactive Kedro-Viz DAG viewer
just mlflow-local                           # Launch MLflow UI against sqlite:///mlflow.db
```
