"""Tests for utils.py."""
import pytest
from unittest.mock import patch, MagicMock
from utils import generateToken, auth_login


class TestGenerateToken:
    def test_generates_hex_string(self):
        """测试 generateToken 生成长度为 40 的十六进制字符串。"""
        token = generateToken()
        assert isinstance(token, str)
        assert len(token) == 40  # SHA-1 hex digest length
        # Should be valid hex
        int(token, 16)

    def test_generates_unique_tokens(self):
        """测试 generateToken 生成的多个 token 互不重复。"""
        tokens = {generateToken() for _ in range(100)}
        assert len(tokens) == 100


class TestAuthLogin:
    def test_auth_login_with_valid_token(self, app, db_session):
        """测试携带有效 token 的请求通过 auth_login 认证。"""
        from model import Token
        token = Token('validtoken', 'alice')
        db_session.add(token)
        db_session.commit()

        @app.route('/test_auth')
        def test_auth():
            """返回 auth_login 的认证结果（true/false）。"""
            return 'true' if auth_login() else 'false'

        with app.test_client() as client:
            client.set_cookie('username', 'alice')
            client.set_cookie('tokenid', 'validtoken')
            resp = client.get('/test_auth')
            assert resp.data == b'true'

    def test_auth_login_with_invalid_token(self, app, db_session):
        """测试携带无效 token 的请求未通过 auth_login 认证。"""
        from model import Token
        token = Token('validtoken', 'alice')
        db_session.add(token)
        db_session.commit()

        @app.route('/test_auth_invalid')
        def test_auth_invalid():
            """返回 auth_login 的认证结果（true/false）。"""
            return 'true' if auth_login() else 'false'

        with app.test_client() as client:
            client.set_cookie('username', 'alice')
            client.set_cookie('tokenid', 'wrongtoken')
            resp = client.get('/test_auth_invalid')
            assert resp.data == b'false'

    def test_auth_login_no_cookies(self, app):
        """测试未携带 cookie 的请求未通过 auth_login 认证。"""
        @app.route('/test_auth_none')
        def test_auth_none():
            """返回 auth_login 的认证结果（true/false）。"""
            return 'true' if auth_login() else 'false'

        with app.test_client() as client:
            resp = client.get('/test_auth_none')
            assert resp.data == b'false'
