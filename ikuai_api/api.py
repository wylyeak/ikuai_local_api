import requests

from ikuai_api.utils import *


class Router:
    def __init__(self, username, password, ip, port=80):
        """初始化登录认证"""
        self.username = username
        self.password = password
        self.ip = ip
        self.port = port
        # noinspection HttpUrlsUsage
        self.base_url = f"http://{self.ip}:{self.port}"

        self.session = requests.Session()

        self.__login()

    def __login(self):
        data = {
            "username": self.username,
            "passwd": encode_password(self.password),
            "pass": encode_pass(self.password),
            "remember_password": "",
        }

        # data = {"username": username, "passwd": self.password}
        resp = self.session.post(f"{self.base_url}/Action/login", json=data)

        login_result = resp.json()

        assert login_result['ErrMsg'] == 'Success'
        assert login_result['Result'] == 10000

    def call(self, action, func_name, param):
        payload = {
            'action': action,
            'func_name': func_name,
            'param': param
        }

        resp = self.session.post(f"{self.base_url}/Action/call", json=payload)

        r = resp.json()

        assert r['ErrMsg'] == 'Success'

        return r.get('Data')
