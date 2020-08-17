import redis
from motor import motor_asyncio

from core import REDIS_CONN, MONGODB_CONN


# ==============================
# CLIENT
# ==============================
async def get_redis_client() -> redis.Redis:
    return REDIS_CONN.client


async def get_mongo_client() -> motor_asyncio.AsyncIOMotorClient:
    return MONGODB_CONN.client


async def get_file_bucket() -> motor_asyncio.AsyncIOMotorGridFSBucket:
    return MONGODB_CONN.bucket
