import importlib
import os
import threading
import time
from collections import defaultdict
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pandas as pd
from kedro.framework.hooks import hook_impl
from kedro.io import DataCatalog
from kedro.pipeline import Pipeline
from kedro.pipeline.node import Node
from rich.console import Console
from rich.table import Table

LOAD_COUNT = "Load Count"
SAVE_COUNT = "Save Count"
LOAD_TIME = "Loading Time(s)"
SAVE_TIME = "Saving Time(s)"
NODE_RUN_TIME = "Node Compute Time(s)"
TOTAL_TIME = "Total Time(s)"
EXECUTION_ORDER = "Execution Order"


@dataclass()
class ProfileHook:
    """Kedro hook for profiling pipeline execution performance.

    This hook tracks and profiles the execution time of nodes and datasets
    in a Kedro pipeline, providing detailed performance metrics including
    loading time, computation time, and saving time.

    Attributes:
        env: Environment(s) to run in. Can be a single environment or list.
        save_file: Whether to save profiling results to CSV files.
        node_profile_path: Path where node profiling CSV will be saved.
        dataset_profile_path: Path where dataset profiling CSV will be saved.
    """

    env: str | list[str] = "local"
    save_file: bool = False
    node_profile_path: str | Path = field(
        default_factory=lambda: (
            f"profiling/node_profile_{time.strftime('%Y%m%d_%H%M%S')}.csv"
        )
    )
    dataset_profile_path: str | Path = field(
        default_factory=lambda: (
            f"profiling/dataset_profile_{time.strftime('%Y%m%d_%H%M%S')}.csv"
        )
    )

    def __post_init__(self) -> None:
        """Initialize profiling hook after dataclass initialization.

        Sets up internal state for profiling including:
        - Rich output formatting configuration
        - Enable/disable state based on environment variables
        - Profile data structures for nodes and datasets
        - Pipeline start time tracking
        """
        if os.environ.get("KEDRO_PROFILE_RICH") == "0":
            self.rich_enabled = False
        else:
            try:
                importlib.import_module("rich")
                self.rich_enabled = True
            except ImportError:
                self.rich_enabled = False

        if os.environ.get("KEDRO_PROFILE_DISABLE") == "1":
            self.disable = True
        else:
            self.disable = False

        self._dataset_profile: defaultdict[str, dict[str, Any]] = defaultdict(
            lambda: {}
        )
        self._node_profile: defaultdict[str, dict[str, Any]] = defaultdict(lambda: {})
        self._load_starts: dict[tuple[int, str, str], float] = {}
        self._save_starts: dict[tuple[int, str, str], float] = {}
        self._lock = threading.Lock()

        self._pipeline_start: float = time.time()
        self._node_execution_order: int = 0

    def __hash__(self) -> int:
        """Return hash of the ProfileHook instance.

        Returns:
            Hash value based on instance id (dataclass has no hash method by default).
        """
        return id(self)

    def _save_to_csv(self, df: pd.DataFrame, file_path: str | Path) -> None:
        """Save DataFrame to CSV file.

        Args:
            df: DataFrame containing profiling data to save.
            file_path: Path where CSV file should be saved.
        """
        try:
            # Ensure the directory exists
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(file_path, index=False)
        except Exception as e:
            print(f"Failed to save profile data to {file_path}: {e}")

    def _print_path_saved(self, file_path: str | Path) -> None:
        """Print message indicating where profile data was saved.

        Args:
            file_path: Path where the profile data was saved.
        """
        print(f"Profile data saved to: {file_path}")

    def save_partial_results(self) -> None:
        """Save partial results to CSV files.

        This method is useful when pipelines fail, allowing you to save
        whatever profiling data has been collected up to the point of failure.
        """
        if self.disable or not self.save_file:
            return

        self._total_time = time.time() - self._pipeline_start

        # Build DataFrames for both node and dataset profiles
        node_df = _build_node_table(self._node_profile, index_name="Node Name")
        dataset_df = _build_dataset_table(
            self._dataset_profile, index_name="Dataset Name"
        )

        # Save to CSV files
        self._save_to_csv(node_df, self.node_profile_path)
        self._save_to_csv(dataset_df, self.dataset_profile_path)

        print("Partial profiling results saved due to pipeline failure.")

    # Node Profile
    @hook_impl
    def before_node_run(
        self, node: Node, catalog: DataCatalog, inputs: dict[str, Any]
    ) -> None:
        """Track node execution start time.

        Args:
            node: The Kedro node about to be executed.
            catalog: The data catalog containing datasets.
            inputs: Dictionary of input datasets for the node.
        """
        if self.disable:
            return

        with self._lock:
            self._node_execution_order += 1
            self._node_profile[node.name][EXECUTION_ORDER] = self._node_execution_order
            self._node_profile[node.name][NODE_RUN_TIME] = time.time()

    @hook_impl
    def after_node_run(
        self, node: Node, catalog: DataCatalog, inputs: dict[str, Any]
    ) -> None:
        """Calculate node execution time after node completes.

        Args:
            node: The Kedro node that just finished executing.
            catalog: The data catalog containing datasets.
            inputs: Dictionary of input datasets for the node.
        """
        if self.disable:
            return
        with self._lock:
            self._node_profile[node.name][NODE_RUN_TIME] = (
                time.time() - self._node_profile[node.name][NODE_RUN_TIME]
            )

    @hook_impl
    def on_node_error(
        self,
        error: Exception,
        node: Node,
        catalog: DataCatalog,
        inputs: dict[str, Any],
        is_async: bool,
    ) -> None:
        """Handle node errors and save partial results.

        Args:
            error: The exception that was raised.
            node: The Kedro node that encountered an error.
            catalog: The data catalog containing datasets.
            inputs: Dictionary of input datasets for the node.
            is_async: Whether the node was running asynchronously.
        """
        if self.disable:
            return

        # Calculate partial node time if it was started
        with self._lock:
            if NODE_RUN_TIME in self._node_profile[node.name]:
                self._node_profile[node.name][NODE_RUN_TIME] = (
                    time.time() - self._node_profile[node.name][NODE_RUN_TIME]
                )

        # Save partial results when a node fails
        self.save_partial_results()

    # Dataset profile
    @hook_impl
    def before_dataset_loaded(self, dataset_name: str, node: Node) -> None:
        """Track dataset loading start time.

        Args:
            dataset_name: Name of the dataset being loaded.
            node: The Kedro node loading the dataset.
        """
        if self.disable:
            return
        key = (threading.get_ident(), dataset_name, node.name)
        with self._lock:
            self._load_starts[key] = time.time()

    @hook_impl
    def after_dataset_loaded(self, dataset_name: str, node: Node) -> None:
        """Calculate and accumulate dataset loading time.

        Args:
            dataset_name: Name of the dataset that was loaded.
            node: The Kedro node that loaded the dataset.
        """
        if self.disable:
            return
        now = time.time()
        key = (threading.get_ident(), dataset_name, node.name)
        with self._lock:
            start = self._load_starts.pop(key, now)
            load_duration = now - start

            # Accumulate the duration instead of overwriting
            self._dataset_profile[dataset_name][LOAD_TIME] = (
                self._dataset_profile[dataset_name].get(LOAD_TIME, 0) + load_duration
            )
            self._node_profile[node.name][LOAD_TIME] = (
                self._node_profile[node.name].get(LOAD_TIME, 0) + load_duration
            )
            self._dataset_profile[dataset_name][LOAD_COUNT] = (
                self._dataset_profile[dataset_name].get(LOAD_COUNT, 0) + 1
            )

    @hook_impl
    def before_dataset_saved(self, dataset_name: str, node: Node) -> None:
        """Track dataset saving start time.

        Args:
            dataset_name: Name of the dataset being saved.
            node: The Kedro node saving the dataset.
        """
        if self.disable:
            return
        key = (threading.get_ident(), dataset_name, node.name)
        with self._lock:
            self._save_starts[key] = time.time()

    @hook_impl
    def after_dataset_saved(self, dataset_name: str, node: Node) -> None:
        """Calculate and accumulate dataset saving time.

        Args:
            dataset_name: Name of the dataset that was saved.
            node: The Kedro node that saved the dataset.
        """
        if self.disable:
            return
        now = time.time()
        key = (threading.get_ident(), dataset_name, node.name)
        with self._lock:
            start = self._save_starts.pop(key, now)
            save_duration = now - start

            # Accumulate the duration instead of overwriting
            self._dataset_profile[dataset_name][SAVE_TIME] = (
                self._dataset_profile[dataset_name].get(SAVE_TIME, 0) + save_duration
            )
            self._node_profile[node.name][SAVE_TIME] = (
                self._node_profile[node.name].get(SAVE_TIME, 0) + save_duration
            )
            self._dataset_profile[dataset_name][SAVE_COUNT] = (
                self._dataset_profile[dataset_name].get(SAVE_COUNT, 0) + 1
            )

    @hook_impl
    def before_pipeline_run(
        self,
        run_params: dict[str, Any],
        pipeline: Pipeline,
        catalog: DataCatalog,
    ) -> None:
        """Initialize profiling at the start of pipeline execution.

        Args:
            run_params: Parameters passed to the pipeline run.
            pipeline: The Kedro pipeline being executed.
            catalog: The data catalog containing datasets.
        """
        if self.disable:
            return
        self._pipeline_start = time.time()
        self.run_env = run_params.get("env") if run_params.get("env") else "local"

    @hook_impl
    def on_pipeline_error(
        self,
        error: Exception,
        run_params: dict[str, Any],
        pipeline: Pipeline,
        catalog: DataCatalog,
    ) -> None:
        """Handle pipeline errors and save partial results.

        Args:
            error: The exception that caused the pipeline to fail.
            run_params: Parameters passed to the pipeline run.
            pipeline: The Kedro pipeline that encountered an error.
            catalog: The data catalog containing datasets.
        """
        if self.disable:
            return

        print(f"Pipeline failed with error: {error}")
        # Save partial results when the entire pipeline fails
        self.save_partial_results()

    @hook_impl
    def after_pipeline_run(
        self,
        run_params: dict[str, Any],
        run_result: dict[str, Any],
        pipeline: Pipeline,
        catalog: DataCatalog,
    ) -> None:
        """Generate and display profiling results after pipeline completes.

        Args:
            run_params: Parameters passed to the pipeline run.
            run_result: Results from the pipeline execution.
            pipeline: The Kedro pipeline that was executed.
            catalog: The data catalog containing datasets.
        """
        if self.disable:
            return

        self._total_time = time.time() - self._pipeline_start

        # Build DataFrames for both node and dataset profiles
        node_df = _build_node_table(self._node_profile, index_name="Node Name")
        dataset_df = _build_dataset_table(
            self._dataset_profile, index_name="Dataset Name"
        )

        # Save to CSV files if enabled
        if self.save_file:
            self._save_to_csv(node_df, self.node_profile_path)
            self._save_to_csv(dataset_df, self.dataset_profile_path)

        # Add total row for display tables
        node_df_display = _add_total_row(node_df.copy(), "Node Name")
        node_df_display = _add_wall_clock_row(
            node_df_display, "Node Name", self._total_time
        )
        dataset_df_display = _add_total_row(dataset_df.copy(), "Dataset Name")
        dataset_df_display = _add_wall_clock_row(
            dataset_df_display, "Dataset Name", self._total_time
        )

        # Display results
        if self.rich_enabled:
            print()
            print("=" * 10 + "Node Summary" + "=" * 10)
            node_summary = dataframe_to_rich_table(node_df_display)
            print_rich_table_to_console(node_summary)
            if self.save_file:
                self._print_path_saved(file_path=self.node_profile_path)

            print()
            print("=" * 10 + "Dataset Summary" + "=" * 10)
            dataset_summary = dataframe_to_rich_table(dataset_df_display)
            print_rich_table_to_console(dataset_summary)
            if self.save_file:
                self._print_path_saved(file_path=self.dataset_profile_path)

        else:
            print("Node Profile:")
            print(node_df_display)
            if self.save_file:
                self._print_path_saved(file_path=self.node_profile_path)

            print("\nDataset Profile:")
            print(dataset_df_display)
            if self.save_file:
                self._print_path_saved(file_path=self.dataset_profile_path)


