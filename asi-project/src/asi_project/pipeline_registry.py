"""Project pipelines."""

from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline
from .pipelines import (
data_engineering,
data_science
)
from typing import Dict


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    # 1. Import the individual pipelines from their respective modules.
    data_engineering_pipeline = data_engineering.create_pipeline()
    data_science_pipeline = data_science.create_pipeline()


    return {
        "de": data_engineering_pipeline,
        "ds": data_science_pipeline,
        "__default__": data_engineering_pipeline,
    }

