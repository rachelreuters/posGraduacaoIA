**Rachel Reuters - Engenharia de Machine Learning [25E1_3]**

Link pra o git:  [posGraduacaoIA/EngenhariaML/pdblackmamba at main · rachelreuters/posGraduacaoIA](https://github.com/rachelreuters/posGraduacaoIA/tree/main/EngenhariaML/pdblackmamba)


[TOC]


# Diagrama

![Alt Text](docs/source/DiagramaProjeto.png)

# Estrutua de arquivos

![alt text](docs/source/ArquiteturaPastas.png)

# Descrição dos artefatos
 - 01_raw
   - dataset_kobe_dev.parquet : Arquivo original para teste e treino do modelo 
   - dataset_kobe_prod.parquet : Arquivo original para avaliação do modelo em produção
 - 03_primary
   - data_filtered.parquet: Dataset de dev filtrado para treino e teste do modelo, nesse dataset foram removidos os nulos e selecionado as que irão ser utilizadas como teste e treino. Colunas : 'lat','lon','minutes_remaining','period','playoffs','shot_distance', 'shot_made_flag' 
 - 05_model_input
   - base_test.parquet : Dataset gerado depois de separar 80/20 o dataset de dev filtrado para testar o modelo.
   - base_train.parquet: Dataset gerado depois de separar 80/20 o dataset de dev filtrado para treinar o modelo.
   - x_prod.pkl : Arquivo pickle que representa o dado de producao ja filtrado e que sera utilizado como input do modelo para avaliacao em producao. 
   - y_prod.pkl: Arquivo pickle que representa o dado de producao ja filtrado e que sera utilizado para avaliar os resultados do modelo comparando com os outputs de predicao
 - 07_model_output
   - predict_prod_server.parquet: Resultado das metricas do modelo depois da avaliacao dos dados de producao comparando a predicao com os Y original. 
   - y_pred_prod.pkl: Resultado da predicao do modelo utilizando os dados de producao como entrada.
   - y_prob_prod.pkl: Resultado das probabilidades do modelo utilizando os dados de producao como entrada.
 - 08_reporting
   - data_input_analysis
     - dev_test_correlation.png: Correlacao dos dados de input do grupo de teste do dataset de dev. 
     - dev_test_distribution.png: Distribuicao dos dados de input do grupo de teste do dataset de dev. 
     - dev_test_lat_lon_shot_original.png: Plot da latitude e longitude com o shot_made_flag (Y) do grupo de teste do dataset de dev.
     - dev_train_correlation.png: Correlacao dos dados de input do grupo de treino do dataset de dev. 
     - dev_train_distribution.png: Distribuicao dos dados de input do grupo de treino do dataset de dev. 
     - dev_train_lat_lon_shot_original.png: Plot da latitude e longitude com o shot_made_flag (Y) do grupo de treino do dataset de dev.
     - dev_train_test_balance.png: Balanceamento do Y (shot_made_flag) comparando os dados de trein e teste do dataset de dev. 
   - model_prod_report
     - balance_Y_prod.png
     - lat_lon_shot_prod.png
     - prod_metrics.png
     - roc_curve_prod_server.png
   - model_train_report
     - dev_dt_lat_lon_shot_model_test.png
     - dev_lr_lat_lon_shot_model_test.png
     - dev_model_feature_importance_dt.png
     - dev_model_feature_importance_lr.png
     - dev_roc_dt.png
     - dev_roc_lr.png
     - dt_metrics.png
     - lr_metrics.png
 - Metricas no MLFLOW:
   - metrics_prod_server
     - f1_score
     - log_loss
     - precision_score
     - recall_score
   - metrics_dev
     - f1_score_dt_test
     - f1_score_lr_test
     - log_loss_dt_test
     - log_loss_lr_test
     - test_size
     - train_size
 - Parametros no MLFLOW:
   - file_name_test_prefix
   - file_name_train_prefix
   - mlflow_experiment
   - model_dt
   - model_regLog
   - percent_test
 - Pipelines
   - DataPreparation
   - ModelEvaluation
   - ModelTrain

# Rubricas e Perguntas Teóricas :


# HOW TO:
## Requisitos:
Versão do Python que foi criado o projeto: **Python 3.11**
Sistema operacional:  **Windows 11**
Gerenciador de pacotes do Python:  **conda** 

## Comandos:

Comandos para iniciar o ambiente virtual:

    conda create --name py11_kedro python=3.11    
    conda activate py11_kedro  

Instalar os pacotes:

    pip install -r requirements.txt

Para preparar os dados e treinar o modelo:

    kedro run

Apos o treinamento, verificar os plots e metricas resultantes dos treinamentos. Utilizando o mlflow :

    mlflow ui 

Com isso escolhe-se o melhor modelo (nesse caso a regressao logistica) , e serve ele utilizando o mlflow:

    mlflow models serve ^
        -m models:/kobe_lr_model_prod/latest ^
        --env-manager=local ^
        --port 5001


Para gerar as metricas encima dos dados de producao, acessando o modelo servido pelo Mlflow (escolhido anteriormente):

    kedro run --pipeline model_evaluation_server


Para acessar o formulário em streamlit para testar o modelo em produção  e verificar as inferências do modelo, entrar na pasta do streamlit e executar o comando:

    streamlit run main.py



