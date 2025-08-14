from langchain_core.tools import tool
from services.repassesServices import retornar_extrato_locador

@tool
def tool_coletar_dados_repasse(codigoCliente: int, codigoImovel: int, ano: int, mes: int):
    """
        Utilize essa ferramenta para coletar dados de um determinado repasse de um proprietário em um determinado mês e ano.
    """
    
    response = retornar_extrato_locador(codigoCliente, codigoImovel, ano, mes)

    if response['erro']:
        return "Erro ao realizar a requisição!"
    
    extrato = response['dados'].json()
    movimentosExtrato = extrato['lista'][0]

    return movimentosExtrato