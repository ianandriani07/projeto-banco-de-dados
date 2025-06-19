from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv(override=True)

url = "postgresql://user:password@localhost:5432/database_name"

string_connection = f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@localhost:{os.getenv("DB_PORT")}/{os.getenv("DB_DATABASE")}'

print(string_connection)

try:
    engine = create_engine(string_connection, echo=True)
    print("Conectado")
    Session = sessionmaker(bind=engine)
    Base = declarative_base()
    
    def get_session():
        return Session()
    
except Exception as e:
    print(f"Erro ao conectar ao banco de dados: {e}")
