from langchain_google_vertexai import ChatVertexAI
from langchain.agents.react.agent import create_react_agent
from langchain_core.prompts import PromptTemplate
from tools import tools
from dotenv import load_dotenv

load_dotenv()

llm = ChatVertexAI(model_name="gemini-1.5-flash")