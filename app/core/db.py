# coding=UTF-8

"""``db`` ...
"""


class Conn:
    """链接基类"""
    # pylint: disable=too-few-public-methods

    client = None
    bucket = None


# ==============================
# CONN INIT
# ==============================
MONGODB_CONN = Conn()

REDIS_CONN = Conn()



