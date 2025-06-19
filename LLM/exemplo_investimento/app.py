import streamlit as st
import pandas as pd

import pandas_ta as ta
import os
from dotenv import load_dotenv


from langchain_google_genai import ChatGoogleGenerativeAI
import asyncio

from agent import Agent

# --- CONFIGURAÇÃO INICIAL E DE SEGURANÇA ---

# Carrega a chave de API do arquivo .env
load_dotenv()
API_KEY = os.getenv("API_GOOGLE")

# Solução para o loop de eventos assíncronos no Streamlit
try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

st.set_page_config(layout="wide", page_title="Screener Técnico da B3")


# --- INTERFACE DO STREAMLIT ---

st.title("🤖 Screener Técnico de Setores da B3")
st.markdown("Uma ferramenta analítica para filtrar ações com base em indicadores técnicos.")

st.warning("**Aviso Legal:** Esta ferramenta é para fins educacionais e de estudo. As informações aqui apresentadas **não constituem recomendação de investimento**.")

# Inputs do usuário
col1, col2 = st.columns(2)
with col1:
    setor_selecionado = st.selectbox(
        "Escolha um setor para analisar:",
        ("Bancos", "Varejo", "Energia Elétrica", "Mineração")
    )
with col2:
    indicador_selecionado = st.selectbox(
        "Escolha um indicador técnico:",
        ("IFR",) # Por enquanto, só implementamos o IFR
    )

if st.button(f"Analisar Setor '{setor_selecionado}' com Indicador '{indicador_selecionado}'"):
    # Prompt que instrui o agente sobre seu objetivo final
    prompt = f"""
    Seu objetivo é criar um ranking de ações para o setor '{setor_selecionado}' com base no indicador '{indicador_selecionado}'.
    Siga estes passos:
    1. Obtenha a lista de tickers para o setor '{setor_selecionado}'.
    2. Para cada ticker na lista, calcule o indicador '{indicador_selecionado}' usando a ferramenta apropriada.
    3. Apresente os resultados em uma tabela Markdown, ordenada do menor para o maior valor do indicador.
    4. Após a tabela, escreva uma análise educacional sobre o que é o indicador '{indicador_selecionado}'.
    """
    
    with st.spinner("O Agente está trabalhando... Buscando dados e analisando..."):
        try:
            # Executa o agente com o prompt
            agent = Agent(google_api_key=API_KEY)
            response = agent.get_tips_investing(prompt)
            st.markdown(response["output"])
        except Exception as e:
            st.error(f"Ocorreu um erro durante a execução do agente: {e}")