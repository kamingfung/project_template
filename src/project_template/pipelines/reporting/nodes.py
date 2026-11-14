"""Nodes for the reporting pipeline."""

import mlflow
import pandas as pd


def summarize_fleet(
    model_input_table: pd.DataFrame,
    min_passenger_capacity: int,
) -> pd.DataFrame:
    """Aggregate eligible shuttles by type and log summary metrics to MLflow."""
    eligible = model_input_table[
        model_input_table["passenger_capacity"] >= min_passenger_capacity
    ]
    if eligible.empty:
        mlflow.log_metrics({"eligible_shuttle_count": 0.0})
        return pd.DataFrame(
            columns=["shuttle_type", "shuttle_count", "avg_price", "total_capacity"]
        )

    summary = (
        eligible.groupby("shuttle_type", as_index=False)
        .agg(
            shuttle_count=("shuttle_id", "count"),
            avg_price=("price", "mean"),
            total_capacity=("passenger_capacity", "sum"),
        )
        .sort_values("shuttle_type")
        .reset_index(drop=True)
    )
    mlflow.log_metrics(
        {
            "eligible_shuttle_count": float(len(eligible)),
            "mean_shuttle_price": float(eligible["price"].mean()),
        }
    )
    return summary
