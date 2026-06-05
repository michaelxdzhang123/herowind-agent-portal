"""Tests for auth_token.py blueprint."""
import pytest
from model import Token, db


@pytest.fixture
def token_app(app):
    """注册 token 蓝图并返回应用实例。"""
    from auth_token import token_bp
    app.register_blueprint(token_bp)
    return app


@pytest.fixture
def token_client(token_app):
    """返回 token 应用的测试客户端。"""
    return token_app.test_client()


class TestValidateTokenRoute:
    def test_validate_token_get_logged_in(self, token_app, token_client, db_session):
        """测试已登录用户访问 /validate_token GET 请求返回已登录状态。"""
        token = Token('mytoken', 'alice')
        db_session.add(token)
        db_session.commit()

        token_client.set_cookie('username', 'alice')
        token_client.set_cookie('tokenid', 'mytoken')
        resp = token_client.get('/validate_token')
        assert resp.status_code == 200
        assert b'\xe5\xb7\xb2\xe7\x99\xbb\xe5\xbd\x95' in resp.data or b'logined' in resp.data.lower()

    def test_validate_token_get_not_logged_in(self, token_client):
        """测试未登录用户访问 /validate_token GET 请求返回未登录状态。"""
        resp = token_client.get('/validate_token')
        assert resp.status_code in (200, 400)

    def test_validate_token_post_valid(self, token_app, token_client, db_session):
        """测试通过 POST 提交有效 tokenid 时返回登录状态。"""
        token = Token('mytoken', 'alice')
        db_session.add(token)
        db_session.commit()

        resp = token_client.post('/validate_token', json={'tokenid': 'mytoken'})
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['status'] == 'logined'

    def test_validate_token_post_invalid(self, token_app, token_client, db_session):
        """测试通过 POST 提交无效 tokenid 时返回未登录状态。"""
        resp = token_client.post('/validate_token', json={'tokenid': 'notexist'})
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['status'] == 'unlogined'
