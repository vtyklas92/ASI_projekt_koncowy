from kedro.pipeline import Pipeline, node
from .nodes import train_model, evaluate_model

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            node(
                func=train_model,
                inputs=["train_data", "params:data_science_params"],
                outputs="autogluon_predictor",
                name="train_autogluon_model_node",
            ),
            node(
                func=evaluate_model,
                inputs=["autogluon_predictor", "test_data"],
                outputs=["classification_report", "confusion_matrix_plot"],
                name="evaluate_model_node",
            ),
        ]
    )