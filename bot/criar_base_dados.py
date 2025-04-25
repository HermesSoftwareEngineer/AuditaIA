import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(f'sqlite:///prestacoes.db')
nomes_planilhas=['fev2025', 'mar2025']

for nome_planilha in nomes_planilhas:
    df = pd.read_excel(rf"C:\Users\Hermes\PROJETOS_DEV\AuditaIA\bot\{nome_planilha}.xlsx")

    df = df.drop(columns=['CodigoDetalhe', 'NumeroDocumento', 'TipoEnvolvido', 'NomeEnvolvido', 'CodigoCliente', 'CpfCliente', 'CodigoImovel', 'ResumoImovel', 'CodigoContrato', 'CodigoAuxiliarContrato', 'ResumoContrato', 'DataInclusao', 'DataVencimento', 'DataPagamento', 'DataPagamento', 'DataVencimentoBoleto', 'CodigoAuxiliarPlanoConta', 'CentroCusto', 'DataConciliacao', 'DataConciliacao', 'DataConciliacao', 'UnidadeCodigo', 'UnidadeNome'])

    # print(df.head())

    df.to_sql(f"{nome_planilha}", con=engine, if_exists="replace", index=False)