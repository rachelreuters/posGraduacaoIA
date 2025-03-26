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
            ),
            node(
                func=nodes.log_loss_regLog,
                inputs=["regLog_model","dev_train", "dev_test"],
                outputs=None,
                tags=['log_loss']
            ),
            node(
                func=nodes.log_loss_decisionTree,
                inputs=["decisionTree_model","dev_train", "dev_test"],
                outputs=None,
                tags=['log_loss']
            )
        ]
    )
