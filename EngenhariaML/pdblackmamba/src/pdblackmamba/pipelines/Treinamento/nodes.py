from pycaret.classification import *
import pandas as pd


def model_train_regLog(data: pd.DataFrame, mlflowExperiment: str):
    exp = ClassificationExperiment()
    exp.setup(data=data, target='shot_made_flag', session_id=22, log_experiment='mlflow', experiment_name=mlflowExperiment)

    model_lr = exp.create_model('lr')

    tuned = exp.tune_model(model_lr, n_iter= 1000, optimize='F1')

    exp.get_metrics()

    return tuned


def model_train_decisionTree(data: pd.DataFrame, mlflowExperiment: str):
    exp = ClassificationExperiment()
    exp.setup(data=data, target='shot_made_flag', session_id=22, log_experiment='mlflow', experiment_name=mlflowExperiment)

    model_dt = exp.create_model('dt')

    tuned = exp.tune_model(model_dt, n_iter= 1000, optimize='F1')

    exp.get_metrics()

    return tuned