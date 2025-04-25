from langchain_core .tools import tool
from custom_types import ConsultaMovimentos
from langchain_core.messages import SystemMessage
from llms import llm
from sqlalchemy import MetaData
from langchain import hub
from criar_base_dados import engine as db
from custom_types import QueryOutput
import pandas as pd

@tool
def consultar_movimentos(consulta: ConsultaMovimentos):
    """Use esta ferramenta para consultar movimentos das prestações de conta com base nos critérios fornecidos pelo usuário."""
    metadata = MetaData()
    metadata.reflect(bind=db) 
    table_info = {table.name: [col.name for col in table.columns] for table in metadata.sorted_tables}

    query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")

    input_customize = input + "\n\nRetorne os dados apropriadamente.'"
    prompt = query_prompt_template.invoke(
        {
            "dialect": db.engine.name,
            "top_k": 5,
            "table_info": table_info,
            "input": input_customize
        }
    )

    query = llm.with_structured_output(QueryOutput).invoke(prompt)
    print(f"query gerada: {query['query']}")

    df_filtrado = pd.read_sql(query["query"], con=db)
    
    if df_filtrado.empty:
        return {"result": "Nenhum movimento encontrado para os critérios fornecidos."}

    result = df_filtrado.to_string()
    print(f"Resultado: {result}")

    return {"result": result}

tools = [consultar_movimentos]