from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api import api_router

from core import (
    connect_to_mongo,
    connect_to_redis,
    close_mongo_connection,
    close_redis_connection
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
