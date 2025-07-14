from langchain_core.tools import tool
from services.coleta import retornar_extrato_locador, pesquisar_cliente
import json

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

@tool
def tool_pesquisar_clientes(textoPesquisa: str):
    """
        Use esta ferramenta para buscar clientes informando qualquer dado disponível — como nome, CPF, e-mail, entre outros. O resultado será uma lista contendo os códigos dos clientes encontrados.
    """

    response = pesquisar_cliente(textoPesquisa)

    if response['erro']:
        return "Erro ao realizar a requisição de pesquisar cliente!"
    
    listaClientes = response['dados'].json()

    return listaClientes

# movimentosExtrato = coletar_dados_repasse(1745, 454, 2025, 3)
# with open('dados.json', 'w', encoding='utf-8') as f:
#     json.dump(movimentosExtrato, f, ensure_ascii=False, indent=4)