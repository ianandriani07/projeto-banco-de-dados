from utils.cards import Card
from typing import Optional

class Perfil:
    def __init__(self, nome, descricao="", posts=None, compatibility: Optional[float] = None):
        self.nome = nome
        self.descricao = descricao
        self.compatibility = compatibility
        self.posts = posts if posts is not None else []

    def as_card(self):
        largura = 44  # Total entre as bordas ║     ║

        nome = f"@{self.nome}"
        info = [
            f"Posts Avaliados: {len(self.posts)}",
        ]

        if self.compatibility is not None:
            info = [f"Compatibilidade: {int(self.compatibility * 100)}%"] + info

        info = tuple(info)

        descricao_formatada = f'"{self.descricao}"'

        if self.posts:
            ultimo_post = f'"{self.posts[-1]}"'
        else:
            ultimo_post = "Nenhum post ainda."

        return Card(
            nome,
            info,
            descricao_formatada,
            ultimo_post,
            inner_card_width=largura,
        )
