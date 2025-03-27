from kedro.pipeline import Pipeline, node, pipeline

from . import nodes


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=nodes.model_prod,
                inputs=["raw_prod","regLog_model"],
                outputs="metric_prod",
            ),
        ]
    )
