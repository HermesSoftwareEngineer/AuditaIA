from langgraph.graph.message import add_messages
from typing import Annotated, Any, Optional
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

class Property(BaseModel):  # Corrigido: herda de BaseModel
    id: int
    link: str
    address: str
    description: str
    price: float
    area: float
    valueM2: float

class HeaderValuation(BaseModel):  # Corrigido
    date: str
    regionAnalysis: str
    area: float
    avgM2: float
    depreciation: float
    finalAverage: float
    finalValue: float

class PropertyAssessed(BaseModel):  # Corrigido
    addressProperty: str
    area: float
    owner: str
    purpose: str
    type: str

class PropertyValuation(BaseModel):
    listProperties: list[Property] = Field(
        description="Lista de imóveis utilizados na avaliação"
    )
    header: HeaderValuation = Field(
        description="Cabeçalho da avaliação, contendo informações gerais"
    )
    propertyAssessed: PropertyAssessed = Field(
        description="Informações sobre o imóvel avaliado"
    )

class State(TypedDict):
    messages: Annotated[list[Any], add_messages]
    propertyValuation: Optional[PropertyValuation] = None