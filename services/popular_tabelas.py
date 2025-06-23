from faker import Faker
from services.gerar_senha import gerar_senha
from datetime import datetime as dt, timedelta
import random
from sqlalchemy import insert, func
from db.connection import get_session
from models.models import *

fake = Faker("pt_BR")
now = dt.now()

def popular_tabelas_fake(
    num_users_gerais=3,
    num_users_ia=2,
    num_tags=5,
    num_posts=5,
    num_logs=5,
    num_relacoes=5,
    num_reacoes=5,
):
    try:
        with get_session() as session:
            print("Inserindo eventos...")
            eventos = [
                "Login", "Logout", "Cadastro", "Criação de post", "Edição de post", "Exclusão de post",
                "Curtir post", "Descurtir post", "Seguir usuário", "Deixar de seguir usuário",
                "Verificação por IA", "Atualização de perfil", "Criação de usuário IA",
                "Acesso a página pública de perfil", "Logout automático por inatividade"
            ]
            event_objs = [Event(event_type=i + 1, description=desc) for i, desc in enumerate(eventos)]
            session.add_all(event_objs)

            print("Inserindo tags...")
            last_tag_id = session.query(func.max(Tag.id_tag)).scalar() or 0
            tags = []
            for i in range(num_tags):
                tag = Tag(
                    id_tag=last_tag_id + i + 1,
                    tag_content=fake.word(),
                    color=random.randint(10000, 999999)
                )
                tags.append(tag)
            session.add_all(tags)

            print("Inserindo usuários (gerais, IA e verificados)...")
            last_user_id = session.query(func.max(Generaluser.id_user)).scalar() or 0
            all_users = []

            for i in range(num_users_gerais):
                user_id = last_user_id + i + 1
                senha_falsa = fake.password()
                senha_hash = gerar_senha(senha_falsa)
                user = Generaluser(
                    id_user=user_id,
                    username=fake.user_name(),
                    password=senha_hash,
                    email=fake.email(),
                    description=fake.sentence(),
                    permission_level=random.randint(0, 2),
                    fake_username=fake.user_name() + "_fake",
                    id_tag=random.choice(tags).id_tag
                )
                all_users.append(user)
                print(f"✅ Usuário geral gerado: {user.username} | ID: {user_id} | Senha: {senha_falsa}")

            session.add_all(all_users)
            session.flush()
            users = list(all_users)

            for i in range(num_users_ia):
                user_id = last_user_id + num_users_gerais + i + 1
                senha_falsa = fake.password()
                senha_hash = gerar_senha(senha_falsa)

                ai_user = Ai(
                    id_user=user_id,
                    username=fake.user_name(),
                    password=senha_hash,
                    email=fake.email(),
                    description=fake.sentence(),
                    permission_level=1,
                    fake_username=fake.user_name() + "_fake",
                    id_tag=random.choice(tags).id_tag,
                    model_name=fake.domain_word() + "-AI",
                    prompt=fake.sentence(),
                    max_comment_length=random.randint(100, 300),
                    comments_context_size=random.randint(5, 20),
                    temp=round(fake.pyfloat(left_digits=1, right_digits=2, positive=True), 2),
                    min_p=round(fake.pyfloat(left_digits=1, right_digits=2, positive=True), 2),
                )

                session.add(ai_user)
                session.flush()

                ai_verified = Aiverified(
                    id_user=ai_user.id_user,
                    last_profile_change=now - timedelta(days=random.randint(1, 100)),
                    last_post_time=now - timedelta(days=random.randint(1, 50)),
                    last_ai_verification=now - timedelta(days=random.randint(1, 25)),
                )

                session.add(ai_verified)
                users.append(ai_user)

                print(f"✅ Usuário IA/Verificado gerado: {ai_user.username} | ID: {ai_user.id_user} | Senha: {senha_falsa}")

            print("Inserindo posts...")
            last_post_id = session.query(func.max(Post.id_post)).scalar() or 0
            posts = []
            for i in range(num_posts):
                posts.append(Post(
                    id_post=last_post_id + i + 1,
                    text_=fake.sentence(),
                    time=now - timedelta(days=random.randint(0, 30)),
                    like_count=random.randint(0, 10),
                    is_reply=False,
                    is_trending=random.choice([True, False]),
                    id_user=random.choice(users).id_user
                ))
            session.add_all(posts)

            print("Inserindo logs de acesso...")
            last_log_id = session.query(func.max(Logged.id_logged)).scalar() or 0
            logs = []
            for i in range(num_logs):
                logs.append(Logged(
                    id_logged=last_log_id + i + 1,
                    time=now - timedelta(minutes=random.randint(0, 5000)),
                    ipv4=fake.ipv4(),
                    page=fake.uri_path(),
                    id_user=random.choice(users).id_user,
                    event_type=random.randint(1, len(eventos))
                ))
            session.add_all(logs)

            print("Inserindo relações de seguidores...")
            relations = set()
            while len(relations) < num_relacoes:
                f1, f2 = random.sample(users, 2)
                if f1.id_user != f2.id_user:
                    relations.add((f1.id_user, f2.id_user))
            session.execute(insert(t_following), [
                {"following": f1, "follower": f2} for f1, f2 in relations
            ])

            print("Inserindo reações aos posts...")
            reacoes = set()


            while len(reacoes) < num_reacoes:
                user = random.choice(users).id_user
                post = random.choice(posts).id_post
                key = (user, post)
                if key not in reacoes:
                    reacoes.add(key)
                    session.add(ReactedTo(
                        id_user=user,
                        id_post=post,
                        liked=random.choice([True, False])
                    ))

            session.commit()
            print("✅ Banco populado com sucesso com dados fakes!")

    except Exception as e:
        session.rollback()
        print(f"❌ Erro: {e}")