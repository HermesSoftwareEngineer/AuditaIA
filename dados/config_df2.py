import pandas as pd
from data_frames import meses2, df_mes1, df_mes2, df_proprietarios
from request_api import consultar_repasse_locador
from engine import engine
from manipular_engine import upsert_dataframe

meses = meses2

def salvar_movimentos(data):
    movimentos = []
    detalhes = []
    for item in data["lista"]:
        movimento_id = item["codigo"]

        movimento = item.copy()

        detalhes_raw = movimento.pop("detalhes", [])

        movimento.pop("formasquitacao", None)
        movimento.pop("repasses", None)

        movimentos.append(movimento)

        for detalhe in detalhes_raw:
            detalhe['movimento_id'] = movimento_id
            detalhes.append(detalhe)

    df_movimentos = pd.DataFrame(movimentos)
    df_detalhes = pd.DataFrame(detalhes)

    upsert_dataframe(df_movimentos, 'movimentos', engine, 'codigo')
    # upsert_dataframe(df_detalhes, 'detalhes', engine, 'codigodetalhe')

def listar_repasses(df_proprietarios, list_dfs, meses):

    # Adiciona uma nova coluna para cada mês
    for i in range(len(meses)):

        df_proprietarios[f'{meses[i]["mes"]}'] = ""
        
        # Configura os valores da coluna do mês atual
        for index, row in df_proprietarios.iterrows():

            movimentos = consultar_repasse_locador(meses[i]['data_inicial'], meses[i]['data_final'], row['Proprietário'])
            salvar_movimentos(movimentos)
    
    # Calcula a diferença entre os meses
    # df_proprietarios['Diferença'] = df_proprietarios[f'{meses[1]}'] - df_proprietarios[f'{meses[0]}']
    
    print(df_proprietarios.head(100))

listar_repasses(df_proprietarios, [df_mes1, df_mes2], meses)