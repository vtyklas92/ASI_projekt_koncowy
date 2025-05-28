from kedro.pipeline import Pipeline, node, pipeline
from .nodes import create_image_dataframe, split_data

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=create_image_dataframe,
                inputs="params:data_engineering.pokemon_data_dir",
                outputs="pokemon_master_df",
                name="create_image_dataframe_node",
            ),
            node(
                func=split_data,
                inputs=["pokemon_master_df", "params:data_engineering.test_size", "params:data_engineering.random_state"],
                outputs=["train_df", "test_df"],
                name="split_data_node",
            ),
        ]
    )
