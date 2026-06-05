"""Tests for guide.py blueprint."""
import sys
import types
import os
from unittest.mock import MagicMock, patch
import pytest


@pytest.fixture
def guide_app(app):
    """模拟外部依赖后注册 guide 蓝图并返回应用实例。"""
    # Mock heavy external dependencies
    for mod_name in ['ModelMagnet_structure_cooling', 'LubanToolBox', 'LubanToolBox.ExcelAPI']:
        if mod_name not in sys.modules:
            sys.modules[mod_name] = types.ModuleType(mod_name)

    sys.modules['ModelMagnet_structure_cooling'].GeneratorSys = MagicMock
    sys.modules['LubanToolBox.ExcelAPI'].Data2excel = MagicMock

    # Mock config.py loading from instance folder in guide.py
    with patch('flask.Flask.config', create=True) as mock_config:
        from guide import guide_bp
        app.register_blueprint(guide_bp)
        return app


@pytest.fixture
def guide_client(guide_app):
    """返回 guide 应用的测试客户端。"""
    return guide_app.test_client()


class TestGuideRoute:
    def test_guide_imports(self, guide_app):
        """确保 guide 蓝图已注册且导入未发生异常。"""
        # Just ensure the blueprint was registered without crashing on import
        assert 'guide_bp.guide_route' in guide_app.view_functions
