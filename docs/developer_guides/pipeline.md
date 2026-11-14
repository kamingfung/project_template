# Kedro Pipeline Conventions

Rules for adding, wiring, and naming pipelines and nodes. For parameter injection, see [parameters.md](parameters.md). For schema validation at node boundaries, see [schema_validation.md](schema_validation.md).

## Data Layers

```text
data/
├── 01_raw/              ← Raw data as loaded from source (read-only)
├── 02_intermediate/     ← Cleaned, typed, validated
├── 03_primary/          ← Reshaped/aggregated to standard grains
├── 04_feature/          ← Derived features
├── 05_model_input/      ← Merged, model-ready input tables
├── 06_models/           ← Trained model artifacts
├── 07_model_output/     ← Predictions and evaluation outputs
└── 08_reporting/        ← Consumer-formatted outputs (summaries, CSVs)
```

## Pipeline File Structure

Each domain lives in its own package under `src/project_template/pipelines/`:

```text
src/project_template/
├── pipeline_registry.py  ← registers all domain pipelines
└── pipelines/
    ├── data_processing/
    │   ├── __init__.py
    │   ├── nodes.py      ← pure functions, one per node
    │   ├── pipeline.py   ← create_pipeline() for this domain
    │   └── schemas.py    ← Pandera schemas
    └── reporting/
        ├── __init__.py
        ├── nodes.py
        └── pipeline.py
```

Node functions live in `nodes.py`; wiring lives in `pipeline.py`. Never put business logic inside `pipeline.py`.

## `create_pipeline()` and Node Naming

- Every `pipeline.py` exposes `create_pipeline(**kwargs) -> Pipeline`.
- Match the node `name` to the function name (or `<func>_node`) consistently so runner logs and Kedro-Viz stay unambiguous.
- Never use generic names like `"step_1"` or `"process_data"`.
- Use a list for `inputs` when positional order matches the function signature, or a dict to bind arguments explicitly by name.

## Adding a New Pipeline

1. Create `src/project_template/pipelines/<domain>/` with `__init__.py`, `nodes.py`, and `pipeline.py`.
2. Add catalog entries in `conf/base/catalog.yml` (or `conf/base/catalog/<domain>.yml`).
3. Add parameters in `conf/base/parameters.yml` (or `conf/base/parameters/<domain>.yml`).
4. Register the new pipeline in `src/project_template/pipeline_registry.py`.
