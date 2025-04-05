**Rachel Reuters - Engenharia de Machine Learning [25E1_3]**

Link pra o git:  [posGraduacaoIA/EngenhariaML/pdblackmamba at main · rachelreuters/posGraduacaoIA](https://github.com/rachelreuters/posGraduacaoIA/tree/main/EngenhariaML/pdblackmamba)


[TOC]


# Diagrama

![Diagrama](docs/source/DiagramaProjeto.png)

# Estrutua dos arquivos

![Arquivos](docs/source/ArquiteturaPastas.png)

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
     - balance_Y_prod.png: Balanceamento do Y para o dataset de producao
     - lat_lon_shot_prod.png: Plot da latitude e longitude X modelo acertou ou errou
     - prod_metrics.png: Metricas do modelo com os dados de producao.
     - roc_curve_prod_server.png
   - model_train_report
     - dev_dt_lat_lon_shot_model_test.png : Plot da latitude e longitude X modelo acertou ou errou para o grupo de teste (modelo de arvore de decisao)
     - dev_lr_lat_lon_shot_model_test.png : Plot da latitude e longitude X modelo acertou ou errou para o grupo de teste (modelo de regressao logistica)
     - dev_model_feature_importance_dt.png : Importancia de features para o modelo de arvore de decisao 
     - dev_model_feature_importance_lr.png: Importancia de features para o modelo de regressao logistica
     - dev_roc_dt.png: Curva roc para o modelo de arvore de decisao no grupo de teste.
     - dev_roc_lr.png: Curva roc para o modelo de regressao logistica no grupo de teste.
     - dt_metrics.png: Metricas finais para o modelo de arvore de decisao.
     - lr_metrics.png: Metricas finais para o modelo de regressao logistica.
 - Metricas no MLFLOW:
   - metrics_prod_server
     - f1_score: f1_score no modelo para o dataset de producao
     - log_loss: log_loss no modelo para o dataset de producao
     - precision_score: Precisao no modelo para o dataset de producao
     - recall_score: Recall no modelo para o dataset de producao
   - metrics_dev
     - f1_score_dt_test: f1 score para a arvore de decisao para o grupo de teste
     - f1_score_lr_test: f1 score para a regressao logistica para o grupo de teste
     - log_loss_dt_test: log_loss para a arvore de decisao para o grupo de teste
     - log_loss_lr_test: log_loss para a regressao logistica para o grupo de teste
     - test_size: tamanho do dataset de teste depois de dividir em treino e teste (80/20)
     - train_size: tamanho do dataset de treino depois de dividir em treino e teste (80/20)
 - Parametros no MLFLOW:
   - file_name_test_prefix
   - file_name_train_prefix
   - mlflow_experiment
   - model_dt
   - model_regLog
   - percent_test
 - Pipelines
   - DataPreparation: Essa etapa é responsável por preparar os dados para serem usados para treinar o modelo. Retirar nulos, separar dados de treino e teste, gerar métricas relativas aos dados iniciais. 
   - ModelEvaluation: Essa etapa é responsável por executar predição do modelo em dados de produção e com isso gerando métricas. 
   - ModelTrain:  Essa etapa é responsável por realizar treinos dos modelos, comparar modelos, gerar métricas, gerar plots dos relativos testes e treinos. 
 - Páginas do Streamlit:
   - main.py: Página inicial para redirecionar para as demais páginas.
   - Analise.py : Reune todos os resultados e análises dos modelos.
   - Inferencia.py: Input de dados de formulário para teste do modelo servido em produção pelo MLFlow.
  
# Respostas do Projeto de Disciplina e Rubricas explicadas :
## PD:
- Como as ferramentas Streamlit, MLFlow, PyCaret e Scikit-Learn auxiliam na construção dos pipelines descritos anteriormente? 
RESPOSTA
-  Explique como a escolha de treino e teste afetam o resultado do modelo final. Quais estratégias ajudam a minimizar os efeitos de viés de dados.
RESPOSTA 
-Registre os parâmetros (% teste) e métricas (tamanho de cada base) no MlFlow
![MetricasModeloDev](docs/source/MetricasMlflowDev.png)
-Implementar o pipeline de treinamento do modelo 


## Rubricas:

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



