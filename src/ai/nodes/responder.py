from ai.custom_types import State
from ai.llms import llm
from langchain_core.messages import SystemMessage, HumanMessage

def responder(state: State):
    list_messages_tools = [msg for msg in state['messages'] if msg.type == 'tool']
    docs_messages_tools = "\n\n".join(m.content for m in list_messages_tools[-20:])

    system_message = SystemMessage(
        """
        Utilize os dados disponíveis pra responder o usuário da melhor forma, segundo o que foi solicitado.
        
        Se o retorno da ferramenta for uma lista vazia ou quantidade 0, é porque não foi encontrado dados a partir dos parâmetros passados.\n\n
        """ + docs_messages_tools
    )

    conversation_messsages = [
        m for m in state['messages']
        if m.type in ('system', 'human')
        or (m.type == 'ia' and not m.tool_calls)
    ]

    prompt = [system_message] + conversation_messsages[-20:]
    
    return {'messages': llm.invoke(prompt)}