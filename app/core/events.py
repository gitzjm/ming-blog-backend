import redis
from motor import motor_asyncio

from core import (
    MONGODB_CONN,
    REDIS_CONN
)
from core.conf import conf


# ==============================
# Mongo
# ==============================
# @app.on_event('startup')
async def connect_to_mongo():
    """链接Mongo"""
    MONGODB_CONN.client = motor_asyncio.AsyncIOMotorClient(
        host=conf.database.host,
        port=int(conf.database.port),
        username=conf.database.username,
        password=conf.database.password,
        authSource=conf.database.name,
        ServerSelectionTimeoutMS=3000,
    )[conf.database.name]
    MONGODB_CONN.bucket = motor_asyncio.AsyncIOMotorGridFSBucket(MONGODB_CONN.client)


# @app.on_event('shutdown')
async def close_mongo_connection():
    """关闭Mongo"""
    MONGODB_CONN.client.close()


# ==============================
# Redis
# ==============================
# @app.on_event('startup')
async def connect_to_redis():
    """连接Redis"""
    REDIS_CONN.client = redis.Redis(
        host=conf.redis.host,
        port=int(conf.database.port),
        db=int(conf.redis.db),
        socket_connect_timeout=1,
    )


# @app.on_event('shutdown')
async def close_redis_connection():
    """关闭Redis"""
    REDIS_CONN.client.close()
