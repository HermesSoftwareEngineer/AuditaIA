from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_google_vertexai import ChatVertexAI
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv

load_dotenv()

llm = ChatVertexAI(model_name="gemini-2.0-flash")

class State(TypedDict):
    messages: Annotated[list[str], add_messages]

graph_builder = StateGraph(State)

def responder(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

graph_builder.add_node("responder", responder)

graph_builder.add_edge(START, "responder")
graph_builder.add_edge("responder", END)

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)