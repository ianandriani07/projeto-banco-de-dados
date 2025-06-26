from db.connection import get_session
from ai.cache import create_vec_database
from ai.bot import UserID
from sqlalchemy import select, func, Table, MetaData
from models.models import Tag, Generaluser, Post, Event, t_following, Logged, Ai, ReactedTo
from typing import List, Tuple
from utils.post import Post
from utils.perfil import Perfil

def get_similar_users():
    db = create_vec_database()

    user_id = int(input("Digite o ID do usuário (deve já existir na tabela GeneralUser): "))

    with get_session() as session:
        result = db.search_similar_texts_by_user_id(user_id)

        if result is None:
            print('❌ Usuário inexistente!')
            return
        
        self_result, result = result[0], result[1]

        main_user = UserID(**self_result.payload)
        
        print('USUÁRIO SELECIONADO:')
        print(Perfil(main_user.username, main_user.description, posts=main_user.posts).as_card())
        print('*******************************')

        print('USUÁRIOS RECOMENDADOS:')
        for r in result:
            user = UserID(**r.payload)
            print(Perfil(user.username, user.description, posts=user.posts, compatibility=r.score).as_card())

        print('*******************************')
        