# Format Table
def dataframe_to_rich_table(df: pd.DataFrame) -> Table:
    """Convert a pandas DataFrame to a Rich Table for console display.

    Automatically detects summary rows ("TOTAL" and
    "TOTAL Wall Clock") and adds a separator line before them for
    better visual distinction. Numeric columns are formatted with
    thousands separators and aligned on decimal places.

    Args:
        df: Pandas DataFrame to convert to a Rich table.

    Returns:
        Rich Table object ready for console printing.
    """
    table = Table(show_header=True, header_style="bold magenta")

    # Create a copy to avoid modifying the original DataFrame
    df_formatted = df.copy()

    # Format numeric columns (including object columns coerced by "" summary cells)
    for col in df.columns:
        non_empty = [v for v in df[col] if v != "" and pd.notna(v)]
        is_numeric = pd.api.types.is_numeric_dtype(df[col]) or (
            bool(non_empty)
            and all(
                isinstance(v, (int, float)) and not isinstance(v, bool)
                for v in non_empty
            )
        )
        if is_numeric:
            is_integer_col = pd.api.types.is_integer_dtype(df[col]) or (
                bool(non_empty) and all(isinstance(v, int) for v in non_empty)
            )
            if is_integer_col:
                df_formatted[col] = df_formatted[col].apply(
                    lambda x: (
                        "" if x == "" else (f"{int(x):,}" if pd.notna(x) else str(x))
                    )
                )
            else:
                df_formatted[col] = df_formatted[col].apply(
                    lambda x: (
                        ""
                        if x == ""
                        else (f"{float(x):,.2f}" if pd.notna(x) else str(x))
                    )
                )
            table.add_column(col, justify="right")
        else:
            table.add_column(col, justify="left")

    # Add rows
    rows = list(df_formatted.iterrows())
    for idx, (_, row) in enumerate(rows):
        is_total_row = any(str(cell) in ("TOTAL", "Time Elapsed") for cell in row)

        # Add separator before total rows
        if is_total_row and idx > 0:
            table.add_section()

        table.add_row(*[str(cell) for cell in row])

    return table


