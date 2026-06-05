"""Tests for index.py blueprint."""
import pytest
from model import Token, db


@pytest.fixture
def index_app(app):
    """注册 index 蓝图并返回应用实例。"""
    from index import index_bp
    app.register_blueprint(index_bp)
    return app


@pytest.fixture
def index_client(index_app):
    """返回 index 应用的测试客户端。"""
    return index_app.test_client()


class TestIndexRoute:
    def test_index_get_authenticated(self, index_app, index_client, db_session):
        """测试已认证用户 GET 请求 /index 返回状态码 200。"""
        token = Token('idx123', 'alice')
        db_session.add(token)
        db_session.commit()

        index_client.set_cookie('username', 'alice')
        index_client.set_cookie('tokenid', 'idx123')
        resp = index_client.get('/index')
        assert resp.status_code == 200

    def test_index_get_not_authenticated(self, index_client):
        """测试未认证用户 GET 请求 /index 的响应。"""
        resp = index_client.get('/index')
        assert resp.status_code == 200
        # Returns error message when not logged in

    def test_index_post_authenticated(self, index_app, index_client, db_session):
        """测试已认证用户 POST 请求 /index 返回状态码 200。"""
        token = Token('idx456', 'bob')
        db_session.add(token)
        db_session.commit()

        index_client.set_cookie('username', 'bob')
        index_client.set_cookie('tokenid', 'idx456')
        resp = index_client.post('/index')
        assert resp.status_code == 200
