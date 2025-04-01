from kedro.pipeline import Pipeline, node, pipeline

from . import nodes


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=nodes.model_train,
                inputs=["dev_train","params:model_regLog","params:mlflow_experiment"],
                outputs="regLog_model",
            ),
            node(
                func=nodes.model_train,
                inputs=["dev_train","params:model_dt","params:mlflow_experiment"],
                outputs="decisionTree_model",
            ),
            node(
                func=nodes.get_metrics,
                inputs=["regLog_model","dev_train", "dev_test", "params:model_regLog"],
                outputs=None,
                tags=['metrics_train_model']
            ),
            node(
                func=nodes.get_metrics,
                inputs=["decisionTree_model","dev_train", "dev_test","params:model_dt" ],
                outputs=None,
                tags=['metrics_train_model']
            ),
            node(
                func=nodes.feature_importance_plot,
                inputs=["regLog_model", "params:model_regLog"],
                outputs=None,
                tags=['metrics_train_model'],            
            ),
            node(
                func=nodes.feature_importance_plot,
                inputs=["decisionTree_model", "params:model_dt"],
                outputs=None,
                tags=['metrics_train_model'],            
            )
        ]
    )
