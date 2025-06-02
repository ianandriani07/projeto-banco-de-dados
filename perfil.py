import textwrap

class Perfil:
    def __init__(self, nome, seguidores=0, seguindo=0, descricao="", posts=None):
        self.nome = nome
        self.seguidores = seguidores
        self.seguindo = seguindo
        self.descricao = descricao
        self.posts = posts if posts is not None else []
        

    def mostrar_perfil(self):
        largura = 44  # Total entre as bordas ║     ║
        print("╔" + "═" * largura + "╗")
        print(f"║ @{self.nome:<{largura - 2}} ║")
        print("╠" + "═" * largura + "╣")

        info = f"Seguidores: {self.seguidores}   Seguindo: {self.seguindo}   Posts: {len(self.posts)}"
        print(f"║ {info:<{largura - 1}}║")
        print("╠" + "═" * largura + "╣")

        descricao_formatada = f"\"{self.descricao}\""
        linhas_desc = textwrap.wrap(descricao_formatada, width=largura - 2)
        for linha in linhas_desc:
            print(f"║ {linha:<{largura - 2}} ║")

        print("╠" + "═" * largura + "╣")
        print(f"║ Último post:{' ' * (largura - 13)}║")

        if self.posts:
            ultimo_post = f"\"{self.posts[-1]}\""
            linhas_post = textwrap.wrap(ultimo_post, width=largura - 2)
            for linha in linhas_post:
                print(f"║ {linha:<{largura - 2}} ║")
        else:
            print(f"║ Nenhum post ainda.{' ' * (largura - 20)}║")

        print("╚" + "═" * largura + "╝")
        print("[N] Próximo  |  [V] Voltar  |  [S] Sair")