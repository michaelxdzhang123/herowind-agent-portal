"""Tests for model.py SQLAlchemy models."""
import pytest
from model import User, Token, db


class TestUserModel:
    def test_user_creation(self, db_session):
        """测试创建 User 记录并验证字段值。"""
        user = User('testuser', 'testpass')
        db_session.add(user)
        db_session.commit()
        assert user.id is not None
        assert user.username == 'testuser'
        assert user.password == 'testpass'

    def test_user_repr(self, db_session):
        """测试 User 对象的 repr 字符串表示。"""
        user = User('alice', 'secret')
        db_session.add(user)
        db_session.commit()
        assert repr(user) == "<User 'alice'>"

    def test_multiple_users(self, db_session):
        """测试批量创建多个 User 记录。"""
        users = [User(f'user{i}', f'pass{i}') for i in range(5)]
        db_session.add_all(users)
        db_session.commit()
        assert db_session.query(User).count() == 5


class TestTokenModel:
    def test_token_creation(self, db_session):
        """测试创建 Token 记录并验证字段值。"""
        token = Token('abc123', 'testuser')
        db_session.add(token)
        db_session.commit()
        assert token.id is not None
        assert token.tokenid == 'abc123'
        assert token.username == 'testuser'
        assert token.status is True

    def test_token_repr(self, db_session):
        """测试 Token 对象的 repr 字符串表示。"""
        token = Token('tok1', 'bob')
        db_session.add(token)
        db_session.commit()
        assert repr(token) == "<Token 'bob'>"

    def test_token_query_by_username(self, db_session):
        """测试按用户名查询 Token 记录。"""
        t1 = Token('t1', 'alice')
        t2 = Token('t2', 'bob')
        db_session.add_all([t1, t2])
        db_session.commit()
        result = db_session.query(Token).filter_by(username='alice').first()
        assert result.tokenid == 't1'


class TestGenerateSession:
    def test_generate_session_returns_session(self, db_session):
        """测试 generate_session 函数返回数据库会话对象。"""
        from model import generate_session
        sess = generate_session()
        assert sess is db_session
