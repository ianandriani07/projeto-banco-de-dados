from old.cards import Card


class Perfil:
    def __init__(self, nome, seguidores=0, seguindo=0, descricao="", posts=None):
        self.nome = nome
        self.seguidores = seguidores
        self.seguindo = seguindo
        self.descricao = descricao
        self.posts = posts if posts is not None else []

    def mostrar_perfil(self):
        largura = 44  # Total entre as bordas ║     ║

        nome = f"@{self.nome}"
        info = (
            f"Seguidores: {self.seguidores}",
            f"Seguindo: {self.seguindo}",
            f"Posts: {len(self.posts)}",
        )
        descricao_formatada = f'"{self.descricao}"'

        if self.posts:
            ultimo_post = f'"{self.posts[-1]}"'
        else:
            ultimo_post = "Nenhum post ainda."

        print(
            Card(
                nome,
                info,
                descricao_formatada,
                ultimo_post,
                inner_card_width=largura,
            )
        )
        print("[N] Próximo  |  [V] Voltar  |  [S] Sair")
