import pytest
from fastapi.testclient import TestClient
from app import schema
# from .database import client, session
from jose import JWTError, jwt
from app.config import settings

def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schema.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code",[
    ("alanwang@gmail.com", "password123", 200),  # 正确登录
    ("alanwang@gmail.com", "wrongpass", 403),    # 错误密码
    ("notfound@gmail.com", "password123", 403),  # 用户不存在
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", 
                      data={"username": email, 
                            "password": password}
                      )
    assert res.status_code == status_code