from langchain_core.tools import tool
from services.coleta import retornar_extrato_locador, pesquisar_cliente, retornar_imoveis_do_locador, retornar_contratos_do_locador
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
def tool_retornar_contratos_do_locador(numeroPagina: int, codigoCliente: int, endereco: str = None, codigoContrato: str = None):
    """
        Use esta ferramenta para buscar contratos de locação de um locador em específico. 
        Endereço é opcional. Codigo do contrato também é opcional.
    """

    numeroRegistros = 20

    response = retornar_contratos_do_locador(numeroPagina, numeroRegistros, codigoCliente, endereco, codigoContrato)

    if response['erro']:
        return "Erro ao realizar a requisição de retornar imóveis do locador!"
    
    listaContratos = response['dados'].json()

    return listaContratos

# movimentosExtrato = coletar_dados_repasse(1745, 454, 2025, 3)
# with open('dados.json', 'w', encoding='utf-8') as f:
#     json.dump(movimentosExtrato, f, ensure_ascii=False, indent=4)