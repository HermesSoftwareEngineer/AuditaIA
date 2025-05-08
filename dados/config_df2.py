import pandas as pd
from data_frames import meses2, df_mes1, df_mes2, df_proprietarios
from request_api import consultar_repasse_locador

meses = meses2

def listar_repasses(df_proprietarios, list_dfs, meses):

    df_proprietarios[f'{meses[0]}'] = ""

    # Adiciona uma nova coluna para cada mês
    for i in range(len(meses)):
        
        # Configura os valores da coluna do mês atual
        for index, row in df_proprietarios.iterrows():

            movimentos = consultar_repasse_locador(meses[i]['data_inicial'], meses[i]['data_final'], row['Proprietário'])

    
    # Calcula a diferença entre os meses
    # df_proprietarios['Diferença'] = df_proprietarios[f'{meses[1]}'] - df_proprietarios[f'{meses[0]}']
    
    print(df_proprietarios.head(100))

listar_repasses(df_proprietarios, [df_mes1, df_mes2], meses)