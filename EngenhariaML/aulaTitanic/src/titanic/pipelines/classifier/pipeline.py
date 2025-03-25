"""
This is a boilerplate pipeline 'classifier'
generated using Kedro 0.19.11
"""

from kedro.pipeline import node, Pipeline, pipeline  # noqa
from . import nodes


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            nodes.prepare_data,
            inputs=['raw_train'],
            outputs='train',
            tags=['preprocessamento']
        ),
    ])
