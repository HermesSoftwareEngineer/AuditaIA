from sqlalchemy import create_engine, MetaData, Table, Column
from sqlalchemy import Integer, String, Float, Date, DateTime, Text, BigInteger, Boolean 
from sqlalchemy.orm import declarative_base

engine = create_engine("sqlite:///movimentos.db")
metadata = MetaData()

movimentos_table = Table(
    "movimentos",
    metadata,
    Column("codigo", BigInteger, primary_key=True),  # <- necessário para ON CONFLICT
    Column("codigoauxiliar", String),
    Column("unidadecodigo", Integer),
    Column("unidade", String),
    Column("modulo", Integer),
    Column("tipocliente", String),
    Column("codigocliente", Integer),
    Column("nomecliente", String),
    Column("codigocontratoaluguel", Integer),
    Column("codigocontratovenda", Integer),
    Column("codigoimovel", Integer),
    Column("numerodocumento", String),
    Column("historico", Text),
    Column("linhadigitavel", String),
    Column("datahorainclusao", String),  # pode ser trocado para Date se quiser validar datas
    Column("datahoraultimaalteracao", String),
    Column("datavencimento", String),
    Column("datapagamento", String),
    Column("saldo", String)  # pode ser trocado para Float se quiser operações matemáticas
)

detalhes_table = Table(
    "detalhes",
    metadata,
    Column("codigodetalhe", BigInteger, primary_key=True),  # chave primária
    Column("codigoplanoconta", Integer),
    Column("nomeplanoconta", String),
    Column("codigocontabilplanoconta", String),
    Column("descricao", Text),
    Column("observacao", Text),
    Column("valor", String),
    Column("deduzirir", Boolean),
    Column("movimento_id", BigInteger)
)

metadata.create_all(engine)