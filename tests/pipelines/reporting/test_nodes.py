"""Unit tests for reporting nodes."""

import pandas as pd
import pytest

from project_template.pipelines.reporting.nodes import summarize_fleet


def test_summarize_fleet_filters_by_min_capacity_and_aggregates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Summary filters below min_passenger_capacity and logs metrics to MLflow."""
    logged_metrics: dict[str, float] = {}
    monkeypatch.setattr(
        "project_template.pipelines.reporting.nodes.mlflow.active_run",
        lambda: object(),
    )
    monkeypatch.setattr(
        "project_template.pipelines.reporting.nodes.mlflow.log_metrics",
        lambda metrics: logged_metrics.update(metrics),
    )
    model_input = pd.DataFrame(
        {
            "shuttle_id": [101, 102, 103],
            "shuttle_type": ["Type V5", "Type A2", "Type V5"],
            "passenger_capacity": [4, 1, 6],
            "price": [1200.0, 750.0, 1800.0],
        }
    )

    result = summarize_fleet(
        model_input_table=model_input,
        min_passenger_capacity=2,
    )

    assert len(result) == 1
    assert result.iloc[0]["shuttle_type"] == "Type V5"
    assert result.iloc[0]["shuttle_count"] == 2
    assert result.iloc[0]["avg_price"] == pytest.approx(1500.0)
    assert logged_metrics["eligible_shuttle_count"] == pytest.approx(2.0)


def test_summarize_fleet_empty_after_filter(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """When no shuttles meet capacity threshold, returns empty summary and logs 0."""
    logged_metrics: dict[str, float] = {}
    monkeypatch.setattr(
        "project_template.pipelines.reporting.nodes.mlflow.active_run",
        lambda: object(),
    )
    monkeypatch.setattr(
        "project_template.pipelines.reporting.nodes.mlflow.log_metrics",
        lambda metrics: logged_metrics.update(metrics),
    )
    model_input = pd.DataFrame(
        {
            "shuttle_id": [102],
            "shuttle_type": ["Type A2"],
            "passenger_capacity": [1],
            "price": [750.0],
        }
    )

    result = summarize_fleet(
        model_input_table=model_input,
        min_passenger_capacity=5,
    )

    assert result.empty
    assert logged_metrics["eligible_shuttle_count"] == pytest.approx(0.0)


def test_summarize_fleet_skips_mlflow_without_active_run(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """When no MLflow run is active, log_metrics is not called."""
    called = False

    def _fail_log_metrics(_metrics: dict[str, float]) -> None:
        nonlocal called
        called = True

    monkeypatch.setattr(
        "project_template.pipelines.reporting.nodes.mlflow.active_run",
        lambda: None,
    )
    monkeypatch.setattr(
        "project_template.pipelines.reporting.nodes.mlflow.log_metrics",
        _fail_log_metrics,
    )
    model_input = pd.DataFrame(
        {
            "shuttle_id": [101],
            "shuttle_type": ["Type V5"],
            "passenger_capacity": [4],
            "price": [1200.0],
        }
    )

    result = summarize_fleet(
        model_input_table=model_input,
        min_passenger_capacity=2,
    )

    assert len(result) == 1
    assert not called
