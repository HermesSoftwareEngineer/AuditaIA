from typing import Annotated, List, Tuple
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
import operator
from pydantic import BaseModel, Field

class State(TypedDict):
    messages: Annotated[list[str], add_messages]

class PlanExecute(TypedDict):
    input: str
    plan: List[str]
    past_steps: Annotated[List[Tuple], operator.add]
    response: str

class Plan(BaseModel):
    """Planejamento pra seguir no futuro"""

    steps: List[str] = Field(
        description="diferentes etapas a seguir, devem estar em ordem classificada"
    )