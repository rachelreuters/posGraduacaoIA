import re
import streamlit as st
import os
from dotenv import load_dotenv
import asyncio
import json
import pandas as pd

from agent import Agent

# --- CONFIGURAÇÃO INICIAL ---
load_dotenv()
API_KEY = os.getenv("API_GOOGLE")

# Solução para o loop de eventos assíncronos no Streamlit
try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

st.set_page_config(layout="wide", page_title="Explorador Olfativo")

st.title("Explorador Olfativo 👃✨")
st.markdown("Digite o nome de um perfume que você gosta e descubra fragrâncias similares com base em suas notas olfativas.")

perfume_input = st.text_input(
    "Qual perfume você quer usar como referência?",
    placeholder="Ex: Sauvage Dior, Acqua di Giò, Chanel No. 5"
)

if st.button("Encontrar Decante de Perfumes Similares"):
    if perfume_input:
        prompt = f"""
        O objetivo é recomendar perfumes similares ao perfume '{perfume_input}' fornecido pelo usuário, inclusive fornecendo os links para compra

        Siga estes passos obrigatórios:
        1.  Primeiro, use a ferramenta 'Get Perfume Notes' para descobrir as notas olfativas do perfume '{perfume_input}'.
        2.  A partir da resposta, identifique as notas mais importantes (geralmente as de coração e base) e passe-as como input para a ferramenta 'Find Perfumes by Notes'. A entrada para esta ferramenta deve ser uma string de notas separadas por vírgula.
        3.  Pegue a lista de perfumes similares, e busque no mercado livre os links e os precos de cada um dos similares encontrados anteriormente .
        4.  No final, gere uma lista com os nomes dos similares, o link da compra e o valor no formato de json. 
        """
        
        with st.spinner("Consultando o nosso acervo de fragrâncias..."):
            try:
                agent = Agent(google_api_key=API_KEY)
                response = agent.get_similar_perfumes(prompt)
                st.info(response)
                response = re.sub(r"^\s*```json\s*|```\s*$", "", response['output'], flags=re.MULTILINE).strip()
                json_format = json.loads(response)
                table_format = pd.DataFrame(json_format['perfumes_similares'])
                st.dataframe(table_format, use_container_width=True)
            except Exception as e:
                st.error(f"Ocorreu um erro. O agente pode ter se confundido. Tente novamente ou com outro perfume.")
                st.error(f"Detalhe do erro: {e}")
    else:
        st.warning("Por favor, digite o nome de um perfume.")