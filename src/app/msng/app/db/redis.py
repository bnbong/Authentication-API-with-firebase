import os
import aioredis
from aioredis import Redis,from_url
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL").strip()
REDIS_PORT = os.getenv("REDIS_PORT").strip()

def get_redis() -> Redis:
    return from_url(REDIS_URL, decode_responses=True,encoding="utf-8",port=REDIS_PORT)