def print_rich_table_to_console(rich_table: Table) -> None:
    """Print a Rich Table to the console.

    Args:
        rich_table: Rich Table object to print.
    """
    console = Console()
    console.print(rich_table)


def _format_duration(seconds: float) -> str:
    """Format elapsed seconds into a concise human-readable string."""
    if seconds < 1.0:
        return "a moment"
    if seconds < 60.0:
        rounded = round(seconds)
        return "a second" if rounded == 1 else f"{rounded} seconds"
    minutes, rem_seconds = divmod(round(seconds), 60)
    if minutes < 60:
        return f"{minutes}m {rem_seconds}s"
    hours, rem_minutes = divmod(minutes, 60)
    return f"{hours}h {rem_minutes}m {rem_seconds}s"


def _build_profile_table(
    dictionary: Mapping[str, dict[str, Any]],
    index_name: str,
    time_cols: list[str],
) -> pd.DataFrame:
    """Build a sorted, rounded profiling DataFrame from raw timing metrics."""
    df = pd.DataFrame.from_dict(dict(dictionary), orient="index")
    for col in time_cols:
        if col not in df.columns:
            df[col] = 0.0
    df[TOTAL_TIME] = df[time_cols].sum(axis=1, skipna=True)
    df["Total Time"] = df[TOTAL_TIME].apply(_format_duration)
    return (
        df.reset_index(names=index_name)
        .sort_values(TOTAL_TIME, ascending=False)
        .round(2)
    )


