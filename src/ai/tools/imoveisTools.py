from langchain_core.tools import tool
from services.imoveisServices import retornar_imoveis_do_locador

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