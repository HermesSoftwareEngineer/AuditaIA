import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.environ.get("IMOVIEW_API_KEY")
codigo_acesso = os.environ.get("IMOVIEW_CODIGO_ACESSO")

def retornar_extrato_locador(codigoCliente: int, codigoImovel: int, ano: int, mes: int):
    url = 'https://api.imoview.com.br/Locador/RetornarExtrato'

    params = {
        'codigoCliente': codigoCliente,
        'codigoImovel': codigoImovel,
        'ano': ano,
        'mes': mes
    }

    headers = {
        'acept': 'application/json',
        'chave': api_key
    }

    dados = requests.get(url, params=params, headers=headers)

    if dados.status_code != 200:
        return {'erro': "Erro ao realizar a requisição de retornar extrato locador"}

    return {'dados': dados, 'erro': False}

def retornar_extrato_locatario(codigoCliente: int, ano: int, mes: int, codigoImovel: int = None, codigoContrato: int = None):
    url = 'https://api.imoview.com.br/Locatario/RetornarExtrato'

    params = {
        'codigoCliente': codigoCliente,
        'ano': ano,
        'mes': mes
    }
    if codigoImovel is not None:
        params['codigoImovel'] = codigoImovel
    if codigoContrato is not None:
        params['codigoContrato'] = codigoContrato

    headers = {
        'accept': 'application/json',
        'chave': api_key
    }

    dados = requests.get(url, params=params, headers=headers)

    if dados.status_code != 200:
        print("ERRO AO REQUISITAR EXTRATO LOCATARIO")
        print("DEBUG - Headers:", headers)
        print("DEBUG - Params:", params)
        print("DEBUG - Response:", dados.text)
        return {'erro': "Erro ao realizar a requisição de retornar extrato locatario"}

    return {'dados': dados, 'erro': False}