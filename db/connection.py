from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv(override=True)

string_connection = f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@localhost:{os.getenv("DB_PORT")}/{os.getenv("DB_DATABASE")}'

try:
    engine = create_engine(string_connection, echo=False)
    print(f"✅ Conectado ao banco '{os.getenv('DB_DATABASE')}'")
    Session = sessionmaker(bind=engine)
    Base = declarative_base()

    def get_session():
        return Session()

except Exception as e:
    print(f"❌ Erro ao conectar ao banco de dados:\n{e}")