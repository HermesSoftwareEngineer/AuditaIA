from sqlalchemy.orm import Session
from sqlalchemy.dialects.sqlite import insert

def upsert_dataframe(df, table_name, engine, unique_key):
    """
    Insere ou atualiza dados de um DataFrame em uma tabela SQLite com base em uma chave única.

    Parâmetros:
    - df: DataFrame com os dados a serem inseridos.
    - table_name: nome da tabela no banco de dados.
    - engine: instância do SQLAlchemy engine.
    - unique_key: nome da coluna que deve ser usada como chave única (precisa ser PRIMARY KEY ou UNIQUE).
    """
    from sqlalchemy import MetaData

    metadata = MetaData()
    metadata.reflect(bind=engine)
    table = metadata.tables[table_name]

    with Session(engine) as session:
        for _, row in df.iterrows():
            insert_stmt = insert(table).values(**row.to_dict())
            update_dict = {col: row[col] for col in df.columns if col != unique_key}

            upsert_stmt = insert_stmt.on_conflict_do_update(
                index_elements=[unique_key],
                set_=update_dict
            )
            session.execute(upsert_stmt)
        session.commit()