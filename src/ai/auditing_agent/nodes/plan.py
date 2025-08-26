from ..custom_types import PlanExecute, Plan
from ..prompts_templates import planner_prompt
from ..llms import llm

def plan_step(state: PlanExecute):
    prompt = planner_prompt.invoke(state['input'])
    plan = llm.with_structured_output(Plan).invoke(prompt)

    return {"plan": plan.steps}


# state = PlanExecute({
#     "input": ["Pesquisar prestações de conta de Germana Silva Braga"]
# })
# print(plan_step(state))