from db.connection import get_session
from ai.cache import create_vec_database
from ai.bot import UserID
from sqlalchemy import select, func, Table, MetaData
from models.models import Tag, Generaluser, Post, Event, t_following, Logged, Ai, ReactedTo
from typing import List, Tuple

UserInfo = Tuple[int, str, str]
Posts = Tuple[str]


def get_all_user_info():
    with get_session() as session:
        ai_subquery = select(Ai.id_user)

        query = session.execute(
            select(
                Generaluser.id_user,
                Generaluser.username,
                Generaluser.description
            ).where(~Generaluser.id_user.in_(ai_subquery))
        ).all()
    return query

def get_posts_by_user(user_id: int):
    with get_session() as session:
        query = session.execute(
            select(
                Post.text_,
            )
            .where(Post.id_user == user_id)
            .limit(20)
        ).all()
    return query

unwrap = lambda x: x[0]

def extend_info_with_posts(info: UserInfo) -> UserID:
    user_id = info[0]
    return UserID(user_id, info[1], info[2], list(map(unwrap, get_posts_by_user(user_id))))

def insert_user_info_in_qdrant():
    database = create_vec_database()

    for user in map(extend_info_with_posts, get_all_user_info()):
        try:
            database.save_embedding(user)
            print(f"✅ IA: Usuário {user.username} processado com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao processar usuário: {e}")
            break