from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from custom_types import StateMessages
from nodes import consultar_ou_responder

graph = StateGraph(StateMessages)

graph.add_node('consultar_ou_responder', consultar_ou_responder)

graph.add_edge(START, 'consultar_ou_responder')
graph.add_edge('consultar_ou_responder', END)

memory = InMemorySaver()
app = graph.compile(checkpointer=memory)