def _build_node_table(
    dictionary: Mapping[str, dict[str, Any]], index_name: str
) -> pd.DataFrame:
    """Build a formatted DataFrame from node profiling data."""
    df = _build_profile_table(
        dictionary=dictionary,
        index_name=index_name,
        time_cols=[LOAD_TIME, NODE_RUN_TIME, SAVE_TIME],
    )
    if EXECUTION_ORDER not in df.columns:
        df[EXECUTION_ORDER] = 0
    df[EXECUTION_ORDER] = df[EXECUTION_ORDER].fillna(0).astype(int)
    return df[
        [
            "Execution Order",
            "Node Name",
            "Loading Time(s)",
            "Node Compute Time(s)",
            "Saving Time(s)",
            "Total Time(s)",
            "Total Time",
        ]
    ]


def _build_dataset_table(
    dictionary: Mapping[str, dict[str, Any]], index_name: str
) -> pd.DataFrame:
    """Build a formatted DataFrame from dataset profiling data."""
    df = _build_profile_table(
        dictionary=dictionary,
        index_name=index_name,
        time_cols=[LOAD_TIME, SAVE_TIME],
    )
    if LOAD_COUNT in df.columns:
        df[LOAD_COUNT] = df[LOAD_COUNT].fillna(0).astype(int)
    if SAVE_COUNT in df.columns:
        df[SAVE_COUNT] = df[SAVE_COUNT].fillna(0).astype(int)
    return df


