import base64
import hashlib
import os


def encode_password(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    hash_value = md5.hexdigest()
    return hash_value


def encode_pass(password):
    d = ("salt_11" + password).encode("ASCII")
    return base64.b64encode(d).decode()


def encode_ssl(text: str):
    return text.replace(" ", "#").replace("\n", "@")


def ssl_read(value: str) -> str:
    """
    如果 value 是文件路径，返回文件内容；
    否则认为是直接 PEM 内容。
    """
    if value.strip().startswith("-----BEGIN"):
        return value
    if os.path.exists(value) and os.path.isfile(value):
        try:
            with open(value, "r") as f:
                return f.read()
        except Exception as e:
            raise ValueError(f"无法读取文件 {value}: {e}")
        
    raise ValueError(f"无效输入：既不是 PEM 内容也不是有效路径: {value}")
