#!/usr/bin/env python

import hashlib
import os
from model import Token

def generateToken():
    """
    生成一个可用的Token
    """
    return hashlib.sha1(os.urandom(128)).hexdigest()


def auth_login():
    """
    验证是否登录
    """
    from flask import request
    try:
        username = request.cookies.get('username')
        tokenid = request.cookies.get('tokenid')
        if not username or not tokenid:
            return False

        token = Token.query.filter_by(tokenid=tokenid).first()
        if token is None:
            return False
        return token.username == username
    except Exception as e:
        print(e)
        return False
    