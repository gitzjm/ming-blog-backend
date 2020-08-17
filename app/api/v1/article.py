"""
文章相关接口
"""

from fastapi import (
    APIRouter,
    Depends,
    Body,
)
from motor.motor_asyncio import AsyncIOMotorClient

from depends import (
    pwd_handler,
    get_mongo_client
)
from schema.user import (
    LoginSchema,
    RegisterSchema
)

router = APIRouter()


@router.post(
    path='/login',
    name='登录',
    description='登录',
)
async def login(
        conn: AsyncIOMotorClient = Depends(get_mongo_client),
        # username: str = Body(..., description='用户名'),
        # password: str = Body(..., description='密码'),
        user: LoginSchema = Body(..., )
):
    document = await conn.users.find_one(
        {'username': user.username}
    )
    if user.password == document.password:
        return 'OK'
    else:
        return 'failed'
