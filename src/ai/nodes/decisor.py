from ai.custom_types import State, Response_or_Query
from ai.prompts_templates import prompt_assistente
from ai.tools.toolsList import toolsList
from ai.llms import llm

# Lista de tools
tools = toolsList

def consultar_ou_responder(state: State):
    conversation_messsages = [
        m for m in state['messages']
        if m.type in ('system', 'human')
        or (m.type == 'ia' and not m.tool_calls)
    ]
    
    list_messages_tools = [msg for msg in state['messages'] if msg.type == 'tool']
    docs_messages_tools = "\n\n".join(m.content for m in list_messages_tools[-20:])

    messages = conversation_messsages + list_messages_tools

    list_messages = prompt_assistente.invoke(messages)
    prompt = state['prompt'].__str__()
    messages = list_messages.__str__()
    result = messages + prompt
    response = llm.bind_tools(tools).invoke(result)

    return {'messages': response}