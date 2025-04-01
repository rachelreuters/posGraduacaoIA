import pandas as pd
import requests
from io import BytesIO
import logging
from sklearn.model_selection import train_test_split
import mlflow
import matplotlib.pyplot as plt
import seaborn 
import os

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

'''
A separacao dos dados de teste e treino e fundamental e afeta diretamente a capacidade do modelo de generalizar para novos dados
Representatividade:
Se os dados de treino não representam bem o problema, o modelo pode aprender de maneira enviesada ou limitada.
Se o conjunto de teste não é representativo, a avaliação do modelo será imprecisa.

Overfitting e Underfitting:
Dados de treino muito grandes e teste muito pequenos podem levar a overfitting, pois o modelo será testado em um conjunto limitado de dados.
Por outro lado, treinar com poucos dados pode causar underfitting, já que o modelo não terá aprendido padrões suficientes.

Viés e Variância:
Um conjunto de treino ou teste mal balanceado (como uma classe com mais exemplos que outras) pode induzir viés nos resultados.'
'''
def split_train_test(data: pd.DataFrame, mlflowExperiment: str):
    mlflow.set_experiment(mlflowExperiment)
    y = data[['shot_made_flag']]
    data_train, data_test =  train_test_split(data, test_size=0.2, stratify=y, random_state=22)
    mlflow.set_tag("mlflow.runName", "metrics")
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
    fullpath=current_path + "/data/08_reporting/dev_train_test_balance.png"

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
    fullpath=current_path + f"/data/08_reporting/{file_name}_distribution.png"

    plt.savefig(fullpath, dpi=300, bbox_inches="tight")
    plt.close()  