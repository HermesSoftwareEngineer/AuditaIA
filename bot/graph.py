from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from custom_types import StateMessages
from nodes import consultar_ou_responder, responder_com_contexto
from nodes import tools_node
from langgraph.prebuilt import tools_condition

graph = StateGraph(StateMessages)

graph.add_node('consultar_ou_responder', consultar_ou_responder)
graph.add_node('tools', tools_node)
graph.add_node('responder_com_contexto', responder_com_contexto)

graph.add_edge(START, 'consultar_ou_responder')
graph.add_conditional_edges('consultar_ou_responder', tools_condition, {'tools': 'tools', END: END})
graph.add_edge('tools', 'responder_com_contexto')
graph.add_edge('responder_com_contexto', END)
graph.add_edge('consultar_ou_responder', END)

memory = InMemorySaver()
app = graph.compile(checkpointer=memory)