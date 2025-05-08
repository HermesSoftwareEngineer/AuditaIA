import pandas as pd
from data_frames import meses, df_mes1, df_mes2, df_proprietarios

def listar_repasses(df_proprietarios, list_dfs, meses):

    df_proprietarios[f'{meses[0]}'] = ""

    # Adiciona uma nova coluna para cada mês
    for i in range(len(list_dfs)):
        df = list_dfs[i]
        
        # Configura os valores da coluna do mês atual
        for index, row in df_proprietarios.iterrows():

            if row['Proprietário'] in df['Proprietário'].values:
                index_prop = df.index[df['Proprietário'] == row['Proprietário']].tolist()[0]
                df_proprietarios.loc[index_prop, f'{meses[i]}'] = df.loc[index_prop, 'Valor']
            else:
                df_proprietarios.loc[index_prop, f'{meses[i]}'] = "NaN"
                print("Não encontrado: ", row['Proprietário'])
    
    # Calcula a diferença entre os meses
    df_proprietarios['Diferença'] = df_proprietarios[f'{meses[1]}'] - df_proprietarios[f'{meses[0]}']
    
    print(df_proprietarios.head(100))

listar_repasses(df_proprietarios, [df_mes1, df_mes2], meses)