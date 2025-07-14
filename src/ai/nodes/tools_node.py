from ai.tools.coletar_dados import tool_pesquisar_clientes, tool_coletar_dados_repasse
from langgraph.prebuilt import ToolNode

tools = [
    tool_coletar_dados_repasse,
    tool_pesquisar_clientes
]

toolsNode = ToolNode(tools)