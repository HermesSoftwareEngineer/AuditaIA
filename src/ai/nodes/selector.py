from ai.custom_types import State, Response_or_Query
from ai.prompts_templates import prompt_assistente
from ai.llms import llm

def consultar_ou_responder(state: State):
    prompt = prompt_assistente.invoke(state['messages'][-40:])
    response = llm.bind_tools(tools).invoke(prompt)

    return {'messages': response}