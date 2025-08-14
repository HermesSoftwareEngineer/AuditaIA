from ai.tools.clienteTools import tool_pesquisar_clientes
from ai.tools.contratosTools import tool_retornar_contratos_do_locador, tool_retornar_contratos_do_locatario
from ai.tools.imoveisTools import tool_retornar_imoveis_do_locador
from ai.tools.repasseTools import tool_coletar_dados_repasse

toolsList = [
    tool_coletar_dados_repasse,
    tool_pesquisar_clientes,
    tool_retornar_imoveis_do_locador,
    tool_retornar_contratos_do_locador,
    tool_retornar_contratos_do_locatario
]