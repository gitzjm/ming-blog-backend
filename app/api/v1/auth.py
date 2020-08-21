"""
登录相关接口
"""
import time

from starlette.requests import Request
from fastapi import (
    APIRouter,
    Depends,
    Body,
)
from motor.motor_asyncio import AsyncIOMotorClient

from depends import (
    pwd_handler,
    get_mongo_client, get_ip
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
        user_form: LoginSchema = Body(..., )
):
    """登录"""
    user = await conn.users.find_one(
        {'username': user_form.username}
    )
    if pwd_handler.check_pwd(user_form.password, user.password):
        return 'OK'
    else:
        return 'failed'


@router.post(
    path='/register',
    name='注册',
    description='注册',
)
async def register(
        request: Request,
        conn: AsyncIOMotorClient = Depends(get_mongo_client),
        user_form: RegisterSchema = Body(..., )
):
    """注册"""
    user = await conn.users.find_one(
        {'username': user_form.username}
    )
    if user:
        return '用户已注册'
    if user_form.password == user_form.re_password:
        pwd = pwd_handler.crypto_pwd(user_form.password)
        conn.users.inster_one({
            'username': user_form.username,
            'password': pwd,
            'reg_time': time.time(),
            'reg_ip': await get_ip(request)
        })
        return '注册成功'
    else:
        return '两次输入密码不一致'
