from models.models import *
from services.gerar_senha import gerar_senha
from db.connection import get_session
import getpass
from utils.helpers import maior_id


def gerar_usuario():

    username = input("Digite o nome de usuário: ")
    email = input("Digite o email do usuário: ")
    description = input("Digite a descrição do usuário: ")
    permission_level = int(input("Digite o nível de permissão do usuário (1-5): "))
    fake_username = input("Digite o nome de usuário falso (opcional): ")
    senha = getpass.getpass("Digite a senha do usuário: ")
    id_tag_input = input("Digite o ID da tag (opcional): ")

    with get_session() as session:

        id_usuario = maior_id(Generaluser, "id_user")

        user = Generaluser(
            id_user=id_usuario,
            username=username,
            password=gerar_senha(senha),
            email=email,
            description=description,
            permission_level=permission_level,
            fake_username=fake_username if fake_username else None,
            id_tag = int(id_tag_input) if id_tag_input.strip() else None
        )

        try:
            session.add(user)
            session.commit()
            print("✅ Usuário adicionado com sucesso!")
        except Exception as e:
            return f"❌ Erro ao adicionar usuário: {e}"

def gerar_evento():
    descricao = input("Digite a descrição do evento: ")

    with get_session() as session:
        id_evento = maior_id(Event, "event_type")

        evento = Event(
            event_type=id_evento,
            description=descricao
        )

        try:
            session.add(evento)
            session.commit()
            print("✅ Evento adicionado com sucesso!")
        except Exception as e:
            print(f"Erro ao adicionar evento: {e}")

def gerar_tag():
    tag_content = input("Digite o conteúdo da tag: ")
    color = int(input("Digite o código de cor (int): "))

    with get_session() as session:
        id_tag = maior_id(Tag, "id_tag")

        tag = Tag(
            id_tag=id_tag,
            tag_content=tag_content,
            color=color
        )

        try:
            session.add(tag)
            session.commit()
            print("✅ Tag adicionada com sucesso!")
        except Exception as e:
            print(f"Erro ao adicionar tag: {e}")


from datetime import datetime


def gerar_ai_verified():
    id_user = int(input("Digite o ID do usuário (deve já existir na tabela GeneralUser): "))
    last_profile_change = input("Última alteração de perfil (YYYY-MM-DD HH:MM:SS): ")

    with get_session() as session:
        verificado = Aiverified(
            id_user=id_user,
            last_profile_change=datetime.strptime(last_profile_change, "%Y-%m-%d %H:%M:%S")
        )

        try:
            session.add(verificado)
            session.commit()
            print("✅ Verificação IA adicionada com sucesso!")
        except Exception as e:
            print(f"Erro ao adicionar verificação IA: {e}")

def gerar_ai():
    id_user = int(input("Digite o ID do usuário (deve já existir): "))
    model_name = input("Digite o nome do modelo IA: ")
    prompt = input("Digite o prompt padrão: ")
    max_comment_length = int(input("Máximo de caracteres no comentário: "))
    comments_context_size = int(input("Tamanho do contexto: "))
    temp = float(input("Temperatura do modelo (ex: 0.7): "))
    min_p = float(input("Valor mínimo de p (ex: 0.1): "))

    with get_session() as session:
        ai = Ai(
            id_user=id_user,
            model_name=model_name,
            prompt=prompt,
            max_comment_length=max_comment_length,
            comments_context_size=comments_context_size,
            temp=temp,
            min_p=min_p
        )

        try:
            session.add(ai)
            session.commit()
            print("✅ IA adicionada com sucesso!")
        except Exception as e:
            print(f"Erro ao adicionar IA: {e}")

def gerar_post():
    text = input("Digite o texto do post: ")
    id_user = int(input("Digite o ID do autor: "))
    is_reply = input("É uma resposta? (s/n): ").lower().startswith("s")
    is_trending = input("Está em alta? (s/n): ").lower().startswith("s")

    with get_session() as session:
        id_post = maior_id(Post, "id_post")

        post = Post(
            id_post=id_post,
            text_=text,
            time=datetime.now(),
            like_count=0,
            is_reply=is_reply,
            is_trending=is_trending,
            id_user=id_user
        )

        try:
            session.add(post)
            session.commit()
            print("✅ Post inserido com sucesso!")
        except Exception as e:
            print(f"Erro ao adicionar post: {e}")

def gerar_log():
    id_user = int(input("ID do usuário: "))
    event_type = int(input("Tipo do evento (Event_Type): "))
    ipv4 = input("IPv4 (ex: 192.168.0.1): ")
    page = input("Página acessada (opcional): ")

    with get_session() as session:
        id_logged = maior_id(Logged, "id_logged")

        log = Logged(
            id_logged=id_logged,
            time=datetime.now(),
            ipv4=ipv4,
            page=page if page else None,
            id_user=id_user,
            event_type=event_type
        )

        try:
            session.add(log)
            session.commit()
            print("✅ Log inserido com sucesso!")
        except Exception as e:
            print(f"Erro ao inserir log: {e}")

def gerar_seguindo_seguidores():
    follower = int(input("ID de quem está seguindo (follower): "))
    following = int(input("ID de quem está sendo seguido (following): "))

    with get_session() as session:
        relacao = t_following(
            follower=follower,
            following=following
        )

        try:
            session.add(relacao)
            session.commit()
            print("✅ Relação de seguir adicionada com sucesso!")
        except Exception as e:
            print(f"Erro ao adicionar relação: {e}")


def gerar_reacao():
    id_user = int(input("ID do usuário: "))
    id_post = int(input("ID do post: "))
    liked = input("Curtiu? (s/n): ").lower().startswith("s")

    with get_session() as session:
        reacao = ReactedTo(
            id_user=id_user,
            id_post=id_post,
            liked=liked
        )

        try:
            session.add(reacao)
            session.commit()
            print("✅ Reação adicionada com sucesso!")
        except Exception as e:
            print(f"Erro ao adicionar reação: {e}")
