from ai.tools.coletar_dados import tool_pesquisar_clientes, tool_coletar_dados_repasse, tool_retornar_imoveis_do_locador, tool_retornar_contratos_do_locador
from langgraph.prebuilt import ToolNode

tools = [
    tool_coletar_dados_repasse,
    tool_pesquisar_clientes,
    tool_retornar_imoveis_do_locador,
    tool_retornar_contratos_do_locador
]

toolsNode = ToolNode(tools)