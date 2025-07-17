from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import tools_condition
from ai.custom_types import State
from ai.nodes.decisor import consultar_ou_responder
from ai.nodes.coleta import consultar
from ai.nodes.tools_node import toolsNode
from ai.nodes.responder import responder

def verificar_query(state):
    query = state.get('query')
    content = state.get('content')
    return 'consultar' if query else 'responder'

graph_builder = StateGraph(State)

graph_builder.add_node("consultar_ou_responder", consultar_ou_responder)
graph_builder.add_node("consultar", consultar)
graph_builder.add_node("responder", responder)
graph_builder.add_node("tools", toolsNode)

graph_builder.add_edge(START, "consultar_ou_responder")
graph_builder.add_conditional_edges("consultar_ou_responder", tools_condition, {"tools": "tools", END: END})
graph_builder.add_edge("tools", "responder")
graph_builder.add_edge("responder", END)

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)