import pandas as pd
import requests

def baixar_deputados() -> pd.DataFrame:
    resp = requests.get("https://dadosabertos.camara.leg.br/api/v2/deputados")
    data= resp.json()
    df_data = pd.DataFrame(data["dados"])
    return df_data

def sumarizar_por_partido(deputados) -> pd.DataFrame:
    sumarizado =  (
            deputados
                .groupby('siglaPartido')
                .size()
                .sort_values(ascending=False)
            )
    return sumarizado