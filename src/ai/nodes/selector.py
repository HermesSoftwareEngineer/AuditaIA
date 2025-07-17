from ai.custom_types import State, Response_or_Query
from ai.prompts_templates import prompt_selector
from ai.llms import llm

def selector(state: State):
    conversation_messsages = [
        m for m in state['messages']
        if m.type in ('system', 'human')
        or (m.type == 'ia' and not m.tool_calls)
    ]

    list_messages_tools = [msg for msg in state['messages'] if msg.type == 'tool']
    docs_messages_tools = "\n\n".join(m.content for m in list_messages_tools[-20:])

    prompt = prompt_selector.invoke(docs_messages_tools + conversation_messsages)
    response = llm.invoke(prompt)

    return {'messages': response}