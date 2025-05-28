from kedro.pipeline import Pipeline, node
from .nodes import create_pokemon_dataframe, split_data

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            node(
                func=create_pokemon_dataframe,
                inputs="params:data_engineering_params",
                outputs="pokemon_metadata", # Dane pośrednie, nie zapisywane w catalog.yml
                name="create_metadata_node",
            ),
            node(
                func=split_data,
                inputs=["pokemon_metadata", "params:data_science_params"],
                outputs=["train_data", "test_data"],
                name="split_data_node",
            ),
        ]
    )