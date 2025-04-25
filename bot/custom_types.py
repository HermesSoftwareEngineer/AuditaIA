from typing_extensions import TypedDict, Annotated
from langgraph.graph.message import add_messages

class StateMessages(TypedDict):
    messages: Annotated[list[str], add_messages]

class ConsultaMovimentos(TypedDict):
    mes: int
    ano: int
    input: Annotated[str, "Instrução usada para base da elaboração da consulta SQL"]

class QueryOutput(TypedDict):
    """Generated SQL query."""

    query: Annotated[str, ..., "Syntactically valid SQL query."]