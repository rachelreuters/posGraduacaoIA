import streamlit as st
import os


current_path = os.path.dirname(os.getcwd())

report_path = current_path+"/data/08_reporting/"

st.markdown("## Métricas e Análises do modelo ")

st.markdown("### Analisando os dados: ")

st.markdown("#### Correlação entre os dados de input: ")
st.markdown("Podemos ver que, logicamente, os dados de latitude e distância do arremesso tem correlação inversa porém alta. ")
correlation = report_path + "data_input_analysis/dev_train_correlation.png"
st.image(correlation, caption='Correlação Treino')

st.markdown("#### Balanceamento dos dados (Treino x Teste): ")
st.markdown("O balanceamento entre os dados de teste e treino foi bem próximo e perto dos 50%, o que é muito bom para treinar o modelo.")
correlation = report_path + "data_input_analysis/dev_train_test_balance.png"
st.image(correlation, caption='Balanceamento Y')

st.markdown("#### Distribuição dos dados utilizados no modelo: ")
st.markdown("Os dados não estão muito bem distribuídos e possuem diferentes métricas, o que provavelmente vai necessitar normalização.")
correlation = report_path + "data_input_analysis/dev_train_distribution.png"
st.image(correlation, caption='Distribuição Treino')
correlation = report_path + "data_input_analysis/dev_test_distribution.png"
st.image(correlation, caption='Distribuição Teste')

st.markdown("#### Dados de Lat e Lon X Acertou ou não a Cesta: ")
st.markdown("Os dados de latitude e longitude estão bem concentrados, podendo gerar overfit.")
correlation = report_path + "data_input_analysis/dev_train_lat_lon_shot_original.png"
st.image(correlation, caption='Lat e Lon Treino')
correlation = report_path + "data_input_analysis/dev_test_lat_lon_shot_original.png"
st.image(correlation, caption='Lat e Lon Teste')


st.markdown("### Analisando o treino do modelo: ")

st.markdown("#### Dados de Lat e Lon X Acertou (verde) ou não (vermelho) a Previsão: ")
st.markdown("A performance de ambos modelos foi bem parecida. ")
correlation = report_path + "model_train_report/dev_dt_lat_lon_shot_model_test.png"
st.image(correlation, caption='Lat e Lon Arvore de Decisao')
correlation = report_path + "model_train_report/dev_lr_lat_lon_shot_model_test.png"
st.image(correlation, caption='Lat e Lon Regressao Logistica')


st.markdown("#### Importância das variáveis utilizadas: ")
st.markdown("Em ambos modelos, podemos verificar que os dados de Latitude, Longitude e "
"Minutos Restantes foram os que mais interferiram no modelo. "
"Latitude e Longitude que a bola foi arremessada logicamente afeta a probabilidade de acerto."
"Os minutos restantes afetam razoavelmente, pois provavelmente o jogador fica com mais vontade de ganhar e aumentar sua"
"performance quando o jogo vai terminando. ")
correlation = report_path + "model_train_report/dev_model_feature_importance_dt.png"
st.image(correlation, caption='Importância das variáveis Arvore de Decisao')
correlation = report_path + "model_train_report/dev_model_feature_importance_lr.png"
st.image(correlation, caption='Importância das variáveis Regressao Logistica')


st.markdown("#### Curva ROC: ")
st.markdown("A performance de ambos modelos foi bem parecida. Porém muito baixa. "
"Em ambos, ao comparar uma instância positiva e uma negativa, o modelo tem 60% de chance de classificar corretamente. ")
correlation = report_path + "model_train_report/dev_roc_dt.png"
st.image(correlation, caption='ROC Arvore de Decisão')
correlation = report_path + "model_train_report/dev_roc_lr.png"
st.image(correlation, caption='ROC Regressao Logistica')

st.markdown("#### Métricas: ")
st.markdown("Focando no F1-Score, podemos ver que para a classificação de 'errar a cesta' o modelo obteve um bom resultado, acertando"
"69% das vezes. Porém, para a classificação de 'acertar a cesta' o modelo não conseguiu nenhum percentual.")
correlation = report_path + "model_train_report/dt_metrics.png"
st.image(correlation, caption='Metricas gerais da Arvore de Decisão')
correlation = report_path + "model_train_report/lr_metrics.png"
st.image(correlation, caption='Metricas gerais da Regressao Logistica')


st.markdown("### Testando o modelo escolhido (Regressão Logística) com dados de produção: ")

st.markdown("#### Dados de Lat e Lon X Acertou (verde) ou não (vermelho) a Previsão: ")
st.markdown("A performance do modelo foi um pouco abaixo do resultado de treino e teste. "
"Esses dados tem uma distribuição um pouco diferente da utilizada no treino do modelo,"
"o que pode significar que o modelo teve overfit.")
correlation = report_path + "model_prod_report/lat_lon_shot_prod.png"
st.image(correlation, caption='Lat e Lon Modelo Produção (Reg Log)')


st.markdown("#### Balanceamento do Y para os dados de produção: ")
st.markdown("Nesse conjunto de dados podemos ver um numero muito maior de arremessos não convertidos")
correlation = report_path + "model_prod_report/balance_Y_prod.png"
st.image(correlation, caption='Lat e Lon Modelo Produção (Reg Log)')


st.markdown("#### Curva ROC ")
st.markdown("Nesse conjunto de dados podemos ver que o modelo tem 56% de chance de acertar a classificação. ")
correlation = report_path + "model_prod_report/roc_curve_prod_server.png"
st.image(correlation, caption='ROC do Modelo de Produção')

st.markdown("#### Métricas: ")
st.markdown("Focando no F1-Score, podemos ver que para a classificação de 'errar a cesta' o modelo obteve um bom resultado, acertando"
" 80% das vezes. Porém, para a classificação de 'acertar a cesta' o modelo não conseguiu nenhum percentual.")
correlation = report_path + "model_prod_report/prod_metrics.png"
st.image(correlation, caption='Metricas gerais do Modelo de Produção')