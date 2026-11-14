"""Pipeline definition for reporting."""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import summarize_fleet


def create_pipeline(**kwargs: object) -> Pipeline:
    """Build the reporting pipeline."""
    return pipeline(
        [
            node(
                func=summarize_fleet,
                inputs=["model_input_table", "params:reporting.min_passenger_capacity"],
                outputs="fleet_summary",
                name="summarize_fleet_node",
            ),
        ]
    )
