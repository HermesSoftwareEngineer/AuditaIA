from langchain_google_vertexai import ChatVertexAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatVertexAI(model_name="gemini-1.5-flash")