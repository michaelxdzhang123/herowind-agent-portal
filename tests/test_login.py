"""Tests for login.py blueprint."""
import pytest
from model import User, Token, db


@pytest.fixture
def login_app(app):
    """注册 login 蓝图并返回应用实例。"""
    from login import login_bp
    app.register_blueprint(login_bp)
    return app


@pytest.fixture
def login_client(login_app):
    """返回 login 应用的测试客户端。"""
    return login_app.test_client()


class TestLoginRoute:
    def test_login_get_not_authenticated(self, login_client):
        """测试未认证用户 GET 请求 /login 返回登录页面。"""
        resp = login_client.get('/login')
        assert resp.status_code == 200
        # Should render login template
        assert b'<html' in resp.data.lower() or b'<h1>' in resp.data

    def test_login_post_valid_form(self, login_app, login_client, db_session):
        """测试使用正确的表单数据 POST /login 可以成功登录并设置 cookie。"""
        user = User('alice', 'secret')
        db_session.add(user)
        db_session.commit()

        resp = login_client.post('/login', data={'username': 'alice', 'password': 'secret'})
        assert resp.status_code == 200
        # Check cookie was set via headers
        assert 'username=alice' in str(resp.headers.getlist('Set-Cookie'))

    def test_login_post_invalid_password(self, login_app, login_client, db_session):
        """测试使用错误的密码 POST /login 返回凭证错误提示。"""
        user = User('alice', 'secret')
        db_session.add(user)
        db_session.commit()

        resp = login_client.post('/login', data={'username': 'alice', 'password': 'wrong'})
        assert resp.status_code == 200
        assert b'\xe5\x87\xad\xe8\xaf\x81\xe9\x94\x99\xe8\xaf\xaf' in resp.data or b'error' in resp.data.lower()

    def test_login_post_json_valid(self, login_app, login_client, db_session):
        """测试使用正确的 JSON 数据 POST /login 返回成功状态和 token。"""
        user = User('bob', 'pass')
        db_session.add(user)
        db_session.commit()

        resp = login_client.post('/login', json={'username': 'bob', 'password': 'pass'})
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['status'] == 'success'
        assert 'token' in data

    def test_login_post_json_invalid(self, login_app, login_client, db_session):
        """测试使用错误的 JSON 凭证 POST /login 返回 401。"""
        user = User('bob', 'pass')
        db_session.add(user)
        db_session.commit()

        resp = login_client.post('/login', json={'username': 'bob', 'password': 'wrong'})
        # We fixed the missing return to return 401 for wrong password
        assert resp.status_code == 401


class TestLogoutRoute:
    def test_logout_get_valid(self, login_app, login_client, db_session):
        """测试已登录用户 GET 请求 /logout 成功登出。"""
        user = User('alice', 'secret')
        token = Token('tok123', 'alice')
        db_session.add_all([user, token])
        db_session.commit()

        login_client.set_cookie('username', 'alice')
        login_client.set_cookie('tokenid', 'tok123')
        resp = login_client.get('/logout')
        assert resp.status_code == 200
        assert b'\xe7\x99\xbb\xe5\x87\xba\xe6\x88\x90\xe5\x8a\x9f' in resp.data or b'success' in resp.data.lower()

    def test_logout_post_json_valid(self, login_app, login_client, db_session):
        """测试通过 JSON POST 请求 /logout 成功登出。"""
        user = User('alice', 'secret')
        token = Token('tok123', 'alice')
        db_session.add_all([user, token])
        db_session.commit()

        resp = login_client.post('/logout', json={'username': 'alice', 'tokenid': 'tok123'})
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['status'] == 'success'
