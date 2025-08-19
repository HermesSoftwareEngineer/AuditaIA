from langchain_core.tools import tool
from services.imoveisServices import retornar_imoveis_do_locador, retornar_imoveis_disponiveis

@tool
def tool_retornar_imoveis_do_locador(codigoCliente: str, numeroPagina: int):
    """
        Use esta ferramenta para buscar imóveis de um locador específico. Passe como parâmetro o código do cliente e o número da página (são mostrados 20 imóveis por página).
    """

    numeroRegistros = 20

    response = retornar_imoveis_do_locador(codigoCliente, numeroPagina, numeroRegistros)

    if response['erro']:
        return "Erro ao realizar a requisição de retornar imóveis do locador!"
    
    listaImoveis = response['dados'].json()

    return listaImoveis

@tool
def tool_retornar_imoveis_disponiveis(
    finalidade: int,
    numeroPagina: int = 1,
    numeroRegistros: int = 20,
    destinacao: int = None,
    endereco: str = None,
    numeroquartos: int = None,
    numerovagas: int = None,
    numerobanhos: int = None,
    valorde: int = None,
    valorate: int = None
):
    """
        Use esta ferramenta para buscar imóveis disponíveis.
        Parâmetros obrigatórios:
        - finalidade (ex: 1 para locação, 2 para venda)
        - numeroPagina (padrão: 1)
        - numeroRegistros (padrão: 20)

        Parâmetros opcionais:
        - destinacao (opcional, Enviar 1 para Residencial, 2 para Comercial, 3 para Residencial e comercial, 4 para industrial, 5 para rural, 6 para temporada, 7 para corporativa, 8 para comercial e industrial ou 0 para todos)
        - endereco (opcional)
        - numeroquartos (opcional)
        - numerovagas (opcional)
        - numerobanhos (opcional)
        - valorde (opcional, valor mínimo)
        - valorate (opcional, valor máximo)
        O retorno será uma lista reduzida com os principais dados dos imóveis.
    """
    response = retornar_imoveis_disponiveis(
        finalidade,
        numeroPagina,
        numeroRegistros,
        destinacao,
        endereco,
        numeroquartos,
        numerovagas,
        numerobanhos,
        valorde,
        valorate
    )
    if response['erro']:
        return "Erro ao realizar a requisição de retornar imóveis disponíveis!"
    return response['dados']