# Parallelism & Threading

Rules for running Kedro pipelines concurrently without thread oversubscription or native-library segmentation faults.

## 1. The OpenMP + `ThreadRunner` Problem

Libraries backed by OpenMP (LightGBM, XGBoost, scikit-learn) spawn internal C++ thread pools when `n_jobs=-1`. Kedro's `ThreadRunner` executes independent nodes concurrently across Python threads inside a single process.

Initializing OpenMP thread pools simultaneously from multiple Python threads can crash the process with a segmentation fault (`SIGSEGV` in `__kmp_suspend_initialize_thread`) or oversubscribe CPU cores (`N_nodes × N_cores` threads).

## 2. Core Rules

- **Pick one level of parallelism — never both at once.**
- **Cap `OMP_NUM_THREADS`** in the environment (or `settings.py`) when running under `ThreadRunner`.
- **Pass `n_jobs=1` on individual estimators** (`LGBMRegressor`, `XGBRegressor`, `RandomForestRegressor`, `GridSearchCV`) when parallelizing across nodes (`ThreadRunner`) or across outer model fits (`fit_n_jobs`).
- **Make hooks and shared utilities thread-safe:** protect shared counters and dictionaries in Kedro hooks with `threading.Lock()` (as in `ProfileHook`).

| Strategy | Kedro Runner | Outer `fit_n_jobs` | Estimator `n_jobs` | When to use |
| --- | --- | --- | --- | --- |
| Node + outer fit | `ThreadRunner` | `cores // concurrent_nodes` | `1` | Default for multi-node / multi-target pipelines |
| Node-level only | `ThreadRunner` | `1` | `1` | Debugging concurrent nodes with deterministic traces |
| Model-level | `SequentialRunner` | `1` | `-1` | Single heavy model fit on a large dataset |
| Process-level | `ParallelRunner` | `1` | `-1` | Separate OS processes (requires persisted Parquet/Pickle datasets) |

```python
# Good — safe inside ThreadRunner
model = LGBMRegressor(
    random_state=42, n_jobs=1, deterministic=True, force_row_wise=True
)

# Bad — spawns OpenMP thread pools inside Python threads under ThreadRunner
model = LGBMRegressor(random_state=42, n_jobs=-1)
```

## 3. Container CPU Limits

`multiprocessing.cpu_count()` reports the **host** machine's core count, not a container's cgroup vCPU quota. In containerized batch jobs, read the allocated vCPU budget from an explicit environment variable (or `os.process_cpu_count()` in Python 3.13+) before sizing thread pools.
