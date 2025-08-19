import sys
import os

# Caminho absoluto do diretório raiz do projeto (que contém /src)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC_DIR = os.path.join(ROOT_DIR, "src")

# Adiciona o diretório `src` ao sys.path
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)


from graph import graph
from dotenv import load_dotenv
import os

load_dotenv()

config = {"configurable": {"thread_id": "1"}}
def stream_graph_update(user_input: str):
    response = graph.invoke({'messages': user_input}, config)
    print("Assistent: ", response['messages'][-1].content)

while True:
    user_input = input("User: ")
    if user_input.lower() in ['quit', 'sair', 'q']:
        break
    stream_graph_update(user_input)