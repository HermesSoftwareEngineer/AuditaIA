from graph import State
from graph import llm
from ai.tools.coletar_dados import coletar_dados_repasse
from ai.prompts import prompt_coletor

def coletar_dados(state: State):
    prompt = prompt_coletor.invoke(state['messages'][-10])
    response = llm.bind_tools([coletar_dados_repasse]).invoke(prompt)

    return {'messages': response}