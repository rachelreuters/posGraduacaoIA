from kedro.pipeline import Pipeline, node, pipeline

from . import nodes


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=nodes.model_train_regLog,
                inputs=["dev_train","params:mlflow_experiment"],
                outputs="regLog_model",
            ),
            node(
                func=nodes.model_train_decisionTree,
                inputs=["dev_train","params:mlflow_experiment"],
                outputs="decisionTree_model",
            )
        ]
    )
