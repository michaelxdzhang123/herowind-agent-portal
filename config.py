# Stub config for testing
import os

class Config:
    """
    应用配置类，包含数据库连接、密钥及工作目录等配置项。
    """
    SECRET_KEY = 'test-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data/data.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WORKING_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates/users')
    WORKING_MODEL_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'models')
