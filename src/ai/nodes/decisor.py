from ai.custom_types import State, Response_or_Query
from ai.prompts_templates import prompt_assistente
from ai.tools.toolsList import toolsList
from ai.llms import llm

# Lista de tools
tools = toolsList

def consultar_ou_responder(state: State):
    messagesConversation = [m for m in state['messages'][-20:] if m.type != "tool"]
    tools_messages = [m for m in state['messages'][-20:] if m.type == "tool"]
    messages = messagesConversation + tools_messages
    list_messages = prompt_assistente.invoke(messages)
    prompt = state['prompt'].__str__()
    messages = list_messages.__str__()
    result = messages + prompt
    response = llm.bind_tools(tools).invoke(result)

    return {'messages': response}