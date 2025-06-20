

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain import hub
from langchain.agents import Tool, create_structured_chat_agent, AgentExecutor
from langchain.tools import StructuredTool
import yfinance as yf
import pandas as pd
from langchain.pydantic_v1 import BaseModel, Field
import logging

logging.basicConfig(level=logging.INFO)


def get_tickers_from_sector(sector: str) -> list[str]:
    """
    Retorna uma lista de tickers de ações para um determinado setor da B3.
    Os setores válidos são: 'Bancos', 'Varejo', 'Energia Elétrica', 'Mineração'.
    """
    # Para este exemplo, usamos um dicionário fixo. 
    # Em um projeto real, isso poderia vir de uma API ou web scraping.
    sector_map = {
        "Bancos": ["ITUB4.SA", "BBDC4.SA", "SANB11.SA", "BBAS3.SA"],
        "Varejo": ["MGLU3.SA", "LREN3.SA", "VVAR3.SA", "PETR4.SA"], # Exemplo, VVAR3 não existe mais
        "Energia Elétrica": ["ELET3.SA", "CMIG4.SA", "CPLE6.SA", "EQTL3.SA"],
        "Mineração": ["VALE3.SA", "CSNA3.SA", "GGBR4.SA"],
    }
    return sector_map.get(sector, [])


def calculate_technical_indicator(ticker: str, indicator: str) -> float:
    """Calcula o valor de um indicador técnico para um ticker específico."""
    data = yf.download(ticker, start="2022-06-01", end="2025-06-01", progress=False)
    if data.empty: return float('nan')
    if isinstance(data.columns, pd.MultiIndex):
        # Remove o nível do ticker (ex: 'ITUB4.SA'), deixando apenas 'Open', 'High', 'Close', etc.
        data.columns = data.columns.droplevel(1)
    print(data.info())
    if indicator.upper() == 'IFR':
        rsi_series = data.ta.rsi()
        print(rsi_series)
        if rsi_series is not None and not rsi_series.empty:
            print(rsi_series.iloc[-1])
            return round(rsi_series.iloc[-1], 2)
    return float('nan')

class IndicatorInput(BaseModel):
    # Usamos o Field para dar uma descrição clara de cada argumento
    ticker: str = Field(description="O ticker da ação a ser analisada, como 'ITUB4.SA'.")
    indicator: str = Field(description="A sigla do indicador técnico a ser calculado, como 'IFR'.")
    

class Agent:
    def __init__(self, google_api_key, model="gemini-2.0-flash", temperature=0.1):
        self.google_api_key = google_api_key
        self.model = model
        self.temperature = temperature
        self.logger = logging.getLogger(__name__)
        self.chat_model = ChatGoogleGenerativeAI(model=self.model,
                                     temperature=self.temperature,
                                     google_api_key=self.google_api_key)

    def get_tips_investing(self, prompt):
        tools = [
            Tool(
                name="Get Tickers from Sector",
                func=get_tickers_from_sector,
                description="Útil para obter uma lista de tickers de ações para um setor específico da bolsa brasileira. Os setores disponíveis são 'Bancos', 'Varejo', 'Energia Elétrica', 'Mineração'."
            ),
            StructuredTool.from_function(
                func=calculate_technical_indicator,
                name="Calculate Technical Indicator for a Stock",
                description="""Calcula um indicador técnico para UMA ÚNICA AÇÃO DE CADA VEZ. 
                   Esta ferramenta NÃO aceita listas de tickers. 
                   O input deve ser o ticker individual da ação (ex: 'ITUB4.SA') 
                   e a sigla do indicador (ex: 'IFR').""",
                args_schema=IndicatorInput # Agora o LangChain sabe como usar este schema
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

            
