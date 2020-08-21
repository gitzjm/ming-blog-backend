"""
app,用于初始化FastAPI应用
"""
from fastapi import FastAPI
from pymongo.errors import PyMongoError, InvalidId
from redis import RedisError
from starlette.middleware.cors import CORSMiddleware

from api import api_router
from core import (
    connect_to_mongo,
    connect_to_redis,
    close_mongo_connection,
    close_redis_connection,
    invalid_id_exception_handler,
    mongodb_exception_handler,
    fish_exception_handler,
    redis_exception_handler,
    FishException
)

app = FastAPI(docs_url="/docs", openapi_url="/openapi.json")

# ==============================
# MIDDLEWARE
# ==============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
# ROUTER
# ==============================
app.include_router(api_router)

# ==============================
# EVENT HANDLER
# ==============================
app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("startup", connect_to_redis)
app.add_event_handler("shutdown", close_mongo_connection)
app.add_event_handler("shutdown", close_redis_connection)

# ==============================
# EXCEPTION HANDLER
# ==============================
app.add_exception_handler(PyMongoError, mongodb_exception_handler)
app.add_exception_handler(InvalidId, invalid_id_exception_handler)
app.add_exception_handler(FishException, fish_exception_handler)
app.add_exception_handler(RedisError, redis_exception_handler)
