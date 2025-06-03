from cards import Card

class Post:
    def __init__(self, usuario, texto, data_postagem, likes=0, respostas=None):
        self.usuario = usuario
        self.texto = texto
        self.likes = likes
        self.data_postagem = data_postagem
        self.respostas = respostas if respostas is not None else []
    
    def mostrar_post(self):
        largura = 44  # Total entre as bordas 
        cabecalho_titulo = (
            f"@{self.usuario:<25}{self.data_postagem.strftime('%d/%m/%Y %H:%M')}",
        )
        texto_post = f"{self.texto}"
        quantidade_likes = f"❤  {self.likes} likes"
        respostas_formatadas = []
        
        
        if self.respostas:
            respostas = "Respostas:"
            todas_resposta = respostas
            for resposta in self.respostas:
                autor = f"  └─ @{resposta['autor']:<16}"  
                data = f"{resposta['data'].strftime('%d/%m/%Y %H:%M'):>18}"
                texto = f"     {resposta['texto']}"  
                resposta_formatada = f"\n{autor}  {data}\n{texto}"
                todas_resposta+= resposta_formatada
            respostas_formatadas.append(todas_resposta)
        else:
            respostas_formatadas.append("└─ Sem respostas ainda.")
        
        print(
            Card(
                cabecalho_titulo,
                texto_post,
                quantidade_likes,
                *respostas_formatadas,
                inner_card_width=largura
            )
        )
        print("[N] Próximo  |  [V] Voltar  |  [S] Sair")