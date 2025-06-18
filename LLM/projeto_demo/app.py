import asyncio
import re
import streamlit as st 
from agent import Agent

import folium
from streamlit_folium import st_folium
import logging
import json
from dotenv import load_dotenv
import os
import numpy as np

# --- CONFIGURAÇÃO INICIAL (sem alterações) ---
load_dotenv()
try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
API_KEY = os.getenv("API_GOOGLE")
if not API_KEY:
    st.error("Variável de ambiente API_GOOGLE não definida.")
    st.stop()
LOGGER = logging.getLogger(__name__)
st.set_page_config(layout="wide")

# --- INICIALIZAÇÃO DO ESTADO ---
# 1. Inicialize as variáveis de estado para os pontos E para o roteiro
if "points" not in st.session_state:
    st.session_state.points = []
if "itinerary" not in st.session_state:
    # Mensagem inicial que aparecerá no container
    st.session_state.itinerary = "Seu roteiro aparecerá aqui."

# --- DASHBOARD ---
st.title("Bem-vindo ao Agente de Turismo!")
st.write("Este aplicativo irá ajudá-lo a planejar suas viagens com dicas e sugestões detalhadas.")

agent = Agent(API_KEY)

col1, col2 = st.columns(2)

with col1:
    request = st.text_area("Para onde você gostaria de viajar? Descreva seu pedido em português.")
    button = st.button("Obter Dicas de Viagem")
    
    box = st.container(height=300, border=True)
    with box:
        container = st.empty()
        # 3. O container agora SEMPRE exibe o que está salvo no session_state
        container.write(st.session_state.itinerary)

if button and request:
    itinerary = agent.get_tips(request)
    
    # 2. ATUALIZE o session_state com o novo roteiro quando o botão for clicado
    try:
        st.session_state.itinerary = itinerary["itinerary"]
    except (KeyError, TypeError):
        st.session_state.itinerary = "Desculpe, não consegui gerar um roteiro para o seu pedido. Tente novamente."

    # Processamento de coordenadas (lógica permanece a mesma)
    try:
        coordinates_str = itinerary["coordinates"]
        coordinates_str = re.sub(r"^\s*```json\s*|```\s*$", "", coordinates_str, flags=re.MULTILINE).strip()
        days = json.loads(coordinates_str)
        
        new_points = []
        for day in days.get("days", []):
            for loc in day.get("locations", []):
                if isinstance(loc.get("lat"), (int, float)) and isinstance(loc.get("lon"), (int, float)):
                    new_points.append([loc["lat"], loc["lon"]])
        
        st.session_state.points = new_points
        
    except (KeyError, TypeError, json.JSONDecodeError) as e:
        LOGGER.warning(f"Não foram encontradas coordenadas ou houve erro no JSON: {e}")
        st.session_state.points = []

    # Re-executa o script para atualizar a tela com os novos dados
    st.rerun()

# A lógica do mapa na col2 permanece a mesma, pois ela já lê do session_state
with col2:
    st.header("Mapa do Roteiro")
    map_center = [-14.2350, -51.9253] # Centro do Brasil
    zoom_start = 4

    if st.session_state.points:
        map_center = np.mean(st.session_state.points, axis=0).tolist()
        zoom_start = 12
    
    folium_map = folium.Map(location=map_center, zoom_start=zoom_start)

    for point in st.session_state.points:
        folium.Marker(location=point).add_to(folium_map)

    st_folium(folium_map, width=725, height=500, key="mapa") # Adicionar uma chave é uma boa prática