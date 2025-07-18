from ai.custom_types import State
from ai.prompts_templates import prompt_selector
from ai.llms import llm
from ai.custom_types import PromptID

def selector(state: State):

    # Últimas 40 mensagens da conversa
    list_messages = [msg for msg in state['messages']]

    # Cria o prompt
    prompt = prompt_selector.invoke(list_messages)

    # Gera resposta com o modelo
    response_prompt_id: PromptID = llm.with_structured_output(PromptID).invoke(prompt)

    return {'selected_prompt_id': response_prompt_id.prompt}