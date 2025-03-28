from kedro.pipeline import Pipeline, node, pipeline

from . import nodes


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=nodes.download_raw_dev,
                inputs=[],
                outputs="raw_dev",
            ),
            node(
                func=nodes.download_raw_prod,
                inputs=[],
                outputs="raw_prod",
            ),
            node(
                func=nodes.filter_raw_dataset,
                inputs=["raw_dev"],
                outputs="dev_filtered",
            ),
            node(
                func=nodes.split_train_test,
                inputs=["dev_filtered", "params:mlflow_experiment"],
                outputs=["dev_train", "dev_test"],
            )
        ]
    )
