import ollama
from qdrant_client import QdrantClient
from typing import List, Optional, NamedTuple
from qdrant_client.models import PointStruct, VectorParams, Distance, PayloadSchemaType
from qdrant_client.http.models import Filter, FieldCondition, MatchValue, FilterSelector

class UserID:

    def __init__(self, id_user: int, username: str, description: str, posts: List[str]):
        self.id_user: int = id_user
        self.username: int = username
        self.description: str = description
        self.posts: List[str] = posts

    def __repr__(self):
        post_string = ""
        for i, post in enumerate(self.posts):
            post_string += f"\n### Post {i + 1}:\n" + post

        return f"""# Bio
## Description
{self.description}
## Posts
{post}
"""
    
    def as_dict(self):
        return {'id_user': self.id_user, 'username': self.username, 'description': self.username, 'posts': self.posts}

class Bot:

    def __init__(self, host: str, default_model: str = "nomic-embed-text"):
        self.client = ollama.Client(host)
        self.default_model = default_model

    def embed(self, query: str) -> List[float]:
        return self.client.embed(model=self.default_model, input=query).embeddings[0]


class VecDB:

    def __init__(self, collection_name: str, bot: Bot):
        self.client = QdrantClient(path="vec")
        self.collection = collection_name
        self.embedding_bot = bot

    def create_collection_if_dont_exist(self, embedding_length: int):
        # Cria a coleção se ainda não existir
        if not self.client.collection_exists(self.collection):
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(
                    size=embedding_length,
                    distance=Distance.COSINE,
                ),
            )

            # self.client.create_payload_index(
            #     collection_name=self.collection,
            #     field_name="extra.user_id",
            #     field_schema=PayloadSchemaType.INTEGER
            # )

    def delete_collection_if_exists(self):
        if self.client.collection_exists(self.collection):
            self.client.delete_collection(collection_name=self.collection)

    def search_similar_texts_by_embedding(
        self, query_embedding: List[float], top_k: int = 5, score_threshold: Optional[float] = None
    ):
        search_results = self.client.search(
            collection_name=self.collection,
            query_vector=query_embedding,
            limit=top_k + 1,
            with_payload=True,
            score_threshold=score_threshold,
        )

        return (search_results[0], search_results[1:])
    
    def search_similar_texts_by_user_id(self, user_id: int, top_k: int = 5, score_threshold: Optional[float] = None):
        embedding = self.get_vector_by_user_id(user_id)

        if embedding is None:
            return None
        
        return self.search_similar_texts_by_embedding(embedding, top_k=top_k, score_threshold=score_threshold)

    def get_vector_by_user_id(self, user_id: int) -> List[float] | None:
        points = self.client.scroll(
            collection_name=self.collection,
            scroll_filter=Filter(
            must=[
                    FieldCondition(
                        key="id_user",
                        match=MatchValue(value=user_id)
                    )
                ]
            ),
            with_vectors=True,
            limit=1
        )

        if len(points[0]) == 0 or points[0][0] is None:
            return None

        return points[0][0].vector

    def delete_register_by_user_id(self, user_id: int):
        self.client.delete(
            collection_name=self.collection,
            points_selector=FilterSelector(
                filter=Filter(
                    must=[
                        FieldCondition(
                            key="id_user",
                            match=MatchValue(value=user_id)
                        )
                    ]
                )
            )
        )

    def save_embedding(self, payload: UserID) -> int:
        # Gera o embedding usando o Ollama com o modelo nomic-embed-text
        embedding = self.embedding_bot.embed(str(payload))

        # Cria a coleção se ainda não existir
        self.create_collection_if_dont_exist(len(embedding))

        self.delete_register_by_user_id(payload.id_user)

        # Gera um ID único para o ponto (por exemplo: usando count total de pontos na collection + 1)
        existing_points = self.client.count(collection_name=self.collection).count
        point_id = existing_points + 1

        # Faz o upsert (salva o vetor com o texto como payload)
        self.client.upsert(
            collection_name=self.collection,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload=payload.as_dict(),
                )
            ],
        )

        return point_id
