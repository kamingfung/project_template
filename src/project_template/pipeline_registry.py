"""Project pipelines."""

from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline


def register_pipelines() -> dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        Mapping from pipeline name to ``Pipeline`` object.
    """
    pipelines = find_pipelines()
    pipelines["__default__"] = sum(pipelines.values(), Pipeline([]))
    return pipelines
