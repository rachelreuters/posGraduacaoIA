import logging
from pycaret.classification import *
import pandas as pd
from sklearn.metrics import log_loss, f1_score, roc_auc_score, roc_curve
import mlflow
import matplotlib.pyplot as plt
import os
import numpy as np

logger = logging.getLogger(__name__)



def model_train(data: pd.DataFrame,type_model,  mlflowExperiment: str):
    exp = ClassificationExperiment()
    exp.setup(data=data, 
              target='shot_made_flag', 
              session_id=22, 
              log_experiment='mlflow', 
              experiment_name=mlflowExperiment,
              normalize=True,
              normalize_method="robust",
              system_log=False,
              verbose=False,               
              )
    
    exp.add_metric(
        id="log_loss",
        name="Log Loss",
        score_func=log_loss,
        greater_is_better=False  
    )

    model = exp.create_model(type_model)

    tuned = exp.tune_model(model, n_iter= 100, optimize='F1',
                           verbose= False, tuner_verbose=False)

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

    mlflow.set_tag("mlflow.runName", "metrics_dev")

    mlflow.log_metric(f"log_loss_{model_type}", log_loss_value)
    mlflow.log_metric(f"f1_score_{model_type}", f1_value)

    fpr, tpr, thresholds = roc_curve(Y_test, [c[1] for c in y_pred_prob] )
    auc_score = roc_auc_score(Y_test, [c[1] for c in y_pred_prob])
    print(f"AUC Score: {auc_score}")

    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color="blue", label=f"ROC Curve (AUC = {auc_score:.2f})")
    plt.plot([0, 1], [0, 1], color="gray", linestyle="--")
    plt.xlabel("False Positive Rate (FPR)")
    plt.ylabel("True Positive Rate (TPR)")
    plt.title("Receiver Operating Characteristic (ROC) Curve")
    plt.legend()
    plt.grid()
    current_path = os.getcwd()
    fullpath=current_path + f"/data/08_reporting/dev_roc_{model_type}.png"

    plt.savefig(fullpath, dpi=300, bbox_inches="tight")
    plt.close()  
    mlflow.set_tag("mlflow.runName", "metrics_dev")
    
    mlflow.log_artifact(fullpath, artifact_path="Plots")


def feature_importance_plot(model, model_type):

    feature_names = ['lat','lon','minutes_remaining','period','playoffs','shot_distance']

    coefficients = model.coef_[0]  
    feature_importance = pd.DataFrame({
        "Feature": feature_names,
        "Importance": coefficients
    })
    feature_importance["Absolute Importance"] = np.abs(feature_importance["Importance"])
    feature_importance = feature_importance.sort_values(by="Absolute Importance", ascending=False)

    plt.barh(y=feature_names, width=feature_importance['Importance'].values)

    current_path = os.getcwd()
    fullpath=current_path + f"/data/08_reporting/dev_model_feature_importance_{model_type}.png"

    plt.savefig(fullpath, dpi=300, bbox_inches="tight")

    mlflow.set_tag("mlflow.runName", "metrics_dev")
    
    mlflow.log_artifact(fullpath, artifact_path="Plots")


    