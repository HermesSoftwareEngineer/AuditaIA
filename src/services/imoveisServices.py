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
        'accept': 'application/json',  # corrigido typo
        'chave': api_key
    }

    dados = requests.get(url, params=params, headers=headers)

    if dados.status_code != 200:
        return {
            'erro': f"Erro ao realizar a requisição de pesquisar cliente",
            'status_code': dados.status_code,
            'response_text': dados.text
        }

    return {'dados': dados, 'erro': False}

def reduzir_imovel(imovel):
    return {
        "codigo": imovel.get("codigo"),
        "titulo": imovel.get("titulo"),
        "finalidade": imovel.get("finalidade"),
        "tipo": imovel.get("tipo"),
        "situacao": imovel.get("situacao"),
        "valor": imovel.get("valor"),
        "bairro": imovel.get("bairro"),
        "cidade": imovel.get("cidade"),
        "estado": imovel.get("estado"),
        "endereco": imovel.get("endereco"),
        "numero": imovel.get("numero"),
        "numeroquartos": imovel.get("numeroquartos"),
        "numerovagas": imovel.get("numerovagas"),
        "numerobanhos": imovel.get("numerobanhos"),
        "area": imovel.get("areaprincipal"),
        "urlfotoprincipal": imovel.get("urlfotoprincipal"),
        "descricao": imovel.get("descricao"),
    }

def retornar_imoveis_disponiveis(finalidade: int, numeroPagina: int = 1, numeroRegistros: int = 20, destinacao: int = None, endereco: str = None, numeroquartos: int = None, numerovagas: int = None, numerobanhos: int = None, valorde: int = None, valorate: int = None):
    url = 'https://api.imoview.com.br/Imovel/RetornarImoveisDisponiveis'

    body = {
        'finalidade': finalidade,
        'numeroPagina': numeroPagina,
        'numeroRegistros': numeroRegistros,
    }
    if destinacao is not None:
        body['destinacao'] = destinacao
    if endereco is not None:
        body['endereco'] = endereco
    if numeroquartos is not None:
        body['numeroquartos'] = numeroquartos
    if numerovagas is not None:
        body['numerovagas'] = numerovagas
    if numerobanhos is not None:
        body['numerobanhos'] = numerobanhos
    if valorde is not None:
        body['valorde'] = valorde
    if valorate is not None:
        body['valorate'] = valorate

    headers = {
        'accept': 'application/json',
        'chave': api_key
    }

    dados = requests.post(url, json=body, headers=headers)

    if dados.status_code != 200:
        result = {
            'erro': "Erro ao realizar a requisição de retornar imoveis!",
            'status_code': dados.status_code,
            'response_text': dados.text
        }
        print("ERRO AO REQUISITAR IMÓVEIS DISPONÍVEIS")
        print("DEBUG - Headers:", headers)
        print("DEBUG - Body:", body)
        print("DEBUG - Response:", result)
        return result

    try:
        resposta = dados.json()
        lista_reduzida = [reduzir_imovel(imovel) for imovel in resposta.get("lista", [])]
        return {
            "dados": {
                "quantidade": resposta.get("quantidade"),
                "menorvalor": resposta.get("menorvalor"),
                "maiorvalor": resposta.get("maiorvalor"),
                "menorarea": resposta.get("menorarea"),
                "maiorarea": resposta.get("maiorarea"),
                "lista": lista_reduzida,
            },
            "erro": False
        }
    except Exception as e:
        return {'erro': f"Erro ao processar resposta: {str(e)}"}