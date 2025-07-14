from ai.custom_types import State
from ai.prompts import prompt_assistente
from ai.tools.coletar_dados import coletar_dados_repasse
from ai.llms import llm

def consultar_ou_responder(state: State):
    prompt = prompt_assistente.invoke(state['messages'][-40:])
    response = llm.bind_tools([coletar_dados_repasse]).invoke(prompt)

    return {'messages': response}