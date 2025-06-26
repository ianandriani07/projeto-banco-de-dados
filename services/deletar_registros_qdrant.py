from ai.cache import create_vec_database

def delete_qdrant_collections():
    try:
        db = create_vec_database()
        db.delete_collection_if_exists()
        print(f"✅ IA: Base de dados excluida com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao excluir base de dados: {e}")
