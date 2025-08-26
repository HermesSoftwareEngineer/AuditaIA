from langchain_core.tools import tool
from services.movimentosServices import retornar_movimentos

@tool
def tool_retornar_movimentos(numeroPagina: int, numeroRegistros: int, codigoCliente: int = None, codigoImovel: int = None, codigoContratoAluguel: int = None, codigoContratoVenda: int = None, dataVencimentoInicial: str = None, dataVencimentoFinal: str = None):
    """
        Use esta ferramenta para buscar movimentos financeiros do sistema.

        Parâmetros obrigatórios:
        - numeroPagina (int): O número da página a ser retornada (padrão é 1).
        - numeroRegistros (int): O número de registros por página (padrão é 20, limite é 50).

        Parâmetros opcionais:
        - codigoCliente (int, opcional): O código do cliente para filtrar os movimentos.
        - codigoImovel (int, opcional): O código do imóvel para filtrar os movimentos.
        - codigoContratoAluguel (int, opcional): O código do contrato de aluguel para filtrar os movimentos.
        - codigoContratoVenda (int, opcional): O código do contrato de venda para filtrar os movimentos.
        - dataVencimentoInicial (str, opcional): Data inicial de vencimento para filtrar os movimentos (formato 'YYYY-MM-DD').
        - dataVencimentoFinal (str, opcional): Data final de vencimento para filtrar os movimentos (formato 'YYYY-MM-DD').
    """

    response = retornar_movimentos(numeroPagina, numeroRegistros, codigoCliente, codigoImovel, codigoContratoAluguel, codigoContratoVenda, dataVencimentoInicial, dataVencimentoFinal)

    if response['erro']:
        return "Erro ao realizar a requisição de retornar movimentos!"
    
    listaMovimentos = response['dados'].json()

    return listaMovimentos