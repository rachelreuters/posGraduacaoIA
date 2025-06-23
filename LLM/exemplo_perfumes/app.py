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
                # agent = Agent(google_api_key=API_KEY)
                # response = agent.get_similar_perfumes(prompt)                
                # json_format = json.loads(response['output'])
                # st.code(json.dumps(json_format, indent=4, ensure_ascii=False), language="json")
                json_format = [
                {
                    "img": "https://http2.mlstatic.com/D_Q_NP_2X_721835-MLB83354304156_042025-E-perfume-arabe-khamrah-lattafa-100ml-eau-de-parfum-original.webp",
                    "nome": "Perfume Árabe Khamrah Lattafa 100ml Eau De Parfum Original",
                    "preco": 393.0,
                    "link": "https://produto.mercadolivre.com.br/MLB-5124857466-perfume-arabe-khamrah-lattafa-100ml-eau-de-parfum-original-_JM#polycard_client=search-nordic&position=19&search_layout=grid&type=item&tracking_id=56a6826e-42d5-4324-8b7f-ea724f3dbf19&wid=MLB5124857466&sid=search"
                },
                {
                    "img": "https://http2.mlstatic.com/D_Q_NP_2X_794567-MLA84558392742_052025-E.webp",
                    "nome": "Jean Paul Gaultier Le Male Elixir 75ml Selo Adipec Spray",
                    "preco": 470.0,
                    "link": "https://www.mercadolivre.com.br/jean-paul-gaultier-le-male-elixir-75ml-selo-adipec-spray/p/MLB24630800#polycard_client=search-nordic&searchVariation=MLB24630800&wid=MLB3874201387&position=5&search_layout=grid&type=product&tracking_id=f39e80a2-ecf6-4a5c-86b6-b89f48350963&sid=search"
                },
                {
                    "img": "https://http2.mlstatic.com/D_Q_NP_2X_633924-MLB82483007418_022025-E-perfume-angels-share-by-kilian-paris-genuino-com-75-ml-embalagem-original.webp",
                    "nome": "Perfume Angels Share By Kilian Paris Genuíno Com 7,5 Ml, Embalagem Original.",
                    "preco": 498.0,
                    "link": "https://produto.mercadolivre.com.br/MLB-5302183176-perfume-angels-share-by-kilian-paris-genuino-com-75-ml-embalagem-original-_JM#polycard_client=search-nordic&position=13&search_layout=grid&type=item&tracking_id=87a799b7-e03c-44ab-bf36-c1532cfd5356&wid=MLB5302183176&sid=search"
                },
                {
                    "img": "https://http2.mlstatic.com/D_Q_NP_2X_921730-CBT76454722268_052024-E.webp",
                    "nome": "Perfume Xerjoff 1861 Renaissance Eau De Parfum 100ml",
                    "preco": 2094.0,
                    "link": "https://www.mercadolivre.com.br/perfume-xerjoff-1861-renaissance-eau-de-parfum-100ml/p/MLB2017696195#polycard_client=search-nordic&searchVariation=MLB2017696195&wid=MLB3709965609&position=9&search_layout=grid&type=product&tracking_id=da37f646-6795-47b5-9572-078321e11347&sid=search"
                },
                {
                    "img": "https://http2.mlstatic.com/D_Q_NP_2X_615006-MLA50485574597_062022-E.webp",
                    "nome": "Giorgio Armani Emporio Armani Stronger with You Intensely Pour homme EDP 50ml para masculino",
                    "preco": 551.0,
                    "link": "https://www.mercadolivre.com.br/giorgio-armani-emporio-armani-stronger-with-you-intensely-pour-homme-edp-50ml-para-masculino/p/MLB19312693#polycard_client=search-nordic&searchVariation=MLB19312693&wid=MLB3817717685&position=4&search_layout=grid&type=product&tracking_id=29f6eabe-2544-4fc7-a4b0-bdfa02e4e6a9&sid=search"
                }
                ]
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