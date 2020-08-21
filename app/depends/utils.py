"""
通用依赖工具模块
"""

import redis
from motor import motor_asyncio
from starlette.requests import Request

from core import REDIS_CONN, MONGODB_CONN


# ==============================
# CLIENT 数据库链接依赖
# ==============================
async def get_redis_client() -> redis.Redis:
    """获取redis链接"""
    return REDIS_CONN.client


async def get_mongo_client() -> motor_asyncio.AsyncIOMotorClient:
    """获取mongo链接"""
    return MONGODB_CONN.client


async def get_file_bucket() -> motor_asyncio.AsyncIOMotorGridFSBucket:
    """获取mongo文件bucket"""
    return MONGODB_CONN.bucket


# ==============================
# Request 相关方法
# ==============================

async def get_ip(request: Request) -> str:
    """获取用户真实IP"""
    if request.headers.getlist("X-Forwarded-For"):
        ip_addr = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip_addr = request.client.host
    return ip_addr
