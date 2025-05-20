from sqlalchemy.orm import Session
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy import text

def upsert_dataframe(df, table_name, engine, unique_keys=["codigo", "saldo"]):
    """
    Insere ou atualiza dados de um DataFrame em uma tabela SQLite com base em uma chave composta.

    Parâmetros:
    - df: DataFrame com os dados a serem inseridos.
    - table_name: nome da tabela no banco de dados.
    - engine: instância do SQLAlchemy engine.
    - unique_keys: lista com os nomes das colunas que compõem a chave única (ex: ['codigo', 'saldo']).
      ATENÇÃO: Deve corresponder exatamente à constraint UNIQUE ou PRIMARY KEY da tabela!
    """
    # print("Atualizando dados na tabela:", table_name)
    # print("Dados a serem atualizados:", df.head(1000))
    from sqlalchemy import MetaData

    metadata = MetaData()
    metadata.reflect(bind=engine)
    table = metadata.tables[table_name]

    # Verifica se unique_keys corresponde a uma constraint da tabela
    pk_cols = [col.name for col in table.primary_key.columns]
    if set(unique_keys) != set(pk_cols):
        print(f"AVISO: unique_keys fornecido ({unique_keys}) não corresponde à PRIMARY KEY da tabela ({pk_cols}). Isso pode causar erros de integridade.")

    # Garante que o índice UNIQUE existe (não é necessário se PRIMARY KEY já cobre, mas não faz mal)
    with engine.connect() as conn:
        unique_cols = ', '.join(unique_keys)
        idx_name = f"idx_{table_name}_{'_'.join(unique_keys)}"
        conn.execute(
            text(f"CREATE UNIQUE INDEX IF NOT EXISTS {idx_name} ON {table_name} ({unique_cols})")
        )

    with Session(engine) as session:
        for _, row in df.iterrows():
            insert_stmt = insert(table).values(**row.to_dict())
            update_dict = {col: row[col] for col in df.columns if col not in unique_keys}

            upsert_stmt = insert_stmt.on_conflict_do_update(
                index_elements=unique_keys,
                set_=update_dict
            )
            session.execute(upsert_stmt)
        session.commit()