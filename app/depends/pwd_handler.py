"""
密码加密模块
"""
import typing
import hashlib
from binascii import b2a_hex, a2b_hex

import bcrypt
from Crypto.Cipher import AES


class AesCrypto:
    """AES工具"""

    def __init__(
            self,
            key: str,
            key_length: int = 16
    ):
        """
        :param key:密钥
        """
        self.key = key.zfill(key_length)
        self.mode = AES.MODE_CBC

    def encrypt(
            self,
            text: str
    ) -> str:
        """
        加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
        :param text:要加密的字符串 str
        :return: 加密后的字符串
        """
        text = text.encode("utf-8")
        cryptor = AES.new(self.key.encode("utf8"), self.mode, self.key.encode("utf8"))
        # 这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
        length = 16
        count = len(text)
        add = length - (count % length)
        text = text + (b'\0' * add)
        ciphertext = cryptor.encrypt(text)
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(ciphertext).decode("ASCII")

    def decrypt(
            self,
            text
    ) -> str:
        """
        解密后，去掉补足的空格用strip() 去掉
        :param text:要解密的字符串 bytes 或 str
        :return:
        """
        cryptor = AES.new(self.key.encode("utf8"), self.mode, self.key.encode("utf8"))
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip(b'\0').decode("utf8")


class NsPwdCrypto:
    """密码加密模块"""

    def __init__(
            self,
            aes_obj: AesCrypto
    ):
        """
        :param aes_obj: 自定义的AES加密对象
        """
        self.aes_obj = aes_obj

    @staticmethod
    def sha_pwd(
            pwd: str
    ) -> str:
        """
        hash加密
        :param pwd:要加密的字符串 str
        :return:sha_pwd加密后字符串 str
        """
        sha_512 = hashlib.sha512()
        sha_512.update(pwd.encode("utf8"))
        sha_pwd = sha_512.hexdigest()
        return sha_pwd

    @staticmethod
    def bcrypt_pwd(
            pwd: str,
            salt: typing.Optional[bytes] = None
    ) -> str:
        """
        bcrypt 随机盐加密
        :param pwd:要加密的字符串 str salt:验证盐 bytes
        :return:bcrypt加密后字符串 bytes类型
        """
        if salt is not None:
            bcrypt_pwd = bcrypt.hashpw(pwd.encode("utf8"), salt=salt)
        else:
            bcrypt_pwd = bcrypt.hashpw(pwd.encode("utf8"), bcrypt.gensalt())
        return bcrypt_pwd.decode("utf8")

    def aes_pwd(
            self,
            pwd: str
    ) -> str:
        """
        AES加密
        :param pwd:
        :return: AES加密过密码
        """
        aes_pwd = self.aes_obj.encrypt(pwd)
        return aes_pwd

    def crypto_pwd(
            self,
            pwd: str
    ) -> str:
        """
        密码加密
        :param pwd: 密码 str
        :return: 加密过的密码 str
        """
        sha_pwd = self.sha_pwd(pwd)
        bcrypt_pwd = self.bcrypt_pwd(sha_pwd)
        aes_pwd = self.aes_pwd(bcrypt_pwd)
        return aes_pwd

    def check_pwd(
            self,
            pwd: str,
            crypto_pwd: str
    ) -> bool:
        """
        验证密码是否正确
        :param pwd: 用户输入的密码
        :param crypto_pwd: 数据库加密过的密码
        :return: 密码是否正确
        """
        salt = self.aes_obj.decrypt(crypto_pwd).encode("utf8")
        sha_pwd = self.sha_pwd(pwd)
        bcrypt_pwd = self.bcrypt_pwd(sha_pwd, salt)
        return bcrypt_pwd == salt


aes_handler = AesCrypto(key="4190dbe7b5f7db0b")
pwd_handler = NsPwdCrypto(aes_handler)

if __name__ == '__main__':
    s = pwd_handler.crypto_pwd('123456')
    print(s)
