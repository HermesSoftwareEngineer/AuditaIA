from ..tools.webSearchTools import web_search_properties
from ..customTypes import State
from ..tools.tools_list import toolsList
from ai.llms import llm
from langchain_core.messages import SystemMessage

def answer(state: State):
    # list_messages_tools = [msg for msg in state['messages'] if msg.type == 'tool']
    # docs_messages_tools = "\n\n".join(m.content for m in list_messages_tools[-20:])

    system_message = SystemMessage(
        f"""
        Utilize os dados disponíveis pra responder o usuário da melhor forma, fornecendo os dados da avaliação realizada.
        
        Dados da avaliação: 
        {state['propertyValuation']}
        """
    )

    conversation_messsages = [
        m for m in state['messages']
        if m.type in ('system', 'human')
        or (m.type == 'ia' and not m.tool_calls)
    ]

    prompt = [system_message] + conversation_messsages[-20:]
    
    return {'messages': llm.bind_tools(toolsList).invoke(prompt)}