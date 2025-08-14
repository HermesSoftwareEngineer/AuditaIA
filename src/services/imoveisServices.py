import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.environ.get("IMOVIEW_API_KEY")
codigo_acesso = os.environ.get("IMOVIEW_CODIGO_ACESSO")

def retornar_imoveis_do_locador(codigoCliente: int, numeroPagina: int, numeroRegistros: int, situacao: int = None):
    url='https://api.imoview.com.br/Locador/RetornarImoveis'

    params = {
        'codigoCliente': codigoCliente,
        'numeroPagina': numeroPagina,
        'numeroRegistros': numeroRegistros,
    }
    if situacao is not None:
        params['situacao'] = situacao

    headers = {
        'accept':'aplication/json',
        'chave': api_key
    }

    dados = requests.get(url, params=params, headers=headers)

    if dados.status_code != 200:
        return {'erro': "Erro ao realizar a requisição de pesquisar cliente"}

    return {'dados': dados, 'erro': False}