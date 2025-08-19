from langchain_core.tools import tool
from services.clienteServices import pesquisar_cliente

@tool
def tool_pesquisar_clientes(textoPesquisa: str):
    """
        Use esta ferramenta para descobrir o CÓDIGO DE UM CLIENTE. Você pode informar qualquer dado disponível — como nome (mesmo inco,mpleto), CPF, e-mail, entre outros. O resultado será uma lista contendo os códigos dos clientes encontrados.
    """

    response = pesquisar_cliente(textoPesquisa)

    if response['erro']:
        return "Erro ao realizar a requisição de pesquisar cliente!"
    
    listaClientes = response['dados'].json()

    return listaClientes