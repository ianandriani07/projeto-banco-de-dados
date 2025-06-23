from sqlalchemy import text
from db.connection import engine
import os
# import subprocess

def criar_tabelas():
    try:
        caminho_sql = os.path.join(os.path.dirname(__file__), "scripts", "init.sql")
        print(f"📄 Executando script SQL: {caminho_sql}")

        with engine.connect() as conexao:
            with open(caminho_sql, "r", encoding="utf-8") as file:
                sql = file.read()

            for stmt in sql.strip().split(";"):
                if stmt.strip():
                    conexao.execute(text(stmt + ';'))
            conexao.commit()
            """
            subprocess.run([
                "sqlacodegen",
                string_connection,
                "--generator", "declarative",
                "--outfile", "models.py"
            ])
            """
            print("✅ Tabelas criadas com sucesso!")

    except Exception as e:
        print(f"Erro ao criar tabelas:\n{e}")

def dropar_tabelas():
    try:
        with engine.connect() as conexao:
            conexao.execute(text("""
               DO $$ BEGIN
                        EXECUTE 'DROP SCHEMA public CASCADE';
                        EXECUTE 'CREATE SCHEMA public';
                    END $$; 
            """))
            conexao.commit()
            print("🧨 Tabelas dropadas com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao criar tabelas:\n{e}")

