from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv
from langgraph.prebuilt import tools_condition

from .nodes.tools_node import toolsNode
from .nodes.answer import answer
from .nodes.query_or_answer import query_or_answer
from .nodes.organize_evaluation import organize_evaluation
from .customTypes import State

load_dotenv()

graph_builder = StateGraph(State)

# Nós e arestas do grafo
graph_builder.add_node("query_or_answer", query_or_answer)
graph_builder.add_node("organize_evaluation", organize_evaluation)
graph_builder.add_node("answer", answer)
graph_builder.add_node("tools", toolsNode)

graph_builder.add_edge(START, "query_or_answer")
graph_builder.add_conditional_edges("query_or_answer", tools_condition, {"tools": "tools", END: END})
graph_builder.add_edge("tools", "organize_evaluation")
graph_builder.add_edge("organize_evaluation", "answer")
graph_builder.add_conditional_edges("answer", tools_condition, {"tools": "tools", END: END})

memory = MemorySaver()

graph = graph_builder.compile(checkpointer=memory)