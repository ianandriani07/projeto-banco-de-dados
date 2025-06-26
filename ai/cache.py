import os
from .bot import Bot, VecDB
from functools import lru_cache

@lru_cache(maxsize=1)
def create_vec_database() -> VecDB:
    bot = Bot(os.getenv("OLLAMA_HOST"))
    return VecDB("user-data", bot)
