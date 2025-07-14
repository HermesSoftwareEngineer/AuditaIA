from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import tools_condition
from ai.custom_types import State
from ai.nodes.decisor import consultar_ou_responder
from ai.nodes.tools_node import toolsNode

graph_builder = StateGraph(State)

graph_builder.add_node("consultar_ou_responder", consultar_ou_responder)
graph_builder.add_node("tools", toolsNode)

graph_builder.add_edge(START, "consultar_ou_responder")
graph_builder.add_conditional_edges("consultar_ou_responder", tools_condition, {"tools": "tools", END: END})
graph_builder.add_edge("tools", "consultar_ou_responder")
graph_builder.add_edge("consultar_ou_responder", END)

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)