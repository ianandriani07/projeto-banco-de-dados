from db.connection import get_session
from sqlalchemy import select, func, Table, MetaData
from models.models import Tag, Generaluser, Post, Event, t_following, Logged, Ai, ReactedTo

def medias_curtidas_por_tag():

    with get_session() as session:

        query = session.execute(
            select(
                Tag.tag_content.label("Nome da tag"),
                func.trunc(func.avg(Post.like_count.label("Media de curtidas")))
            )
            .join(Generaluser, Tag.id_tag == Generaluser.id_tag)
            .join(Post, Generaluser.id_user == Post.id_user)
            .group_by(Tag.tag_content.label("Nome da tag"))
        ).all()

    return query

def contar_eventos_usuarios_ativos():

    with get_session() as session:
        query = session.execute(
            select(
                Event.description.label("Evento"),
                func.count()
            )
            .select_from(t_following)
            .join(Logged, Logged.id_user == t_following.c.follower)
            .join(Event, Logged.event_type == Event.event_type)
            .group_by(Event.description.label("Evento"))
        ).all()

    return query

def contar_likes_feitos_pela_ia():

    with get_session() as session:
        query = session.execute(
            select(
                Ai.model_name.label("Nome do modelo"),
                func.count()
            )
            .select_from(Ai)
            .join(Post, Ai.id_user == Post.id_user)
            .join(ReactedTo, Post.id_post == ReactedTo.id_post)
            .group_by(Ai.model_name.label("Nome do modelo"))
        ).all()

    return query

def consultar_todos_registros_tabela(nome_tabela):

    metadata = MetaData()

    with get_session() as session:
        tabela = Table("ai", metadata, autoload_with=session.bind)

        query = select(tabela)
        resultado = session.execute(query)

    return resultado

