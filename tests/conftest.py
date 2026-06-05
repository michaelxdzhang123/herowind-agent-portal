"""Pytest fixtures and configuration."""
import sys
import os
import types
from unittest.mock import MagicMock
import pytest

# Ensure project root is on path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock missing third-party modules that are imported but not needed for core tests
_MISSING_MODULES = {
    'flask_script': None,
    'flask_admin': None,
    'flask_admin.contrib.sqla': None,
    'pyecharts': None,
    'pyecharts.charts': None,
    'ModelMagnet_structure_cooling': None,
    'LubanToolBox': None,
    'LubanToolBox.ExcelAPI': None,
    'DeGenerator': None,
    'JIRA': None,
    'demjson': None,
    'django': None,
    'django.http': None,
    'django.shortcuts': None,
    'django.contrib': None,
    'django.contrib.auth': None,
    'django.contrib.auth.decorators': None,
    'farmInsightPro': None,
    'farmInsightPro.powernestaepAlgorithm': None,
    'farmInsightPro.forms': None,
}

for mod_name, mod_attrs in _MISSING_MODULES.items():
    if mod_name not in sys.modules:
        mock_mod = types.ModuleType(mod_name)
        if mod_attrs:
            for attr_name, attr_val in mod_attrs.items():
                setattr(mock_mod, attr_name, attr_val)
        sys.modules[mod_name] = mock_mod

# For flask_admin, provide minimal mock classes
if 'flask_admin' in sys.modules:
    fa = sys.modules['flask_admin']
    fa.Admin = MagicMock()
    fa.ModelView = MagicMock()

if 'flask_script' in sys.modules:
    fs = sys.modules['flask_script']
    fs.Manager = MagicMock()

if 'pyecharts.charts' in sys.modules:
    pc = sys.modules['pyecharts.charts']
    pc.Line = MagicMock()


@pytest.fixture
def app():
    """创建并配置一个用于测试的 Flask 应用实例，注册蓝图并初始化数据库。"""
    from flask import Flask
    from model import db

    app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.config['TESTING'] = True

    db.init_app(app)

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """返回应用 app 的测试客户端。"""
    return app.test_client()


@pytest.fixture
def db_session(app):
    """在应用上下文中提供数据库会话对象。"""
    from model import db
    with app.app_context():
        yield db.session
