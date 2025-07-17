from graph import graph
from dotenv import load_dotenv
import os

load_dotenv()

# --- ADICIONE ESTA LINHA PARA TESTE ---
print(f"GOOGLE_APPLICATION_CREDENTIALS: {os.getenv('GOOGLE_APPLICATION_CREDENTIALS')}")
# --- FIM DO TESTE ---


config = {"configurable": {"thread_id": "1"}}
def stream_graph_update(user_input: str):
    response = graph.invoke({'messages': user_input}, config)
    print("Assistent: ", response['messages'][-1].content)

while True:
    user_input = input("User: ")
    if user_input.lower() in ['quit', 'sair', 'q']:
        break
    stream_graph_update(user_input)