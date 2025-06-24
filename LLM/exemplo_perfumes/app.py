import re
import streamlit as st
import os
from dotenv import load_dotenv
import asyncio
import json
import pandas as pd

from agent import Agent

load_dotenv()
API_KEY = os.getenv("API_GOOGLE")

# Solução para o loop de eventos assíncronos no Streamlit
try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

st.set_page_config(layout="wide", page_title="Dicas Olfativas")

st.title("Dicas Olfativas 👃✨")
st.markdown("Digite o nome de um perfume que você gosta e descubra fragrâncias similares com base em suas notas olfativas.")

perfume_input = st.text_input(
    "Qual perfume você quer usar como referência?",
    placeholder="Ex: Sauvage Dior, Acqua di Giò, Chanel No. 5"
)

if st.button("Encontrar Perfumes Similares"):
    if perfume_input:
        prompt = f"""
        O objetivo é recomendar perfumes similares ao perfume '{perfume_input}' fornecido pelo usuário, inclusive fornecendo os links para compra

        Siga estes passos obrigatórios:
        1.  Primeiro, use a ferramenta 'Get Perfume Notes' para descobrir as notas olfativas do perfume '{perfume_input}'.
        2.  A partir da resposta, identifique as notas mais importantes (geralmente as de coração e base) e passe-as como input para a ferramenta 'Find Perfumes by Notes'. A entrada para esta ferramenta deve ser uma string de notas separadas por vírgula.
        3.  Pegue a lista de perfumes similares, e busque no mercado livre os links e os precos de cada um dos similares encontrados anteriormente .
          4.  No final, gere uma lista com os nomes dos similares, o link da compra e o valor no formato de json como no exemplo:
            [{{
               "img": "xxx.png",
               "nome": "X",
               "preco": 123,
               "link": "https//..."
            }},
            {{
               "img": "xxx.png",
               "nome": "X",
               "preco" 123,
               "link": "https//..."
            }}]
        """
        
        with st.spinner("Consultando o nosso acervo de fragrâncias..."):
            try:
                agent = Agent(google_api_key=API_KEY)
                response = agent.get_similar_perfumes(prompt)                
                json_format = json.loads(response['output'])
                if not json_format:
                    st.warning("Nenhum perfume encontrado :( ")
                else:
                    col1, col2 = st.columns(2)
                    for index, item in enumerate(json_format):
                        if index % 2 == 0:
                            with col1:
                                with st.container(border=True):
                                    st.markdown(
                                        f"<div style='text-align: center;'><img src='{item.get("img")}' width='250'></div>",
                                        unsafe_allow_html=True
                                    )
                                    st.markdown(f"<h4 style='text-align: center;'>{item.get('nome')}</h4>", unsafe_allow_html=True)
        
                                    preco = item.get('preco', 0)
                                    st.markdown(f"<h3 style='text-align: center;'>R$ {preco:.2f}</h3>", unsafe_allow_html=True)
                                    st.link_button("Ver na Loja", item.get("link"), use_container_width=True)
                        else:
                            with col2:
                                with st.container(border=True):
                                    st.markdown(
                                        f"<div style='text-align: center;'><img src='{item.get("img")}' width='250'></div>",
                                        unsafe_allow_html=True
                                    )
                                    st.markdown(f"<h4 style='text-align: center;'>{item.get('nome')}</h4>", unsafe_allow_html=True)
                                    preco = item.get('preco', 0)
                                    st.markdown(f"<h3 style='text-align: center;'>R$ {preco:.2f}</h3>", unsafe_allow_html=True)
                                    st.link_button("Ver na Loja", item.get("link"), use_container_width=True)
            except Exception as e:
                st.error(f"Ocorreu um erro. O agente pode ter se confundido. Tente novamente ou com outro perfume.")
                st.error(f"Detalhe do erro: {e}")
    else:
        st.warning("Por favor, digite o nome de um perfume.")