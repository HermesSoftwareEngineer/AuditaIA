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

def retornar_contratos_do_locador(numeroPagina: int, numeroRegistros: int, codigoCliente: int, endereco: str = None, codigoContrato: str = None):
    url='https://api.imoview.com.br/Locador/RetornarContratos'

    params = {
        'numeroPagina': numeroPagina,
        'numeroRegistros': numeroRegistros,
        'codigoCliente': codigoCliente,
    }
    if endereco is not None:
        params['endereco'] = endereco

    if codigoContrato is not None:
        params['codigoContrato'] = codigoContrato

    headers = {
        'accept':'aplication/json',
        'chave': api_key
    }

    dados = requests.get(url, params=params, headers=headers)

    if dados.status_code != 200:
        return {'erro': "Erro ao realizar a requisição de pesquisar cliente"}

    return {'dados': dados, 'erro': False}

def retornar_contratos_do_locatario(numeroPagina: int, numeroRegistros: int, codigoCliente: int, endereco: str = None, codigoContrato: str = None):
    url='https://api.imoview.com.br/Locatario/RetornarContratos'

    params = {
        'numeroPagina': numeroPagina,
        'numeroRegistros': numeroRegistros,
        'codigoCliente': codigoCliente,
        'mostrarRescindidos': 'true'
    }
    if endereco is not None:
        params['endereco'] = endereco

    if codigoContrato is not None:
        params['codigoContrato'] = codigoContrato

    headers = {
        'accept':'aplication/json',
        'chave': api_key
    }

    dados = requests.get(url, params=params, headers=headers)

    if dados.status_code != 200:
        return {'erro': "Erro ao realizar a requisição de pesquisar cliente"}

    return {'dados': dados, 'erro': False}