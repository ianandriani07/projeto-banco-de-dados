from sqlalchemy import delete, select, MetaData, Table, insert
from models.models import ReactedTo, Post, Ai, Logged
from db.connection import get_session

def executar_deletes():

    with get_session() as session:

        ids_posts_com_ate_3_likes = session.execute(
            select(Post.id_post)
            .where(
                (Post.id_user == 50) & (Post.like_count <= 3)
            )
        ).scalars().all()

        session.execute(
            delete(ReactedTo)
            .where(ReactedTo.id_post.in_(ids_posts_com_ate_3_likes))
        )

        session.execute(
            delete(Post)
            .where(Post.id_post.in_(ids_posts_com_ate_3_likes))
        )

        session.execute(
            delete(Logged)
            .where(Logged.event_type == 9)
        )

        session.execute(
            delete(Ai)
            .where(Ai.id_user == 103)
        )

        session.commit()
        print("🧹 Dados deletados com sucesso.")

def deletar_por_id(nome_tabela, nome_coluna_id, valor_id):

    try:
        metadata = MetaData()

        with get_session() as session:
            tabela = Table(nome_tabela.lower(), metadata, autoload_with=session.bind)

            stmt = delete(tabela).where(tabela.c[nome_coluna_id] == valor_id)

            resultado = session.execute(stmt)
            session.commit()

            print(f"{resultado.rowcount} registro(s) deletado(s) da tabela '{nome_tabela}'")

    except Exception as e:
        print(f"Erro: {e}")