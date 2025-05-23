import logging
from pycaret.classification import *
import pandas as pd
import seaborn
from sklearn.metrics import classification_report, log_loss,  roc_auc_score, roc_curve
import mlflow
import matplotlib.pyplot as plt
import os
import numpy as np
import matplotlib.image as mpimg

logger = logging.getLogger(__name__)

def model_train(data: pd.DataFrame,type_model,  mlflowExperiment: str):
        mlflow.set_tag("mlflow.runName", "Treinamento")        
        exp = ClassificationExperiment()
        exp.setup(data=data, 
                target='shot_made_flag', 
                session_id=22, 
                log_experiment='mlflow', 
                experiment_name=mlflowExperiment,
                normalize=True,
                normalize_method="robust",         
                experiment_custom_tags={"mlflow.runName": f"Treinamento_{type_model}"}  
                )
        
        exp.add_metric(
            id="log_loss",
            name="Log Loss",
            score_func=log_loss,
            greater_is_better=False  
        )

        model = exp.create_model(type_model)

        tuned = exp.tune_model(model, n_iter= 3, optimize='F1', )

        exp.get_metrics()

        return tuned


def get_metrics(model, dev_train, dev_test, model_type):
    X_train = dev_train[['lat','lon','minutes_remaining','period','playoffs','shot_distance']]
    X_test = dev_test[['lat','lon','minutes_remaining','period','playoffs','shot_distance']]
    Y_train = dev_train[['shot_made_flag']]
    Y_test = dev_test[['shot_made_flag']]

    y_pred_prob = model.predict_proba(X_test)
    y_pred = model.predict(X_test)

    performance_teste = classification_report(Y_test, y_pred, output_dict=True)

    log_loss_value = log_loss(Y_test, y_pred_prob)

    f1_value = performance_teste['macro avg']['f1-score']
    mlflow.log_metric(f"log_loss_{model_type}_test", log_loss_value)
    mlflow.log_metric(f"f1_score_{model_type}_test", f1_value)

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
    fullpath=current_path + f"/data/08_reporting/model_train_report/dev_roc_{model_type}.png"

    plt.figure(figsize=(8, 6))
    seaborn.heatmap(pd.DataFrame(performance_teste).iloc[:-1, :].T, annot=True, cmap="viridis")
    current_path = os.getcwd()
    fullpath=current_path + f"/data/08_reporting/model_train_report/{model_type}_metrics.png"

    plt.savefig(fullpath, dpi=300, bbox_inches="tight")

    plt.savefig(fullpath, dpi=300, bbox_inches="tight")
    plt.close()      
    mlflow.log_artifact(fullpath, artifact_path="Plots")


def lat_lon_plot_model_success(model, data: pd.DataFrame, model_type):
    X_test = data[['lat','lon','minutes_remaining','period','playoffs','shot_distance']]
    Y_test = data['shot_made_flag']

    y_pred = model.predict(X_test)

    lat= data['lat']
    lon= data['lon']
    color = ["green" if shot == y_pred[index] else "red" for index, shot in enumerate(Y_test)]

    fig, ax = plt.subplots(figsize=(10, 7))

    current_path = os.getcwd()

    plt.legend(loc="upper left", bbox_to_anchor=(1, 1)) 

    image = mpimg.imread(current_path+"/streamlit/lakers.gif")

    ax.imshow(image, extent=[-118.54, -118 ,33.2, 34.2], aspect='auto', alpha=0.9,zorder=9)    

    ax.scatter(lon, lat,s=80, c=color,marker='x' ,alpha=1, label='Arremesso',zorder=10, linewidths=2)
    plt.ticklabel_format(style="plain", axis="both",useOffset=False)
    plt.title('Arremesso na quadra', fontsize=15)
    plt.xlabel('Lon')
    plt.ylabel('Lat')

    fullpath=current_path + f"/data/08_reporting/model_train_report/dev_{model_type}_lat_lon_shot_model_test.png"

    plt.savefig(fullpath, dpi=300, bbox_inches="tight")
    plt.close()  



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
    fullpath=current_path + f"/data/08_reporting/model_train_report/dev_model_feature_importance_{model_type}.png"

    plt.savefig(fullpath, dpi=300, bbox_inches="tight")

    mlflow.log_artifact(fullpath, artifact_path="Plots")





    