import logging
from matplotlib.lines import Line2D
from pycaret.classification import *
import pandas as pd
import seaborn
from sklearn.metrics import classification_report, log_loss
import mlflow
import requests
import os
logger = logging.getLogger(__name__)
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score
import numpy as np
import matplotlib.image as mpimg

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

    mlflow.set_tag("mlflow.runName", "PipelineAplicacao")

    mlflow.log_metric(f"log_loss", log_loss_value)
    mlflow.log_metric(f"f1_score", f1_value)
    mlflow.log_metric(f"precision_score", precision_value)
    mlflow.log_metric(f"recall_score", recall_value)

    plt.figure(figsize=(8, 6))
    seaborn.heatmap(pd.DataFrame(performance_teste).iloc[:-1, :].T, annot=True, cmap="viridis")
    current_path = os.getcwd()
    fullpath=current_path + "/data/08_reporting/model_prod_report/prod_metrics.png"
    plt.savefig(fullpath, dpi=300, bbox_inches="tight")

    return result_df



def generate_roc_plot( Y_test, y_pred_prob ):
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
    fullpath=current_path + "/data/08_reporting/model_prod_report/roc_curve_prod_server.png"

    plt.savefig(fullpath, dpi=300, bbox_inches="tight")
    plt.close()  
    mlflow.set_tag("mlflow.runName", "PipelineAplicacao")
    
    mlflow.log_artifact(fullpath, artifact_path="Plots")
   


def lat_lon_plot_model_success(Y_test,y_pred, data: pd.DataFrame):

    lat= data['lat']
    lon= data['lon']
    color = ["green" if shot == y_pred[index] else "red" for index, shot in enumerate(Y_test.values.ravel())]

    fig, ax = plt.subplots(figsize=(10, 7))

    current_path = os.getcwd()

    plt.legend(loc="upper left", bbox_to_anchor=(1, 1)) 

    image = mpimg.imread(current_path+"/streamlit/lakers.gif")

    ax.imshow(image, extent=[-118.54, -118 ,33.2, 34.2], aspect='auto', alpha=0.9,zorder=5)  

    custom_legend = [
        Line2D([0], [0], marker="x", color="green", markerfacecolor="green", markersize=10, label="Y_raw == Y_predict"),
        Line2D([0], [0], marker="x", color="red", markerfacecolor="red", markersize=10, label="Y_raw != Y_predict")
    ]

    # Adicionar legenda ao gráfico
    plt.legend(handles=custom_legend, loc="lower right", title="Legenda",frameon=True, fancybox=True, framealpha=0.5) 


    ax.scatter(lon, lat,s=80, c=color,marker='x' ,alpha=1, label='Arremesso',zorder=10, linewidths=2)
    plt.ticklabel_format(style="plain", axis="both",useOffset=False)
    plt.title('Arremesso na quadra', fontsize=15)
    plt.xlabel('Lon')
    plt.ylabel('Lat')
   
    fullpath=current_path + f"/data/08_reporting/model_prod_report/lat_lon_shot_prod.png"

    plt.savefig(fullpath, dpi=300, bbox_inches="tight")
    plt.close()  

def plot_shot_balance(Y_test):

    plt.figure(figsize=(8, 6))
    new_labels = ['Not Shot', 'Shot']
    seaborn.countplot(x=Y_test.values.ravel())
    plt.xticks(ticks=[0,1], labels=new_labels) 
    plt.title("Production Data")
    plt.tight_layout()

    current_path = os.getcwd()
    fullpath=current_path + "/data/08_reporting/model_prod_report/balance_Y_prod.png"

    plt.savefig(fullpath, dpi=300, bbox_inches="tight")
    plt.close()  


def plot_distribution(data: pd.DataFrame ):

    input_columns = ['lat','lon','minutes_remaining','period','playoffs','shot_distance']

    plt.figure(figsize=(40, 20))

    for index, value in enumerate(input_columns):
        plt.subplot(4, 3,index+1)
        seaborn.histplot(data[value])
        plt.xlabel(input_columns[index])
        plt.tight_layout()

    current_path = os.getcwd()
    fullpath=current_path + f"/data/08_reporting/model_prod_report/prod_data_distribution.png"

    plt.savefig(fullpath, dpi=300, bbox_inches="tight")
    plt.close()  