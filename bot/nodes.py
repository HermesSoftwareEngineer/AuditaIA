from custom_types import StateMessages, prompt_assistente
from llms import llm
from tools import tools
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import ToolNode

def consultar_ou_responder(state: StateMessages):
    prompt = prompt_assistente.invoke(state['messages'][-10:])
    response = llm.bind_tools(tools).invoke(prompt)
    return {'messages': response}

def responder_com_contexto(state: StateMessages):
    """Responde a mensagem do usuário com base no contexto consultado."""

    list_messages_tools = [m for m in reversed(state['messages']) if m.type == 'tool']
    docs_messages_tools = '\n\n'.join(m.content for m in reversed(list_messages_tools))

    system_message = SystemMessage(
        """
        Você é um assistente virtual que responde a perguntas sobre o sistema de gestão de prestações de conta.
        Você deve responder com base no contexto consultado. Se não houver contexto, informe que não há informações disponíveis.\n\n
        """ + docs_messages_tools + "\n\n"
    )

    conversation_messages = [
        m for m in state['messages']
        if m.type in ('system', 'human')
        or (m.type == 'ia' and not m.tool_calls)
    ]

    input_llm = [system_message] + conversation_messages

    response = llm.invoke(input_llm)
    return {'messages': response}

tools_node = ToolNode(tools)