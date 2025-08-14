from ai.custom_types import State
from ai.prompts_templates import prompt_selector
from ai.llms import llm
from ai.prompts_reader import PromptChoice, prompt_index

def selector(state: State):

    list_messages = []
    index = 0
    while True:
        m = state['messages'][index]
        if m.type != "tool":
            list_messages.append(m)
        index += 1
        if (len(list_messages) >= 5) or (index >= len(state['messages'])):
            break
        
    # Cria o prompt
    prompt_with_messages = prompt_selector.invoke(list_messages)

    # Gera resposta com o modelo
    titulo_prompt = llm.with_structured_output(PromptChoice).invoke(prompt_with_messages).title

    for p in prompt_index:
        if p['title'] == titulo_prompt:
            prompt = p
            break
        else:
            prompt = "Prompt não localizado!"

    return {'prompt': prompt}