import pytest
import requests

# 配置若依后端的地址
BASE_URL = "http://localhost:8080"


@pytest.fixture(scope="session")
def get_token():
    """全局登录夹具：只执行一次登录，获取 token 供所有用例使用"""
    login_url = f"{BASE_URL}/login"
    payload = {
        "username": "admin",
        "password": "admin123"
    }

    # 发送登录请求
    response = requests.post(login_url, json=payload)
    res_data = response.json()

    # 断言登录是否成功
    assert res_data["code"] == 200, f"登录失败，返回信息: {res_data}"

    # 提取 token（若依返回的 token 通常在这个字段里）
    token = res_data["token"]
    return token


@pytest.fixture(scope="session")
def auth_headers(get_token):
    """全局请求头夹具：把 token 拼装成标准的 Headers"""
    return {
        "Authorization": f"Bearer {get_token}",
        "Content-Type": "application/json"
    }