from pycaret.classification import *
import pandas as pd
from sklearn.metrics import log_loss
import mlflow


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


def log_loss_regLog(model, dev_train, dev_test):
    X_train = dev_train[['lat','lon','minutes_remaining','period','playoffs','shot_distance']]
    X_test = dev_test[['lat','lon','minutes_remaining','period','playoffs','shot_distance']]
    Y_train = dev_train[['shot_made_flag']]
    Y_test = dev_test[['shot_made_flag']]

    model.fit(X_train, Y_train)

    y_pred_prob = model.predict_proba(X_test)

    log_loss_value = log_loss(Y_test, y_pred_prob)
    mlflow.set_tag("mlflow.runName", "metrics")

    mlflow.log_metric("log_loss_regLog", log_loss_value)

def log_loss_decisionTree(model, dev_train, dev_test):
    X_train = dev_train[['lat','lon','minutes_remaining','period','playoffs','shot_distance']]
    X_test = dev_test[['lat','lon','minutes_remaining','period','playoffs','shot_distance']]
    Y_train = dev_train[['shot_made_flag']]
    Y_test = dev_test[['shot_made_flag']]

    model.fit(X_train, Y_train)

    y_pred_prob = model.predict_proba(X_test)

    log_loss_value = log_loss(Y_test, y_pred_prob)

    mlflow.set_tag("mlflow.runName", "metrics")

    mlflow.log_metric("log_loss_decisionTree", log_loss_value)
