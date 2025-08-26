import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.environ.get("IMOVIEW_API_KEY")
codigo_acesso = os.environ.get("IMOVIEW_CODIGO_ACESSO")

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

