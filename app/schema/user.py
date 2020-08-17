from fastapi import Body
from pydantic import BaseModel


class LoginSchema(BaseModel):
    username: str = Body(..., description='用户名')
    password: str = Body(..., description='密码')


class RegisterSchema(LoginSchema):
    re_password: str = Body(..., description='重复密码', alias='rePassword')
