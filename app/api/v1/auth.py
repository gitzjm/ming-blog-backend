"""
登录相关接口
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


@router.post(
    path='/register',
    name='注册',
    description='注册',
)
async def login(
        conn: AsyncIOMotorClient = Depends(get_mongo_client),
        user: RegisterSchema = Body(..., )
):
    document = await conn.users.find_one(
        {'username': user.username}
    )
    if document:
        return '用户已注册'
    if user.password == user.re_password:
        pwd = pwd_handler.crypto_pwd(user.password)
        conn.users.inster_one({
            'username': user.username,
            'password': pwd
        })
        return '注册成功'
    else:
        return '两次输入密码不一致'
