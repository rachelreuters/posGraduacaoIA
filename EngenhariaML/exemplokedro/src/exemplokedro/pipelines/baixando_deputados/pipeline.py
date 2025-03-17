from kedro.pipeline import Pipeline, node, pipeline

from . import nodes


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=nodes.baixar_deputados,
                inputs=[],
                outputs="deputados",
            ),
            node(
                func=nodes.sumarizar_por_partido,
                inputs=["deputados"],
                outputs="sumarizado",
            ),
        ]
    )
