"""
user Schema
"""
import datetime

from fastapi import Body
from pydantic import BaseModel, Field, validator


class LoginSchema(BaseModel):
    """登录请求参数schema"""
    username: str = Body(..., min_length=8, description='用户名')
    password: str = Body(..., min_length=8, description='密码')


class RegisterSchema(LoginSchema):
    """注册请求参数schema"""
    re_password: str = Body(..., min_length=8, description='重复密码', alias='rePassword')


class UserSchema(BaseModel):
    """用户信息Schema"""
    username: str = Field(..., min_length=8, description='用户名')
    password: str = Field(..., min_length=8, description='密码')
    reg_time: str = Field(..., description='注册时间')
    reg_ip: str = Field(..., description='注册IP')
    reg_addr: str = Field(..., default='注册地址')

    @validator(
        "reg_time",
        pre=True
    )
    def date_to_str(self, value):
        """时间戳或时间对象转为时间字符串"""
        if value is None:
            res = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(value, (int, str)):
            res = datetime.datetime.fromtimestamp(int(value)).strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(value, datetime.datetime):
            res = value.strftime('%Y-%m-%d %H:%M:%S')
        else:
            res = value
        return res


if __name__ == '__main__':
    u = UserSchema(username='112345678', password="123123123232", reg_time='2020-02-02')
    print(u)
