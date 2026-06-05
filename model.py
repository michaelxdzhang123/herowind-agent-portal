#!/usr/bin/env python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def generate_session():
    """
    生成并返回数据库会话对象。

    :return: SQLAlchemy 数据库会话对象
    :rtype: Session
    """
    return db.session

class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False)
    password = db.Column(db.String(120), unique=False)

    def __init__(self, username, password):
        """
        初始化用户对象。

        :param username: 用户名
        :type username: str
        :param password: 密码
        :type password: str
        """
        self.username = username
        self.password = password

    def __repr__(self):
        """
        返回用户对象的字符串表示。

        :return: 用户对象描述字符串
        :rtype: str
        """
        return '<User %r>' % self.username


class Token(db.Model):
    __tablename__ = 'Token'
    id = db.Column(db.Integer, primary_key=True)
    tokenid = db.Column(db.String(80), unique=False)
    username = db.Column(db.String(80), unique=False)
    status = db.Column(db.Boolean, default=True)
    
    def __init__(self, tokenid, username):
        """
        初始化令牌对象。

        :param tokenid: 令牌 ID
        :type tokenid: str
        :param username: 用户名
        :type username: str
        """
        self.username = username
        self.tokenid = tokenid

    def __repr__(self):
        """
        返回令牌对象的字符串表示。

        :return: 令牌对象描述字符串
        :rtype: str
        """
        return '<Token %r>' % self.username
