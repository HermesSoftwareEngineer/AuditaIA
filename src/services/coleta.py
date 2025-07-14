import requests
from dotenv import load_dotenv
import os

load_dotenv()

def retornar_extrato_locador(codigoCliente: int, codigoImovel: int, ano: int, mes: int):
    url = 'https://api.imoview.com.br/Locador/RetornarExtrato'

    params = {
        'codigoCliente': codigoCliente,
        'codigoImovel': codigoImovel,
        'ano': ano,
        'mes': mes
    }

    api_key = os.environ.get("IMOVIEW_API_KEY")

    headers = {
        'acept': 'application/json',
        'chave': api_key
    }

    dados = requests.get(url, params=params, headers=headers)

    if dados.status_code != 200:
        return {'erro': "Erro ao realizar a requisição"}

    return {'dados': dados, 'erro': False}