from sqlalchemy import inspect, select, Table, MetaData
from db.connection import get_session
from sqlalchemy.orm import aliased

def maior_id(nome_tabela, nome_pk):

    with get_session() as session:

        pk_coluna = getattr(nome_tabela, nome_pk)

        verificar_id = session.execute(
            select(nome_tabela).order_by(pk_coluna.desc())
        ).first()

        if verificar_id:
            usuario = verificar_id[0]

            return getattr(usuario, nome_pk) + 1
        else:
            return 1

def mostra_todas_tabelas():
    with get_session() as session:

        insp = inspect(session.bind)

        return insp.get_table_names()

def estrutura_tabelas(nome_tabela):
    with get_session() as session:

        insp = inspect(session.bind)
        colunas = insp.get_columns(nome_tabela.lower())

        return colunas
