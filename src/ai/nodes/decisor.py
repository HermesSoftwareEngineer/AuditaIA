from ai.custom_types import State
from ai.prompts import prompt_assistente
from ai.tools.coletar_dados import tool_coletar_dados_repasse, tool_pesquisar_clientes
from ai.llms import llm

# Lista de tools
tools = [
    tool_coletar_dados_repasse, 
    tool_pesquisar_clientes
]

def consultar_ou_responder(state: State):
    prompt = prompt_assistente.invoke(state['messages'][-40:])
    response = llm.bind_tools(tools).invoke(prompt)

    return {'messages': response}