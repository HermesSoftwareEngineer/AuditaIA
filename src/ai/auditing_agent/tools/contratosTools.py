from langchain_core.tools import tool
from services.contratosServices import retornar_contratos_do_locador, retornar_contratos_do_locatario

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

@tool
def tool_retornar_contratos_do_locatario(numeroPagina: int, codigoCliente: int, numeroRegistros: int, endereco: str = None, codigoContrato: str = None):
    """
        Use esta ferramenta para buscar contratos de locação de um LOCATÁRIO(inquilino) em específico. 
        Endereço é opcional. Codigo do contrato também é opcional. Número de registros pode ser no máximo 20.
    """

    response = retornar_contratos_do_locatario(numeroPagina, numeroRegistros, codigoCliente, endereco, codigoContrato)

    if response['erro']:
        return "Erro ao realizar a requisição de retornar imóveis do locador!"
    
    listaContratos = response['dados'].json()

    return listaContratos