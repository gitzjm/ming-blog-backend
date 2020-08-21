# coding=UTF-8

"""``exceptions`` 错误异常

``error code`` 错误码参考:

========== ========================================
code       desc
========== ========================================
40010      对象无法修改
40101      未收到 token(JWT)
40102      无效的 token(JWT)
40103      无法正确解析从 JWT 的用户数据
40104      无法获取用户的 parentLevelUid 信息
40105      无法获取用户的 permissions 信息
40106      用户没有对应的权限
40107      用户并非对象的拥有者
40108      操作仅限admin权限
40109      用户没有通过人脸验证
40301      可能存在风险的查询
40302      对象已经存在
40303      对象不存在
42201      非法的 objectID
50301      mongodb 服务错误
50302      redis 服务错误
50303      enterprise 服务错误
40001      不存在的 objectID
========== ========================================
"""
import typing
from bson.errors import InvalidId
from pymongo.errors import PyMongoError
from redis.exceptions import RedisError
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import (
    HTTP_503_SERVICE_UNAVAILABLE,
    HTTP_422_UNPROCESSABLE_ENTITY
)

from core import conf


class FishExceptionMeta(type):
    """用户自定义异常元类"""

    def __init__(cls, clsname, bases, clsdict):
        super().__init__(clsname, bases, clsdict)
        setattr(
            cls,
            "debug",
            conf.server.mode == "debug"
        )


class FishException(HTTPException, metaclass=FishExceptionMeta):
    """用户自定义异常类"""
    debug = False

    def __init__(
            self,
            status_code: int,
            inner_code: str = "000000",
            detail: str = None
    ):
        self.inner_code = inner_code
        super().__init__(status_code=status_code, detail=detail)

    @property
    def json_response(self):
        """序列化异常返回"""
        return JSONResponse(
            status_code=self.status_code,
            content=self.get_content(self.inner_code, self.detail)
        )

    @classmethod
    def get_content(cls, inner_code: str, detail: Exception = None):
        """获取异常内容"""
        return cls.debug or {
            "code": inner_code,
            "detail": str(detail)
        }

    # ==============================


# HANDLER
# ==============================
async def fish_exception_handler(
        request: Request,
        exc: FishException
) -> JSONResponse:
    """项目自定义异常"""
    return exc.json_response


async def invalid_id_exception_handler(
        request: Request,
        exc: InvalidId
) -> JSONResponse:
    """非法的 objectID """
    return JSONResponse(
        content=FishException.get_content("42201", exc),
        status_code=HTTP_422_UNPROCESSABLE_ENTITY
    )


async def mongodb_exception_handler(
        request: Request,
        exc: PyMongoError
) -> JSONResponse:
    """mongodb 连接超时异常"""
    return JSONResponse(
        content=FishException.get_content("50301", exc),
        status_code=HTTP_503_SERVICE_UNAVAILABLE
    )


async def redis_exception_handler(
        request: Request,
        exc: RedisError
) -> JSONResponse:
    """redis 连接超时异常"""
    return JSONResponse(
        content=FishException.get_content("50302", exc),
        status_code=HTTP_503_SERVICE_UNAVAILABLE
    )
