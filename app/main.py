from db.init_db import dropar_tabelas, criar_tabelas
from services.popular_tabelas import popular_tabelas_fake
from services.atualizar_registros import executar_updates, atualizar_tabela
from services.apagar_registros import executar_deletes, deletar_por_id
from services.consultar_registros import (
    medias_curtidas_por_tag,
    contar_eventos_usuarios_ativos,
    contar_likes_feitos_pela_ia,
    consultar_todos_registros_tabela
)
from utils.helpers import mostra_todas_tabelas, estrutura_tabelas
from questionary import Choice
import questionary
import sys
import os
from sqlalchemy import Integer, TEXT, BOOLEAN, REAL, TIMESTAMP
from services.inserir_registros import *
from services.gerar_graficos_consultas import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def menu_interativo():
    print(r"""
    🧚‍♀️  ██     ██ ██ ███    ██ ██   ██ 
    🧚‍♀️  ██     ██ ██ ████   ██ ██  ██  
    🧚‍♀️  ██  █  ██ ██ ██ ██  ██ █████   
    🧚‍♀️  ██ ███ ██ ██ ██  ██ ██ ██  ██  
    🧚‍♀️   ███ ███  ██ ██   ████ ██   ██ 

    🌐 Bem-vindo à rede social Winx!
    📋 Escolha uma opção:
    """)
    return questionary.select(
        "⬇️  Navegue pelas opções:",
        choices=[
            questionary.Separator("📦  OPERAÇÕES PRINCIPAIS"),
            Choice("1️⃣  CRUD Winx", value="1"),
            questionary.Separator("🧪  TESTES"),
            Choice("2️⃣  Criar todas as tabelas", value="2"),
            Choice("3️⃣  Inserir dados de teste", value="3"),
            Choice("4️⃣  Atualizar dados", value="4"),
            Choice("5️⃣  Deletar dados", value="5"),
            questionary.Separator("📊  CONSULTAS"),
            Choice("6️⃣  Consulta 01", value="6"),
            Choice("7️⃣  Consulta 02", value="7"),
            Choice("8️⃣  Consulta 03", value="8"),
            Choice("9️⃣  Consultar tabelas individuais", value="9"),
            questionary.Separator("🛠️  MANUTENÇÃO"),
            Choice("🔟  Inserir registro", value="10"),
            Choice("1️⃣1️⃣  Atualizar registro", value="11"),
            Choice("1️⃣2️⃣  Deletar registro", value="12"),
            Choice("1️⃣3️⃣  Limpar dados da Winx", value="13"),
            questionary.Separator("🚪  SAIR"),
            Choice("0️⃣  Desconectar do banco e sair", value="0")
        ]
    ).ask()

