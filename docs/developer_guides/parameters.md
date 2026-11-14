# Parameters

Rules for organizing, naming, and accessing Kedro parameters. For how parameters are wired into nodes, see [pipeline.md](pipeline.md).

## File Organization

Parameters live in `conf/base/parameters.yml` or under `conf/base/parameters/`, one file per domain:

```text
conf/base/
├── parameters.yml
└── parameters/
    ├── data_processing.yml
    └── reporting.yml
```

Nest parameters by pipeline/domain → stage → specific key:

```yaml
reporting:
  min_passenger_capacity: 5
```

Avoid flat parameter keys. Nesting makes it clear which stage uses what and prevents name collisions across domains.

## Accessing Parameters in Nodes

Pass the narrowest possible slice — not the whole domain dict:

```python
# Good — node receives only what it needs
node(
    func=summarize_fleet,
    inputs=["model_input_table", "params:reporting.min_passenger_capacity"],
    outputs="fleet_summary",
    name="summarize_fleet_node",
)
```

For multiple related parameters under the same parent key, pass the parent dict rather than listing every leaf path individually:

```python
# Good — one dict, clear boundary
inputs = ["raw_df", "params:ingestion.cols"]
```

## No Silent Defaults

Use `params["key"]` (direct access), not `params.get("key", default)`. Missing required keys should raise `KeyError` immediately rather than falling back silently; defaults belong in YAML.

```python
# Bad — silently ignores a missing key
timezone = params.get("timezone", "UTC")

# Good — fails loudly if the key isn't in YAML
timezone = params["timezone"]
```

## YAML Quoting Rules

| Value type | Rule | Example |
| --- | --- | --- |
| String | Always quote | `timezone: "UTC"` |
| Number | No quotes | `min_passenger_capacity: 5` |
| Boolean | No quotes | `enabled: true` |
| Date | Quote to avoid YAML date inference | `"2026-01-01": true` |
| Key | No quotes unless it looks like a boolean, number, or date | `reporting:` |
