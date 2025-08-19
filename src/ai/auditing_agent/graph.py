from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import tools_condition
from .custom_types import State
from .nodes.decisor import consultar_ou_responder
from .nodes.coleta import consultar
from .nodes.tools_node import toolsNode
from .nodes.responder import responder
from .nodes.selector import selector
from .nodes.verificar_prompt import verificar_prompt
from langgraph.checkpoint.sqlite import SqliteSaver
from dotenv import load_dotenv
import sqlite3

load_dotenv()

graph_builder = StateGraph(State)

graph_builder.add_node("consultar_ou_responder", consultar_ou_responder)
graph_builder.add_node("consultar", consultar)
graph_builder.add_node("responder", responder)
graph_builder.add_node("selector", selector)
graph_builder.add_node("verificar_prompt", verificar_prompt)
graph_builder.add_node("tools", toolsNode)

graph_builder.add_edge(START, "selector")
graph_builder.add_edge("selector", "consultar_ou_responder")
graph_builder.add_conditional_edges("consultar_ou_responder", tools_condition, {"tools": "tools", END: END})
graph_builder.add_edge("tools", "consultar_ou_responder")
graph_builder.add_edge("responder", END)

# cria ou conecta ao DB SQLite
conn = sqlite3.connect('langgraph_memory.db', check_same_thread=False)

# inicializa o checkpointer para persistência
# memory = SqliteSaver(conn)
memory = MemorySaver()

graph = graph_builder.compile(checkpointer=memory)