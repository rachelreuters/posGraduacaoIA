from pycaret.classification import *
import pandas as pd
from sklearn.metrics import log_loss, f1_score
import mlflow


def model_train(data: pd.DataFrame,type_model,  mlflowExperiment: str):
    exp = ClassificationExperiment()
    exp.setup(data=data, target='shot_made_flag', session_id=22, log_experiment='mlflow', experiment_name=mlflowExperiment)

    model = exp.create_model(type_model)

    tuned = exp.tune_model(model, n_iter= 1000, optimize='F1')

    exp.get_metrics()

    return tuned


def get_metrics(model, dev_train, dev_test, model_type):
    X_train = dev_train[['lat','lon','minutes_remaining','period','playoffs','shot_distance']]
    X_test = dev_test[['lat','lon','minutes_remaining','period','playoffs','shot_distance']]
    Y_train = dev_train[['shot_made_flag']]
    Y_test = dev_test[['shot_made_flag']]

    model.fit(X_train, Y_train)

    y_pred_prob = model.predict_proba(X_test)
    y_pred = model.predict(X_test)

    log_loss_value = log_loss(Y_test, y_pred_prob)

    f1_value = f1_score(Y_test, y_pred)

    mlflow.set_tag("mlflow.runName", "metrics")

    mlflow.log_metric(f"log_loss_{model_type}", log_loss_value)
    mlflow.log_metric(f"f1_score_{model_type}", f1_value)


