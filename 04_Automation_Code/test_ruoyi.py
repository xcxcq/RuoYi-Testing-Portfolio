import pytest
import requests

BASE_URL = "http://localhost:8080"


def test_login_success():
    """测试正确账号密码登录"""
    url = f"{BASE_URL}/login"
    payload = {"username": "admin", "password": "admin123"}
    response = requests.post(url, json=payload)
    data = response.json()

    assert response.status_code == 200
    assert data["code"] == 200
    assert "token" in data


def test_login_fail():
    """测试错误密码登录"""
    url = f"{BASE_URL}/login"
    payload = {"username": "admin", "password": "wrong_password"}
    response = requests.post(url, json=payload)
    data = response.json()

    # 若依密码错误通常返回 code 500 或自定义的业务错误码
    assert data["code"] != 200


def test_get_user_list(auth_headers):
    """测试携带合法 Token 获取用户列表（正向测试）"""
    url = f"{BASE_URL}/system/user/list"
    # 只要在参数里写上 auth_headers，pytest 就会自动调用 conftest.py 里的登录逻辑
    response = requests.get(url, headers=auth_headers)
    data = response.json()

    assert response.status_code == 200
    assert data["code"] == 200
    assert "rows" in data


def test_access_without_token():
    """测试未携带 Token 访问受限接口（安全测试）"""
    url = f"{BASE_URL}/system/user/list"
    # 故意不带 Headers
    response = requests.get(url)
    data = response.json()

    # 未登录访问，预期应该被拦截（401 或 403）
    assert data["code"] == 401