
from bs4 import BeautifulSoup
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain import hub
from langchain.agents import Tool, create_structured_chat_agent, AgentExecutor
import requests
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from langchain.chains import LLMChain
from chain_get_notes import GetNotesTemplate
from chain_get_similar_perfumes import GetSimilarPerfumesTemplate
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
        

    def find_ml_prices(self, query: str) -> str:

        query = f'"{query}"'
        search_url = f'https://lista.mercadolivre.com.br/beleza-cuidado-pessoal/perfumes/{query.replace(" ", "-")}'

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
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
            }
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
        get_notes_template_chain = GetNotesTemplate()
        get_similar_template_chain =  GetSimilarPerfumesTemplate()

        get_notes_chain = LLMChain(
            llm=self.chat_model,
            prompt=get_notes_template_chain.chat_prompt,
        )

        get_similar_list = LLMChain(
            llm=self.chat_model,
            prompt=get_similar_template_chain.chat_prompt,
        )

        tools = [
            Tool(
                name="Pegue as Notas do Perfume e o Tipo",
                func=get_notes_chain.invoke,
                description="Use esta ferramenta para encontrar as notas olfativas de um perfume específico e o seu tipo. O input deve ser o nome do perfume."
            ),
            Tool(
                name="Busque Perfumes pelas suas notas e tipo",
                func=get_similar_list.invoke,
                description="Use esta ferramenta para encontrar outros perfumes que compartilham um conjunto de notas e tipo. O input deve ser uma string com o tipo e mais as notas importantes, separadas por vírgula."
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
# load_dotenv() 


# API_KEY = os.getenv("API_GOOGLE")

# agent = Agent(API_KEY)

# response = agent.get_similar_perfumes(prompt)


# print(response)


# import json
# json_format = json.loads(response['output'])


# # print(json_format['perfumes_similares'])


# # print(response)

#agent.find_perfumes_by_notes_and_type("Oriental, Jasmim, Flor de Laranjeira, Cereus Noturno, Rosa, Baunilha, Fava Tonka, Sândalo de Mysore")

# agent.find_ml_prices("Khamrah")