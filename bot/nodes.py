from custom_types import StateMessages
from llms import llm
from tools import tools

def consultar_ou_responder(state: StateMessages):
    response = llm.bind_tools(tools).invoke(state['messages'][-1].content)
    return {'messages': response}