def _append_summary_row(
    df: pd.DataFrame,
    index_col_name: str,
    label: str,
    col_value_fn: Any,
) -> pd.DataFrame:
    """
    Append a single summary row to a profiling DataFrame.

    Iterates over columns, calling col_value_fn to determine each cell's
    value. Handles the empty-df guard and concat boilerplate in one place.

    Args:
        df: DataFrame containing profiling data.
        index_col_name: Name of the index column (receives the label).
        label: Text placed in the index column (e.g. "TOTAL").
        col_value_fn: Callable(col, df) -> value for each non-index column.

    Returns:
        New DataFrame with the summary row appended.
    """
    if df.empty:
        return df

    row: dict[str, Any] = {index_col_name: label}
    for col in df.columns:
        if col == index_col_name:
            continue
        row[col] = col_value_fn(col, df)

    return pd.concat([df, pd.DataFrame([row])], ignore_index=True)


def _add_total_row(df: pd.DataFrame, index_col_name: str) -> pd.DataFrame:
    """
    Add a total row summing all numeric columns.

    Creates a summary row labeled "TOTAL (sum of nodes)" that aggregates
    numeric values across all rows. Special handling for execution order
    (left blank) and human-readable time fields.

    Args:
        df: DataFrame containing profiling data.
        index_col_name: Name of the index column.

    Returns:
        New DataFrame with a total row appended at the end.
    """

    def _col_value(col: str, source_df: pd.DataFrame) -> Any:
        if col == EXECUTION_ORDER:
            return ""
        if col == "Total Time":
            if TOTAL_TIME in source_df.columns:
                total_seconds = source_df[TOTAL_TIME].sum()
                return _format_duration(total_seconds)
            return ""
        if pd.api.types.is_numeric_dtype(source_df[col]):
            return round(source_df[col].sum(), 2)
        return ""

    return _append_summary_row(df, index_col_name, "TOTAL", _col_value)


def _add_wall_clock_row(
    df: pd.DataFrame, index_col_name: str, wall_clock_seconds: float
) -> pd.DataFrame:
    """
    Add a wall clock row showing actual elapsed pipeline time.

    When using ThreadRunner, nodes run concurrently so the sum of individual
    node times exceeds the actual wall-clock duration. This row shows the
    real elapsed time, making the parallelism benefit visible.

    Args:
        df: DataFrame with profiling data (should already have a TOTAL row).
        index_col_name: Name of the index column.
        wall_clock_seconds: Actual elapsed time in seconds.

    Returns:
        DataFrame with a wall clock row appended after the total row.
    """

    def _col_value(col: str, _source_df: pd.DataFrame) -> Any:
        if col == TOTAL_TIME:
            return round(wall_clock_seconds, 2)
        if col == "Total Time":
            return _format_duration(wall_clock_seconds)
        return ""

    return _append_summary_row(df, index_col_name, "Time Elapsed", _col_value)
