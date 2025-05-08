from langchain_core .tools import tool
from custom_types import ConsultaMovimentos, ListaConsultas
from langchain_core.messages import SystemMessage
from llms import llm
from sqlalchemy import MetaData
from langchain import hub
from criar_base_dados import engine as db
from custom_types import QueryOutput
import pandas as pd

@tool
def consultar_movimentos(input: ListaConsultas) -> list:
    """Use esta ferramenta para consultar movimentos das prestações de conta com base nos critérios fornecidos pelo usuário."""
    response = []
    for consulta in input["consultas"]:
        print("TOOL CONSULTAR MOVIMENTOS FOI CHAMADA!")
        metadata = MetaData()
        metadata.reflect(bind=db) 
        table_info = {table.name: [col.name for col in table.columns] for table in metadata.sorted_tables}

        query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")

        input_customize = f"Ano: {consulta['ano']}, mês: {consulta['mes']} obs adicional: {consulta['obs']}" + "\n\nRetorne os dados apropriadamente.'"
        prompt = query_prompt_template.invoke(
            {
                "dialect": db.engine.name,
                "top_k": 100,
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
        print(f"Resultado de {consulta}: {result}")
        response.append(result)

    return {"response": response}

tools = [consultar_movimentos]