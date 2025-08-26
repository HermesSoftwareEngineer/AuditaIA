from ..customTypes import State
from ..prompts_templates import prompt_pesquisador
from ..tools.tools_list import toolsList
from ai.llms import llm

def query_or_answer(state: State):
    conversation_messsages = [
        m for m in state['messages']
        if m.type in ('system', 'human')
        or (m.type == 'ia' and not m.tool_calls)
    ]
    
    list_messages_tools = [msg for msg in state['messages'] if msg.type == 'tool']

    messages = conversation_messsages + list_messages_tools

    list_messages = prompt_pesquisador.invoke(messages)

    response = llm.bind_tools(toolsList).invoke(list_messages)

    return {'messages': response}