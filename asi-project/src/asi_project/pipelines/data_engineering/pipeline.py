from kedro.pipeline import Pipeline, node, pipeline
from .nodes import create_pokemon_dataframe, split_data

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=create_pokemon_dataframe,
                inputs="params:data_engineering",
                outputs="pokemon_metadata",
                name="create_metadata_node",
            ),
            node(
                func=split_data,
                inputs=["pokemon_metadata", "params:data_science"],
                outputs=["train_data", "test_data"],
                name="split_data_node",
            ),
        ]
    )