import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("IMOVIEW_API_KEY") 

def consultar_repasse_locador(data_inicial, data_final, codigo_cliente):
    url = "https://api.imoview.com.br/Movimento/RetornarMovimentos"
    params = {
        "numeroPagina": 1,
        "numeroRegistros": 100,
        "codigoCliente": codigo_cliente,
        "dataVencimentoInicial": data_inicial,
        "dataVencimentoFinal": data_final,
    }
    headers = {
        "accept": "application/json",
        "chave": f"{api_key}",
    }

    print(
        f"""Requisição feita! url: {url}, params: {params}"""
    )
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print("Erro:", response.status_code, response.text)
        return None