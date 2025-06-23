

import os
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain import hub
from langchain.agents import Tool, create_structured_chat_agent, AgentExecutor
import requests
import pandas as pd
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO)

def get_driver():
    from seleniumbase import Driver

    driver = Driver(uc=True, headless=True)
    return driver


class Agent:
    def __init__(self, google_api_key, model="gemini-2.0-flash", temperature=0.1):
        self.google_api_key = google_api_key
        self.model = model
        self.temperature = temperature
        self.logger = logging.getLogger(__name__)
        self.chat_model = ChatGoogleGenerativeAI(model=self.model,
                                     temperature=self.temperature,
                                     google_api_key=self.google_api_key)
        self.driver = get_driver()
        
    def get_perfume_notes(self , perfume_name: str) -> str:
        """
        Busca as notas olfativas de um perfume específico fazendo scraping real do site Fragrantica.
        O input deve ser o nome do perfume.
        Retorna uma string formatada com as notas de topo, coração e base.
        """
        print(f"--- Iniciando scraping para: {perfume_name} ---")

        try:
            # --- ETAPA 1: Buscar pelo perfume e encontrar o link da página correta ---
            
            search_url = f"https://www.fragrantica.com.br/busca/?query={perfume_name}"
            
            print(f"Buscando em: {search_url}")
            response = self.driver.get(search_url)
            wait = WebDriverWait(self.driver, 15)
            xpath_locator = f"//*[normalize-space() = 'Limpar Todos os Filtros']"

            wait.until(EC.visibility_of_element_located((By.XPATH, xpath_locator)))
            html_final = self.driver.page_source
            search_soup = BeautifulSoup(html_final, 'html.parser')
            
            # Encontra o primeiro resultado da busca, que geralmente é o mais relevante
            # O seletor CSS busca por um link dentro de um card de perfume
            result = search_soup.select_one("div.cell.card.fr-news-box")
            result_link = result.find("a")

            if not result_link or not result_link.has_attr('href'):
                return f"Desculpe, não consegui encontrar a página para o perfume '{perfume_name}'."

            perfume_url = result_link['href']
            print(f"Página do perfume encontrada: {perfume_url}")

            # --- ETAPA 2: Acessar a página do perfume e extrair as notas ---
            self.driver.get(perfume_url)

            xpath_locator = f"//*[normalize-space() = 'Principais Acordes']"

            wait.until(EC.visibility_of_element_located((By.XPATH, xpath_locator)))

            html_final = self.driver.page_source
            
            perfume_soup = BeautifulSoup(html_final, 'html.parser')
            
            # Encontra a seção de pirâmide olfativa
            pyramid_section = perfume_soup.find("div", id="pyramid")
            if not pyramid_section:
                return f"Não foi possível encontrar a pirâmide olfativa na página do perfume '{perfume_name}'."

            secoes_h4 = pyramid_section.find_all("h4")
            piramide_olfativa = {}

            for secao in secoes_h4:
                # Pega o nome da categoria (ex: "Notas de Topo") e limpa o texto
                categoria_nome = secao.text.strip()
                
                # Encontra o DIV que contém as notas, que é o "irmão" seguinte da tag <h4>
                notas_container = secao.find_next_sibling("div")
                
                lista_de_notas = []
                if notas_container:
                    # Dentro do container, encontra todos os DIVs que representam uma nota individual
                    # O seletor busca por DIVs que têm um atributo 'style' contendo "margin: 0.2rem"
                    notas_individuais = notas_container.select('div[style*="margin: 0.2rem"]')
                    
                    for nota_div in notas_individuais:
                        # O nome da nota é o texto dentro do último <div>
                        nome_nota = nota_div.text.strip()
                        lista_de_notas.append(nome_nota)
                
                # Adiciona a lista de notas ao nosso dicionário final
                piramide_olfativa[categoria_nome] = lista_de_notas

            # Verifica se alguma nota foi encontrada
            if not any(piramide_olfativa.values()):
                return f"Notas não encontradas na página de '{perfume_name}', a estrutura do site pode ter mudado."

            # --- ETAPA 3: Formatar a saída para o agente ---
            topo_str = ', '.join(piramide_olfativa['Notas de Topo']) if piramide_olfativa['Notas de Topo'] else 'Nenhuma'
            coracao_str = ', '.join(piramide_olfativa['Notas de Coração']) if piramide_olfativa['Notas de Coração'] else 'Nenhuma'
            base_str = ', '.join(piramide_olfativa['Notas de Base']) if piramide_olfativa['Notas de Base'] else 'Nenhuma'

            return f"Notas para {perfume_name}: Topo: {topo_str}; Coração: {coracao_str}; Base: {base_str}."

        except requests.exceptions.RequestException as e:
            return f"Erro de rede ao tentar acessar o Fragrantica: {e}"
        except Exception as e:
            return f"Ocorreu um erro inesperado durante o scraping: {e}"

    def find_perfumes_by_notes(self, notes_str: str) -> str:
        """
        Busca no Fragrantica por perfumes que contenham um conjunto de notas olfativas.
        O input deve ser uma string de notas separadas por vírgula.
        Retorna uma string formatada com uma lista de nomes de perfumes similares.
        """
        print(f"--- Iniciando scraping de busca por notas: {notes_str} ---")


        try:
            # --- ETAPA 1: Construir a URL de busca ---
            # A forma mais simples de buscar é usar a pesquisa geral do site.
            # Formatamos a query para algo como "perfumes com Lavanda e Ambroxan"
            query = f"{notes_str.replace(',', '~')}"
            search_query_encoded = quote_plus(query)
            search_url = f"https://www.fragrantica.com.br/busca/?ingredients.PT={search_query_encoded}"
            
            print(f"Buscando em: {search_url}")
            response = self.driver.get(search_url)
            wait = WebDriverWait(self.driver, 15)
            xpath_locator = f"//*[normalize-space() = 'Limpar Todos os Filtros']"

            wait.until(EC.visibility_of_element_located((By.XPATH, xpath_locator)))

            html_final = self.driver.page_source

            search_soup = BeautifulSoup(html_final, 'html.parser')
            
            # --- ETAPA 2: Extrair os nomes dos perfumes da página de resultados ---
        
            perfume_cards = search_soup.select("div.cell.card.fr-news-box")
            
            if not perfume_cards:
                return f"Não encontrei resultados para perfumes com as notas: '{notes_str}'."

            found_perfumes = []
            for card in perfume_cards[:5]:
                paragraph = card.select('p')
                name_tag=  paragraph[0].text.strip()
                brand_tag = paragraph[1].text.strip()
                name_tag = " ".join([name_tag, brand_tag])    
                if name_tag:
                    found_perfumes.append(name_tag)

            if not found_perfumes:
                return f"Não foi possível extrair nomes de perfumes para as notas: '{notes_str}'. A estrutura do site pode ter mudado."
            
            # --- ETAPA 3: Formatar a saída para o agente ---
            return f"Perfumes similares encontrados: {', '.join(found_perfumes)}."

        except requests.exceptions.RequestException as e:
            return f"Erro de rede ao tentar buscar por notas no Fragrantica: {e}"
        except Exception as e:
            return f"Ocorreu um erro inesperado durante o scraping da busca: {e}"

    def find_ml_prices(self, query: str) -> str:

        query = f'"{query}"'
        search_url = f'https://lista.mercadolivre.com.br/beleza-cuidado-pessoal/perfumes/{query.replace(" ", "-")}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
        }
        print(f"Buscando em: {search_url}")
        response = self.driver.get(search_url)
        wait = WebDriverWait(self.driver, 15)
        class_name = "ui-search-sidebar"
        locator = (By.CSS_SELECTOR, f".{class_name}")
        wait.until(
            EC.visibility_of_element_located(locator)
        )
        html_final = self.driver.page_source

        search_soup = BeautifulSoup(html_final, 'html.parser')

        items = search_soup.select("li.ui-search-layout__item")
            
        if not items:
            print("Nenhum item de produto encontrado na página. Verifique o seletor ou se há um CAPTCHA.")
            return []

        print(f"Encontrados {len(items)} itens na página. Extraindo informações...")
    
        found_products = []
        for item in items[:1]:
            # Seleciona o título, preço e link dentro de cada item
            title_tag = item.select_one('h3')
            price_tag = item.select_one('.andes-money-amount__fraction')
            link_tag = item.select_one('h3').find('a').get('href')
            image_tag = item.select_one('img')
            response = requests.get(link_tag, headers=headers, allow_redirects=True, timeout=10)
        
            link_tag = response.url

            if title_tag and price_tag and link_tag and image_tag:
                # Limpeza e formatação dos dados extraídos
                title = title_tag.text.strip()
                # Remove o separador de milhar e converte vírgula para ponto
                price_str = price_tag.text.strip().replace('.', '').replace(',', '.')
                link = link_tag.split("?pdp")[0]
                image_src= image_tag.get('data-src') or image_tag.get('src')
                try:
                    price = float(price_str)
                    found_products.append({'nome': title,'img':image_src, 'preco': price, 'link': link})
                except (ValueError, TypeError):
                    print(f"Não foi possível converter o preço para o item: {title}")

        if not found_products:
            print("Nenhum produto com preço válido foi extraído.")
            return []

        # Ordena a lista de produtos encontrados pelo preço, do menor para o maior
        sorted_products = sorted(found_products, key=lambda p: p['preco'])
        
        # Retorna apenas os 'num_results' primeiros (os mais baratos)
        return sorted_products    

    def get_similar_perfumes(self, prompt):
        tools = [
            Tool(
                name="Pegue as Notas do Perfume",
                func=self.get_perfume_notes,
                description="Use esta ferramenta para encontrar as notas olfativas de um perfume específico. O input deve ser o nome do perfume."
            ),
            Tool(
                name="Busque Perfumes pelas suas notas",
                func=self.find_perfumes_by_notes,
                description="Use esta ferramenta para encontrar outros perfumes que compartilham um conjunto de notas. O input deve ser uma string de notas importantes, separadas por vírgula."
            ),
            Tool(
                name="Busque links e precos vendendo os Perfumes",
                func=self.find_ml_prices,
                description="Use esta ferramenta para encontrar vendedores que vendam os perfumes encontrados anteriormente. O input e o nome de cada perfume e o output tem que ser o preco e o link do produto."
            )
        ]

        prompt_template = hub.pull("hwchase17/structured-chat-agent")

        # MUDANÇA 2: Criamos o agente com a função correta
        agent = create_structured_chat_agent(
            llm=self.chat_model,
            tools=tools,
            prompt=prompt_template
        )
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True, # verbose=True é ótimo para ver o raciocínio do agente no terminal
            handle_parsing_errors=True,
            max_iterations=20 # Previne loops infinitos
        )
        
        return agent_executor.invoke({"input": prompt})

perfume_input = "Scandal Jean paul"

prompt = f"""
        O objetivo é recomendar perfumes similares ao perfume '{perfume_input}' fornecido pelo usuário.

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
load_dotenv() 


# API_KEY = os.getenv("API_GOOGLE")

# agent = Agent(API_KEY)

# # response = agent.get_similar_perfumes(prompt)

# # import json
# # json_format = json.loads(response['output'])


# # print(json_format['perfumes_similares'])


# # print(response)

# # find_perfumes_by_notes("Caramel, Fava Tonka, Vetiver")

# agent.find_ml_prices("Khamrah")