def executar_opcao(escolha):
    match escolha:
        case "1":
            dropar_tabelas()
            criar_tabelas()
            popular_tabelas_fake(
                num_users_gerais=100,
                num_users_ia=50,
                num_tags=20,
                num_posts=1000,
                num_logs=1000,
                num_relacoes=300,
                num_reacoes=500
            )

            print("\n---CONSULTAS BEFORE---")
            print('Calcula a média de curtidas recebidas por post, agrupadas pela tag associada aos usuários.')
            print()
            resultado = medias_curtidas_por_tag()
            for linha in resultado:
                print(linha)
            print()

            print('Conta a quantidade de eventos (login, logout, criação de post etc.) realizados por usuários com ao menos 1 log registrado.')
            print()
            resultado1 = contar_eventos_usuarios_ativos()
            for linha in resultado1:
                print(linha)
            print()

            print('Conta o número total de likes que foram feitos por usuários cadastrados como IA.')
            print()
            resultado2 = contar_likes_feitos_pela_ia()
            for linha in resultado2:
                print(linha)
            print()

            executar_updates()
            executar_deletes()

            print("\n---CONSULTAS AFTER---")
            print('Calcula a média de curtidas recebidas por post, agrupadas pela tag associada aos usuários.')
            print()
            resultado = medias_curtidas_por_tag()
            for linha in resultado:
                print(linha)
            print()

            print(' Conta a quantidade de eventos realizados por usuários com ao menos 1 log registrado.')
            print()
            resultado1 = contar_eventos_usuarios_ativos()
            for linha in resultado1:
                print(linha)
            print()

            print('Conta o número total de likes que foram feitos por usuários cadastrados como IA.')
            print()
            resultado2 = contar_likes_feitos_pela_ia()
            for linha in resultado2:
                print(linha)
            print()

        case "2":
            criar_tabelas()
        case "3":
            popular_tabelas_fake(
                num_users_gerais=100,
                num_users_ia=50,
                num_tags=20,
                num_posts=1000,
                num_logs=1000,
                num_relacoes=300,
                num_reacoes=500
            )
        case "4":
            executar_updates()
        case "5":
            executar_deletes()
        case "6":
            print()
            print('Calcula a média de curtidas recebidas por post, agrupadas pela tag associada aos usuários.')
            print()
            resultado = medias_curtidas_por_tag()
            for linha in resultado:
                print(linha)
            gerar_grafico_media_curtidas()
        case "7":
            print()
            print(' Conta a quantidade de eventos realizados por usuários com ao menos 1 log registrado.')
            print()
            resultado = contar_eventos_usuarios_ativos()
            for linha in resultado:
                print(linha)
            gerar_grafico_eventos_ativos()
        case "8":
            print()
            print('Conta o número total de likes que foram feitos por usuários cadastrados como IA.')
            print()
            resultado = contar_likes_feitos_pela_ia()
            for linha in resultado:
                print(linha)
            gerar_grafico_likes_ia()
        case "9":
            todas_tabelas = mostra_todas_tabelas()
            tabela_escolhida = questionary.select(
                "📄 Escolha uma tabela para consultar:",
                choices=todas_tabelas
            ).ask()
            if tabela_escolhida:
                linhas = consultar_todos_registros_tabela(tabela_escolhida)

                for linha in linhas:
                    print(linha)

        case "10":

            todas_tabelas = mostra_todas_tabelas()
            tabela_escolhida = questionary.select(
                "📄 Escolha uma tabela para inserir:",
                choices=todas_tabelas
            ).ask()

            if tabela_escolhida == "generaluser":
                gerar_usuario()
            elif tabela_escolhida == "tag":
                gerar_tag()
            elif tabela_escolhida == "aiverified":
                gerar_ai_verified()
            elif tabela_escolhida == "ai":
                gerar_ai()
            elif tabela_escolhida == "post":
                gerar_post()
            elif tabela_escolhida == "logged":
                gerar_log()
            elif tabela_escolhida == "following":
                gerar_seguindo_seguidores()
            else:
                gerar_reacao()

        case "11":
            todas_tabelas = mostra_todas_tabelas()
            tabela_escolhida = questionary.select(
                "📄 Escolha uma tabela para consultar:",
                choices=todas_tabelas
            ).ask()

            if tabela_escolhida:
                colunas = estrutura_tabelas(tabela_escolhida)
                print(f"🧱 Estrutura da tabela '{tabela_escolhida}':")
                for col in colunas:
                    print(f"- {col['name']} {col['type']}", end='')
                    if not col['nullable']:
                        print(" NOT NULL")
                    else:
                        print()

                print(colunas[0])
                nome_pk =colunas[0]['name']

                coluna_escolhida = questionary.select(
                    "Escolha uma coluna para consultar:",
                    choices=[Choice(f"{col['name']} ({col['type']})", value=col['name']) for col in colunas]
                ).ask()

                coluna = next((c for c in colunas if c['name'] == coluna_escolhida), None)

                if isinstance(coluna['type'], Integer):
                    novo_valor = int(input("Digite o novo valor (int): "))
                elif isinstance(coluna['type'], REAL):
                    novo_valor = float(input("Digite o novo valor (float): "))
                elif isinstance(coluna['type'], BOOLEAN):
                    resp = input("Digite o novo valor (true/false): ").strip().lower()
                    novo_valor = resp in ['true', '1', 'sim', 's']
                elif isinstance(coluna['type'], TEXT):
                    novo_valor = input("Digite o novo valor (texto): ")
                elif isinstance(coluna['type'], TIMESTAMP):
                    from datetime import datetime
                    entrada = input("Digite o novo valor (formato: YYYY-MM-DD HH:MM:SS): ")
                    novo_valor = datetime.strptime(entrada, "%Y-%m-%d %H:%M:%S")
                else:
                    print("❌ Tipo ainda não suportado para atualização.")
                    return  # impede que atualizar_tabela seja chamado sem novo_valor

                valor_id = int(input("Digite o id do update: "))

                atualizar_tabela(tabela_escolhida, nome_pk, valor_id, coluna_escolhida, novo_valor)

        case "12":

            todas_tabelas = mostra_todas_tabelas()
            tabela_escolhida = questionary.select(
                "📄 Escolha uma tabela para deletar registro:",
                choices=todas_tabelas
            ).ask()

            colunas = estrutura_tabelas(tabela_escolhida)
            pk_coluna = colunas[0]['name']

            valor_id = int(input("Digite o id do delete: "))

            deletar_por_id(tabela_escolhida, pk_coluna, valor_id)

        case "13":
            dropar_tabelas()
        case "0":
            print("👋 Encerrando o programa...")
            exit()
        case _:
            print("⚠️ Opção inválida.")

while True:
    escolha = menu_interativo()
    executar_opcao(escolha)