from ai.prompts_reader import prompts_list
from ai.custom_types import State

def verificar_prompt(state: State): 
    id = state['selected_prompt_id']
    prompt = prompts_list[id-1]
    return {"prompt": prompt}