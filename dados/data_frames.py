import pandas as pd

meses2 = [
    {
        "mes": "Janeiro2025",
        "data_inicial": "01/02/2025",
        "data_final": "28/02/2025",
    },
    {
        "mes": "Fevereiro2025",
        "data_inicial": "01/03/2025",
        "data_final": "31/03/2025",
    },
]

meses = ['fev2025', 'mar2025']

df_mes1 = pd.read_excel(r"dados/repasses.xlsx", sheet_name=f"{meses[0]}")
df_mes2 = pd.read_excel(r"dados/repasses.xlsx", sheet_name=f"{meses[1]}")
df_proprietarios = pd.read_excel(r"dados/LISTA_DE_PROPRIETÁRIOS.xlsx")