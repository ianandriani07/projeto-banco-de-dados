import matplotlib.pyplot as plt
from services.consultar_registros import *

def gerar_grafico_media_curtidas():
    resultados = medias_curtidas_por_tag()
    tags = [r[0] for r in resultados]
    medias = [r[1] for r in resultados]

    plt.figure(figsize=(10, 6))
    plt.barh(tags, medias)
    plt.xlabel("Média de Curtidas")
    plt.ylabel("Tags")
    plt.title("Média de curtidas por tag")
    plt.tight_layout()
    plt.show()


def gerar_grafico_eventos_ativos():
    resultados = contar_eventos_usuarios_ativos()
    eventos = [r[0] for r in resultados]
    contagens = [r[1] for r in resultados]

    plt.figure(figsize=(10, 6))
    plt.bar(eventos, contagens)
    plt.xlabel("Evento")
    plt.ylabel("Quantidade")
    plt.title("Eventos registrados por usuários ativos")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

def gerar_grafico_likes_ia():
    resultados = contar_likes_feitos_pela_ia()
    modelos = [r[0] for r in resultados]
    curtidas = [r[1] for r in resultados]

    plt.figure(figsize=(10, 6))
    plt.bar(modelos, curtidas)
    plt.xlabel("Modelos de IA")
    plt.ylabel("Likes realizados")
    plt.title("Curtidas feitas por modelos de IA")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()