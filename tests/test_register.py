"""Tests for register.py blueprint."""
import pytest
from model import User, db


@pytest.fixture
def register_app(app):
    """注册 register 蓝图并返回应用实例。"""
    from register import register_bp
    app.register_blueprint(register_bp)
    return app


@pytest.fixture
def register_client(register_app):
    """返回 register 应用的测试客户端。"""
    return register_app.test_client()


class TestRegisterRoute:
    def test_register_get(self, register_client):
        """测试 GET 请求 /register 返回注册页面。"""
        resp = register_client.get('/register')
        assert resp.status_code == 200
        assert b'<html' in resp.data.lower() or b'<h1>' in resp.data

    def test_register_post_form_success(self, register_app, register_client, db_session):
        """测试使用表单数据 POST /register 成功注册新用户。"""
        resp = register_client.post('/register', data={'username': 'newuser', 'password': 'newpass'})
        assert resp.status_code == 200
        assert b'\xe6\xb3\xa8\xe5\x86\x8c\xe6\x88\x90\xe5\x8a\x9f' in resp.data or b'success' in resp.data.lower()
        assert db_session.query(User).filter_by(username='newuser').first() is not None

    def test_register_post_form_duplicate(self, register_app, register_client, db_session):
        """测试使用表单数据重复注册同名用户（无唯一约束时允许重复）。"""
        # The DB schema does not enforce unique usernames, so duplicate registration succeeds
        user = User('existing', 'pass')
        db_session.add(user)
        db_session.commit()

        resp = register_client.post('/register', data={'username': 'existing', 'password': 'pass'})
        assert resp.status_code == 200
        # Since no unique constraint exists, this will succeed
        assert db_session.query(User).filter_by(username='existing').count() == 2

    def test_register_post_json_success(self, register_app, register_client, db_session):
        """测试使用 JSON 数据 POST /register 成功注册新用户。"""
        resp = register_client.post('/register', json={'username': 'jsonuser', 'password': 'jsonpass'})
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['status'] == 'success'
        assert db_session.query(User).filter_by(username='jsonuser').first() is not None

    def test_register_post_json_duplicate(self, register_app, register_client, db_session):
        """测试使用 JSON 数据重复注册同名用户（无唯一约束时允许重复）。"""
        # No unique constraint on username, so duplicate succeeds
        user = User('jsondup', 'pass')
        db_session.add(user)
        db_session.commit()

        resp = register_client.post('/register', json={'username': 'jsondup', 'password': 'pass'})
        assert resp.status_code == 200
        data = resp.get_json()
        # With no unique constraint, duplicate is allowed
        assert data['status'] == 'success'
        assert db_session.query(User).filter_by(username='jsondup').count() == 2
