import logging
from pycaret.classification import *
import pandas as pd
from sklearn.metrics import classification_report, log_loss
import mlflow
import requests
import os
logger = logging.getLogger(__name__)
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score
import numpy as np


def prepare_Y_X_prod(data: pd.DataFrame):
    data_filtered = data.dropna()

    X_test = data_filtered[['lat','lon','minutes_remaining','period','playoffs','shot_distance']]
    Y_test = data_filtered[['shot_made_flag']]

    return X_test, Y_test

def model_prod(X_test):

    response = requests.post('http://127.0.0.1:5001/invocations', json= {'inputs': X_test.values.tolist() }  )

    predict = response.json()

    y_pred = predict['predictions']

    model_uri = "models:/kobe_lr_model_prod/latest"  # Replace with model name and version

    # Load the model
    model = mlflow.sklearn.load_model(model_uri)

    y_pred_prob = model.predict_proba(X_test)

    return y_pred, y_pred_prob
    

def generate_main_metrics(X_test, Y_test, y_pred, y_pred_prob ):

    log_loss_value = log_loss(Y_test, y_pred_prob)

    performance_teste = classification_report(Y_test, y_pred, output_dict=True)
    
    f1_value = performance_teste['macro avg']['f1-score']
    precision_value = performance_teste['macro avg']['precision']
    recall_value = performance_teste['macro avg']['recall']


    predictions_df = pd.DataFrame({
        "Actual": Y_test.values.ravel(),
        "Predicted": y_pred
    }, index=X_test.index)

    result_df = pd.concat([X_test, predictions_df], axis=1)

    mlflow.set_tag("mlflow.runName", "metrics_prod_server")

    mlflow.log_metric(f"log_loss", log_loss_value)
    mlflow.log_metric(f"f1_score", f1_value)
    mlflow.log_metric(f"precision_score", precision_value)
    mlflow.log_metric(f"recall_score", recall_value)
        
    return result_df



def generate_roc_plot( Y_test, y_pred_prob ):
    fpr, tpr, thresholds = roc_curve(Y_test, [c[1] for c in y_pred_prob] )
    auc_score = roc_auc_score(Y_test, [c[1] for c in y_pred_prob])
    print(f"AUC Score: {auc_score}")

    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color="blue", label=f"ROC Curve (AUC = {auc_score:.2f})")
    plt.plot([0, 1], [0, 1], color="gray", linestyle="--")  # Diagonal line
    plt.xlabel("False Positive Rate (FPR)")
    plt.ylabel("True Positive Rate (TPR)")
    plt.title("Receiver Operating Characteristic (ROC) Curve")
    plt.legend()
    plt.grid()
    current_path = os.getcwd()
    fullpath=current_path + "/data/08_reporting/roc_curve_prod_server.png"

    plt.savefig(fullpath, dpi=300, bbox_inches="tight")
    plt.close()  
    mlflow.set_tag("mlflow.runName", "metrics_prod_server")
    
    mlflow.log_artifact(fullpath, artifact_path="Plots")
   

def feature_importance_plot(X_test):

    feature_names = ['lat','lon','minutes_remaining','period','playoffs','shot_distance']

    model_uri = "models:/kobe_lr_model_prod/latest"  # Replace with model name and version

    # Load the model
    model = mlflow.sklearn.load_model(model_uri)

    coefficients = model.coef_[0]  
    feature_importance = pd.DataFrame({
        "Feature": feature_names,
        "Importance": coefficients
    })
    feature_importance["Absolute Importance"] = np.abs(feature_importance["Importance"])
    feature_importance = feature_importance.sort_values(by="Absolute Importance", ascending=False)

    # Display feature importance
    print(feature_importance)

    plt.barh(y=feature_names, width=feature_importance['Importance'].values)

    current_path = os.getcwd()
    fullpath=current_path + "/data/08_reporting/feature_importance_prod_server.png"

    plt.savefig(fullpath, dpi=300, bbox_inches="tight")

    mlflow.set_tag("mlflow.runName", "metrics_prod_server")
    
    mlflow.log_artifact(fullpath, artifact_path="Plots")

