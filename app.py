from perfil import Perfil
from post import Post
from datetime import datetime

""" comentando testes de perfil
novo_perfil = Perfil(
    nome="iandev",
    seguidores=180,
    seguindo=50,
    descricao="Backend lover. Café e código ☕",
    posts= ["Aprendendo Python é como descobrir um novo mundo de possibilidades! #Python #Coding"]
)
"""
novo_post = Post(
    usuario="iandev",
    texto="Aprendendo Python é como descobrir um novo mundo de possibilidades! #Python #Coding",
    data_postagem=datetime(2025, 6, 3, 19, 12),
    likes=150,
    respostas=[
        {"autor": "maria23", "texto": "muito bom, também curto 😄", "data": datetime(2025, 6, 3, 19, 25)},
        {"autor": "coderjr", "texto": "python é top mesmo!", "data": datetime(2025, 6, 3, 19, 33)}
    ]
)

novo_post.mostrar_post()


#novo_perfil.mostrar_perfil()