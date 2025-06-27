from db.connection import get_session
from models.models import Generaluser, Logged, Post, Ai
from sqlalchemy import update, MetaData, Table
from faker import Faker
from services.gerar_senha import gerar_senha

fake = Faker("pt_BR")
senha_falsa = fake.password()
senha_criptografada = gerar_senha(senha_falsa)

def executar_updates():

    with get_session() as session:
        session.execute(
            update(Generaluser)
            .where(Generaluser.id_user == 1)
            .values(
                username="ian_dev",
                password=senha_criptografada,
                email="iandriani07@gmail.com",
                description="Backend lover and coffe lover :)",
                permission_level=5,
                fake_username="ian_god",
            )
        )

        session.execute(
            update(Logged)
            .where(Logged.id_user == 1)
            .values(
                ipv4="192.168.127.12"
            )
        )

        session.execute(
            update(Post)
            .where((Post.id_user == 1) & (Post.like_count > 5))
            .values(
                text_="Meus posts mais curtidos!"
            )
        )

        session.execute(
            update(Ai)
            .where(Ai.id_user == 101)
            .values(
                temp=3.14159265358979
            )
        )

        session.commit()

        print("🔧 Updates aplicados com sucesso.")


def atualizar_tabela(nome_tabela, coluna_filtro, valor_filtro, coluna_alvo, novo_valor):

    try:
        metadata = MetaData()

        with get_session() as session:
            tabela = Table(nome_tabela.lower(), metadata, autoload_with=session.bind)

            stmt = (
                update(tabela)
                .where(tabela.c[coluna_filtro] == valor_filtro)
                .values({coluna_alvo: novo_valor})
            )

            resultado = session.execute(stmt)
            session.commit()

            print(f"✅ {resultado.rowcount} linha(s) atualizada(s) em '{nome_tabela}'")

    except Exception as e:
        print(f"Erro: {e}")