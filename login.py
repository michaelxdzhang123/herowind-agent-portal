#!/usr/bin/env python
# coding: utf-8
"""
登录注销模块
"""

from flask import Blueprint, abort, jsonify, request, make_response, render_template
from model import User, Token, db
from utils import generateToken, auth_login
import os
import sys


login_bp = Blueprint('login_bp', __name__)

def typeof(variate):
    """
    获取变量的类型名称字符串。

    :param variate: 任意变量
    :return: 变量类型名称（如 'int', 'str', 'list' 等）
    :rtype: str
    """
    type = 'None'
    if isinstance(variate,int):
        type = "int"
    elif isinstance(variate,str):
         type = "str"
    elif isinstance(variate,float):
        type = "float"
    elif isinstance(variate,list):
         type = "list"
    elif isinstance(variate,tuple):
        type = "tuple"
    elif isinstance(variate,dict):
         type = "dict"
    elif isinstance(variate,set):
         type = "set"
    return type

@login_bp.route('/login', methods=['POST', 'GET'])
def login_route():
    """
    登录路由

    浏览器中输入: localhost:9999/login
    """
    if request.method == 'GET':
        if auth_login():
            return render_template('index.html')
        else:
            return render_template('login.html')

    else:
        if not request.is_json:
            username = request.form['username']
            password = request.form['password']
            try:
                user = User.query.filter_by(username=username).first()
            except Exception as e:
                print('DB query error:', e)
                return '<h1>没有这个ID或密码错误，请回到登录页面</h1>'

            if user is None or user.password != password:
                return '<h1>ID或密码错误，请回到登录页面</h1>'

            # 登录成功
            my_user = username
            dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
            # check my_user dir and create if no
            my_working_dir = os.path.join(dirname, 'templates/users', my_user)
            if not os.path.isdir(my_working_dir):
                os.system("./create_user.sh %s" % (my_user))
                print('-----------------run create_user.sh------------------------------')

            temp = render_template('index.html')
            resp = make_response(temp)

            # delete old token if exists, then create new one
            old_token = Token.query.filter_by(username=username).first()
            if old_token is not None:
                try:
                    db.session.delete(old_token)
                    db.session.commit()
                except:
                    print('deleted old cookie on server')

            # save new token
            tokenid = generateToken()
            token = Token(tokenid, username)
            db.session.add(token)
            db.session.commit()
            resp.set_cookie('username', username)
            resp.set_cookie('tokenid', tokenid)
            return resp

        else:
            try:
                info = request.get_json(silent=True)
                user = User.query.filter_by(username=info['username']).first()
                if user is None or user.password != info['password']:
                    return jsonify({'status': 'failed'}), 401
                tokenid = generateToken()
                token = Token(tokenid, user.username)
                db.session.add(token)
                db.session.commit()
                return jsonify({'status': 'success', 'token': tokenid})
            except Exception as e:
                print(e)
                return jsonify({'status': 'failed'}), 400


@login_bp.route('/logout', methods=['POST', 'GET'])
def logout_route():
    """
    登出路由
    """
    if request.method == 'GET':
        try:
            username = request.cookies.get('username')
            tokenid = request.cookies.get('tokenid')
            if not username or not tokenid:
                return '<h1>未登录</h1>'

            token = Token.query.filter_by(username=username).first()
            if token is None:
                return '<h1>未登录</h1>'

            if token.tokenid == tokenid:
                db.session.delete(token)
                db.session.commit()
                return '<h1>登出成功</h1>'
            else:
                return '<h1>凭据错误</h1>'
        except Exception as e:
            return '<h1>未登录</h1>'

    else:
        if not request.is_json:
            abort(400)
        else:
            info = request.get_json(silent=True)
            try:
                token = Token.query.filter_by(username=info['username']).first()
                if token is None:
                    return jsonify({'status': 'failed'}), 401
                if token.tokenid == info['tokenid']:
                    db.session.delete(token)
                    db.session.commit()
                    return jsonify({'status': 'success', 'username': info['username']})
                else:
                    return jsonify({'status': 'failed'})
            except Exception as e:
                print(e)
                return jsonify({"status": "failed"}), 400
