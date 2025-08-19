from ..tools.webSearchTools import web_search_properties
from ..customTypes import State, PropertyValuation
from ..prompts_templates import prompt_avaliador
from ai.llms import llm

def organize_evaluation(state: State):
    # Mensagens do usuário e sistema
    conversation_messages = [
        m for m in state['messages']
        if m.type in ('system', 'human')
        or (m.type == 'ia' and not m.tool_calls)
    ]
    # Mensagens de chamada de ferramenta (ia com tool_calls)
    ia_tool_calls = [m for m in state['messages'] if m.type == 'ia' and m.tool_calls]
    # Mensagens de resposta de ferramenta
    tool_responses = [m for m in state['messages'] if m.type == 'tool']

    # Garante que cada chamada de ferramenta tenha uma resposta correspondente
    merged_messages = []
    for m in state['messages']:
        if m.type in ('system', 'human'):
            merged_messages.append(m)
        elif m.type == 'ia' and m.tool_calls:
            merged_messages.append(m)
            # Adiciona a resposta da ferramenta correspondente logo após a chamada
            for call in m.tool_calls:
                # Busca a resposta da ferramenta pelo id da chamada
                resp = next((t for t in tool_responses if getattr(t, 'tool_call_id', None) == call.id), None)
                if resp:
                    merged_messages.append(resp)
        elif m.type == 'ia' and not m.tool_calls:
            merged_messages.append(m)

    list_messages = prompt_avaliador.invoke(merged_messages)
    response = llm.with_structured_output(PropertyValuation).invoke(list_messages)
    return {"propertyValuation": response}