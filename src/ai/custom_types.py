from typing import Annotated, List, Tuple
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
import operator
from pydantic import BaseModel, Field

class State(TypedDict):
    messages: Annotated[list[str], add_messages]
    selected_prompt_id: int
    prompt: str

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

class Response_or_Query(BaseModel):
    """Consultar ou responder"""

    content: str = Field(
        description="conteúdo da resposta pra caso queira responder"
    )

    query: bool = Field(
        description="True para caso queira consultar, ou false para caso queira responder"
    )

class PromptID(BaseModel):
    
    prompt: int = Field(
        description="Número do prompt escolhido"
    )