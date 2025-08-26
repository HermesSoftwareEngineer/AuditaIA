from langchain_core.tools import tool
from ai.evaluating_agent.graph import graph

@tool
def avaliar_imovel(query: str, thread_id: str) -> str:
    """
    Avalia o valor de um imóvel com base em uma consulta.
    
    Args:
        query (str): A consulta para avaliar o imóvel.
        thread_id (str): O ID da thread da avaliação.

    Returns:
        str: O resultado da avaliação do imóvel.
    """

    # Executa o grafo de avaliação
    config = {"configurable": {"thread_id": thread_id}}
    agent_output = graph.invoke({"messages": query}, config)
    return agent_output
