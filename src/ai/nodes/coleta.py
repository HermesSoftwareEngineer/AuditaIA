from ai.custom_types import State
from ai.prompts_templates import prompt_consultor
from ai.tools.toolsList import toolsList
from ai.llms import llm

# Lista de tools
tools = toolsList

def consultar(state: State):
    prompt = prompt_consultor.invoke(state['messages'][-20:])
    response = llm.bind_tools(tools, tool_choice='any').invoke(prompt)

    return {'messages': response}