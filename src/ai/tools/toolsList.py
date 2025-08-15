from ai.tools.clienteTools import tool_pesquisar_clientes
from ai.tools.contratosTools import tool_retornar_contratos_do_locador, tool_retornar_contratos_do_locatario
from ai.tools.imoveisTools import tool_retornar_imoveis_do_locador, tool_retornar_imoveis_disponiveis
from ai.tools.extratosTools import tool_coletar_dados_repasse, tool_coletar_dados_extrato_locatario
from ai.tools.movimentosTools import tool_retornar_movimentos

toolsList = [
    tool_coletar_dados_repasse,
    tool_pesquisar_clientes,
    tool_retornar_imoveis_do_locador,
    tool_retornar_contratos_do_locador,
    tool_retornar_contratos_do_locatario,
    tool_retornar_movimentos,
    tool_retornar_imoveis_disponiveis,
    tool_coletar_dados_extrato_locatario
]