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

def pesquisar_cliente(textoPesquisa: str):
    url='https://api.imoview.com.br/Cliente/App_PesquisarCliente'

    params = {
        'textoPesquisa': textoPesquisa,
        'codigoUsuario': 7
    }

    headers = {
        'accept':'aplication/json',
        'chave': api_key,
        'codigoacesso': codigo_acesso
    }

    dados = requests.get(url, params=params, headers=headers)

    if dados.status_code != 200:
        return {'erro': "Erro ao realizar a requisição de pesquisar cliente"}

    return {'dados': dados, 'erro': False}