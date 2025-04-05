from matplotlib.patches import Rectangle
import pandas as pd
import requests
from io import BytesIO
import logging
from sklearn.model_selection import train_test_split
import mlflow
import matplotlib.pyplot as plt
import seaborn 
import os
import matplotlib.image as mpimg


logger = logging.getLogger(__name__)

def download_raw_dev() -> pd.DataFrame:
    resp = requests.get("https://github.com/tciodaro/eng_ml/blob/main/data/dataset_kobe_dev.parquet?raw=true")
    file_like_object = BytesIO(resp.content)
    df = pd.read_parquet(file_like_object)
    return df

def download_raw_prod() -> pd.DataFrame:
    resp = requests.get("https://github.com/tciodaro/eng_ml/blob/main/data/dataset_kobe_prod.parquet?raw=true")
    file_like_object = BytesIO(resp.content)
    df = pd.read_parquet(file_like_object)
    return df


def filter_raw_dataset(data: pd.DataFrame) -> pd.DataFrame:
    filtered =  data.dropna()[['lat','lon','minutes_remaining','period','playoffs','shot_distance', 'shot_made_flag']]
    logger.info(f"Dimensoes do dataset filtrado: {filtered.shape} ")
    return filtered


def split_train_test(data: pd.DataFrame, mlflowExperiment: str):
    mlflow.set_experiment(mlflowExperiment)
    y = data[['shot_made_flag']]
    data_train, data_test =  train_test_split(data, test_size=0.2, stratify=y, random_state=22)
    mlflow.set_tag("mlflow.runName", "metrics_dev")
    mlflow.log_param("percent_test", 20)
    train_size = len(data_train)
    test_size_actual = len(data_test)
    mlflow.log_metric("train_size", train_size)
    mlflow.log_metric("test_size", test_size_actual)

    return data_train, data_test


def plot_train_test_balance(trainData: pd.DataFrame, testData: pd.DataFrame):

    new_labels = ['Not Shot', 'Shot']
    fig, axes = plt.subplots(1, 2, figsize=(20, 10))  
    seaborn.countplot(x=trainData["shot_made_flag"], ax=axes[0])
    axes[0].set_xticklabels(new_labels)
    axes[0].set_title("Train Data")

    seaborn.countplot(x=testData["shot_made_flag"], ax=axes[1])
    axes[1].set_xticklabels(new_labels)
    axes[1].set_title("Test Data")

    plt.tight_layout()

    current_path = os.getcwd()
    fullpath=current_path + "/data/08_reporting/data_input_analysis/dev_train_test_balance.png"

    plt.savefig(fullpath, dpi=300, bbox_inches="tight")
    plt.close()  

def plot_distribution(data: pd.DataFrame, file_name ):

    input_columns = ['lat','lon','minutes_remaining','period','playoffs','shot_distance']

    plt.figure(figsize=(40, 20))

    for index, value in enumerate(input_columns):
        plt.subplot(4, 3,index+1)
        seaborn.histplot(data[value])
        plt.xlabel(input_columns[index])
        plt.tight_layout()

    current_path = os.getcwd()
    fullpath=current_path + f"/data/08_reporting/data_input_analysis/dev_{file_name}_distribution.png"

    plt.savefig(fullpath, dpi=300, bbox_inches="tight")
    plt.close()  

def plot_correlation(data: pd.DataFrame, file_name ):
    corr_matrix = data.corr()

    plt.figure(figsize=(8, 6))
    seaborn.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title("Heatmap de Correlação")
    current_path = os.getcwd()
    fullpath=current_path + f"/data/08_reporting/data_input_analysis/dev_{file_name}_correlation.png"

    plt.savefig(fullpath, dpi=300, bbox_inches="tight")
    plt.close()  


def plot_shot_areas(data: pd.DataFrame, file_name):

    lat= data['lat']
    lon= data['lon']
    shots = data['shot_made_flag']

    color = ["green" if shot == 1 else "red" for shot in shots]

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
   
    fullpath=current_path + f"/data/08_reporting/data_input_analysis/dev_{file_name}_lat_lon_shot_original.png"

    plt.savefig(fullpath, dpi=300, bbox_inches="tight")
    plt.close()  