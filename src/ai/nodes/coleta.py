from ai.custom_types import State
from ai.prompts_templates import prompt_consultor
from ai.tools.coletar_dados import tool_coletar_dados_repasse, tool_pesquisar_clientes, tool_retornar_imoveis_do_locador, tool_retornar_contratos_do_locador, tool_retornar_contratos_do_locatario
from ai.llms import llm

# Lista de tools
tools = [
    tool_coletar_dados_repasse, 
    tool_pesquisar_clientes,
    tool_retornar_imoveis_do_locador,
    tool_retornar_contratos_do_locador,
    tool_retornar_contratos_do_locatario
]

def consultar(state: State):
    prompt = prompt_consultor.invoke(state['messages'][-40:])
    response = llm.bind_tools(tools, tool_choice='any').invoke(prompt)

    return {'messages': response}