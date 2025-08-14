import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.environ.get("IMOVIEW_API_KEY")

def retornar_movimentos(numeroPagina: int, numeroRegistros: int, codigoCliente: int = None, codigoImovel: int = None, codigoContratoAluguel: int = None, codigoContratoVenda: int = None, dataVencimentoInicial: str = None, dataVencimentoFinal: str = None):
    url = 'https://api.imoview.com.br/Movimento/RetornarMovimentos'

    params = {
        'numeroPagina': numeroPagina,
        'numeroRegistros': numeroRegistros,
    }
    if dataVencimentoInicial is not None:
        params['dataVencimentoInicial'] = dataVencimentoInicial
    if dataVencimentoFinal is not None:
        params['dataVencimentoFinal'] = dataVencimentoFinal
    if codigoCliente is not None:
        params['codigoCliente'] = codigoCliente
    if codigoImovel is not None:
        params['codigoImovel'] = codigoImovel
    if codigoContratoAluguel is not None:
        params['codigoContratoAluguel'] = codigoContratoAluguel
    if codigoContratoVenda is not None:
        params['codigoContratoVenda'] = codigoContratoVenda

    headers = {
        'accept': 'application/json',
        'chave': api_key
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        return {'erro': "Erro ao realizar a requisição de movimentos"}

    return {'dados': response, 'erro': False}