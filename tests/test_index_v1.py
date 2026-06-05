"""Tests for index_v1.py blueprint."""
import pytest
from model import Token, db


@pytest.fixture
def index_v1_app(app):
    """注册 index_v1 蓝图并返回应用实例。"""
    from index_v1 import index_v1_bp
    app.register_blueprint(index_v1_bp)
    return app


@pytest.fixture
def index_v1_client(index_v1_app):
    """返回 index_v1 应用的测试客户端。"""
    return index_v1_app.test_client()


class TestIndexV1Route:
    def test_index_v1_get_authenticated(self, index_v1_app, index_v1_client, db_session):
        """测试已认证用户 GET 请求 /index_v1 返回状态码 200。"""
        token = Token('v1tok', 'alice')
        db_session.add(token)
        db_session.commit()

        index_v1_client.set_cookie('username', 'alice')
        index_v1_client.set_cookie('tokenid', 'v1tok')
        resp = index_v1_client.get('/index_v1')
        assert resp.status_code == 200

    def test_index_v1_get_not_authenticated(self, index_v1_client):
        """测试未认证用户 GET 请求 /index_v1 返回重定向或 200。"""
        resp = index_v1_client.get('/index_v1')
        # Redirects to login when not authenticated
        assert resp.status_code in (200, 302)
