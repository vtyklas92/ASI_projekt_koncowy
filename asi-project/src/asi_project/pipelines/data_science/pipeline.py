from kedro.pipeline import Pipeline, node, pipeline

from .nodes import evaluate_model, train_model


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=train_model,
                inputs=["train_data", "params:data_science"],
                outputs="autogluon_predictor",
                name="train_model_node",
            ),
            node(
                func=evaluate_model,
                inputs=["autogluon_predictor", "test_data"],
                outputs=["classification_report", "confusion_matrix_plot"],
                name="evaluate_model_node",
            ),
        ]
    )
