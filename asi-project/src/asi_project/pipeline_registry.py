from kedro.pipeline import Pipeline, pipeline

from .pipelines import data_engineering as de
from .pipelines import data_science as ds


def register_pipelines() -> dict[str, Pipeline]:
    """Rejestruje pipeline'y projektu."""
    data_engineering_pipeline = de.create_pipeline()
    data_science_pipeline = ds.create_pipeline()

    return {
        "de": data_engineering_pipeline,
        "ds": data_science_pipeline,
        "__default__": pipeline([data_engineering_pipeline, data_science_pipeline]),
    }
