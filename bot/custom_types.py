from typing_extensions import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

class StateMessages(TypedDict):
    messages: Annotated[list[str], add_messages]

class ConsultaMovimentos(TypedDict):
    mes: int
    ano: int
    obs: Annotated[str, "Instrução usada para base da elaboração da consulta SQL. Pode colocar outros parâmetros adicionais aqui."]

class ListaConsultas(TypedDict):
    consultas: Annotated[list[ConsultaMovimentos], "Lista de consultas"]

prompt_assistente = ChatPromptTemplate.from_messages(
    [
        ('system', "Você é um assistente virtual que responde a perguntas sobre o sistema de gestão de prestações de conta."),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

class QueryOutput(TypedDict):
    """Generated SQL query."""

    query: Annotated[str, ..., "Syntactically valid SQL query."]