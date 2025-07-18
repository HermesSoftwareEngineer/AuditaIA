from ai.custom_types import State, Response_or_Query
from ai.prompts_templates import prompt_assistente
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

def consultar_ou_responder(state: State):
    list_messages = prompt_assistente.invoke(state['messages'][-40:])
    prompt = state['prompt']
    messages = list_messages.__str__()
    result = messages + prompt
    response = llm.bind_tools(tools).invoke(result)

    return {'messages': response}