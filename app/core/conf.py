"""
config
"""

import configparser
import os

# 工程路径
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


# ==============================
# 配置
# ==============================
class ConfigMeta(type):
    """配置元类"""
    # pylint: disable=no-value-for-parameter

    _instance = None
    path = None

    def __load(cls):
        """加载配置文件"""
        if cls.path is not None:
            config = configparser.RawConfigParser()
            config.read(cls.path)
            for section in config.sections():
                setattr(cls._instance, section, lambda x: x)
                for key, value in config.items(section):
                    setattr(getattr(cls._instance, section), key, value)

    def __call__(cls, *args, **kwargs):
        """返回配置"""
        if cls._instance is None:
            cls._instance = super().__call__()
            cls.__load()
        return cls._instance


class Config(metaclass=ConfigMeta):
    """配置类"""
    # pylint: disable=too-few-public-methods

    path = os.path.join(PROJECT_PATH, "config.ini")


conf = Config()
