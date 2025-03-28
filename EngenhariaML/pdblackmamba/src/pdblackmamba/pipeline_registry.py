"""Project pipelines."""
from __future__ import annotations

from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline
from .pipelines.DataPreparation import create_pipeline as data_preparation
from .pipelines.ModelTrain import create_pipeline as model_train
from .pipelines.ModelEvaluationPickle import create_pipeline as model_evaluation_pickle
from .pipelines.ModelEvaluationServer import create_pipeline as model_evaluation_server

def register_pipelines() -> dict[str, Pipeline]:

    combined_pipeline = data_preparation() + model_train() + model_evaluation_server()

    return {
        "__default__": model_evaluation_server(),
    }

# def register_pipelines() -> dict[str, Pipeline]:
#     """Register the project's pipelines.

#     Returns:
#         A mapping from pipeline names to ``Pipeline`` objects.
#     """
#     pipelines = find_pipelines()
#     pipelines["__default__"] = sum(pipelines.values())
#     return pipelines

    
