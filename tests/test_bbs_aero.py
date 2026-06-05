"""Tests for bbs_aero.py blueprint."""
import pytest


@pytest.fixture
def bbs_aero_app(app):
    """注册 bbs_aero 蓝图并返回应用实例。"""
    from bbs_aero import bbs_aero_bp
    app.register_blueprint(bbs_aero_bp)
    return app


@pytest.fixture
def bbs_aero_client(bbs_aero_app):
    """返回 bbs_aero 应用的测试客户端。"""
    return bbs_aero_app.test_client()


class TestBbsAeroRoute:
    def test_bbs_aero_get_redirects(self, bbs_aero_client):
        """测试 GET 请求 /bbs_aero 是否重定向到指定地址。"""
        resp = bbs_aero_client.get('/bbs_aero', follow_redirects=False)
        assert resp.status_code == 302
        assert '127.0.0.1:8551' in resp.headers.get('Location', '')

    def test_bbs_aero_post_redirects(self, bbs_aero_client):
        """测试 POST 请求 /bbs_aero 是否重定向到指定地址。"""
        resp = bbs_aero_client.post('/bbs_aero', follow_redirects=False)
        assert resp.status_code == 302
        assert '127.0.0.1:8551' in resp.headers.get('Location', '')
