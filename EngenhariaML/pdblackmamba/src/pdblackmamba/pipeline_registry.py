"""Project pipelines."""
from __future__ import annotations

from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline
from .pipelines.DataPreparation import create_pipeline as data_preparation
from .pipelines.ModelTrain import create_pipeline as model_train
from .pipelines.ModelEvaluationPickle import create_pipeline as model_evaluation_pickle
from .pipelines.ModelEvaluationServer import create_pipeline as model_evaluation_server

def register_pipelines() -> dict[str, Pipeline]:

    pipelines = {
        "data_preparation": data_preparation(),
        "model_train": model_train(),
        "model_evaluation_server": model_evaluation_server(),
        "__default__": data_preparation()+model_train()
    }
    
    return pipelines


    
