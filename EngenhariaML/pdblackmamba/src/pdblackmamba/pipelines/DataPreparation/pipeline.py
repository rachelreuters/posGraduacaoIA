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
            ),
            node (
                func=nodes.plot_train_test_balance,
                inputs=["dev_train", "dev_test"],
                outputs=None,
                tags=["plots_train"]
            ),
            node(
                func=nodes.plot_distribution,
                inputs=["dev_train", "params:file_name_train_prefix"],
                outputs=None,
                tags=["plots_train"]
            ),
            node(
                func=nodes.plot_distribution,
                inputs=["dev_test", "params:file_name_test_prefix"],
                outputs=None,
                tags=["plots_train"]
            )
        ]
    )
