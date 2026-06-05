"""Tests for setup_zone.py blueprint."""
import pytest


@pytest.fixture
def setup_zone_app(app):
    """注册 setup_zone 蓝图并返回应用实例。"""
    from setup_zone import setup_zone_bp
    app.register_blueprint(setup_zone_bp)
    return app


@pytest.fixture
def setup_zone_client(setup_zone_app):
    """返回 setup_zone 应用的测试客户端。"""
    return setup_zone_app.test_client()


class TestSetupZoneRoute:
    def test_setup_zone_get(self, setup_zone_client):
        """测试 GET 请求 /setup_zone 返回状态码 200。"""
        resp = setup_zone_client.get('/setup_zone')
        assert resp.status_code == 200

    def test_setup_zone_post(self, setup_zone_client):
        """测试 POST 请求 /setup_zone 返回状态码 200。"""
        resp = setup_zone_client.post('/setup_zone')
        assert resp.status_code == 200
