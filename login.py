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
@login_bp.route('/login', methods=['POST', 'GET']) # 需要填写method
def login_route():
    """
    在此处填写login的相关代码

    浏览器中输入: localhost:5000/login
    """
    if request.method == 'GET':
        if auth_login():
            #已经登陆了,mkdirs

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
                    print('----------------------------not in sqlmysql',e)
                    return '<h1>没有这个ID或密码错误，请回到登录页面</h1>'
                print('-----------------user = ',user)
                if user.password == password:
                    #resp = make_response('<h1>登录成功</h1>')
                    my_user = username
                    # print('username==', my_user)
                    dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
                    # check my_user dir and create if no
                    my_working_dir = os.path.join(dirname, 'templates/users', my_user)
                    if not os.path.isdir(my_working_dir):
                        os.system("./create_user.sh %s" % (my_user))
                        print('-----------------run create_user.sh------------------------------')
                    temp = render_template('index.html')
                    resp = make_response(temp)
                    print('line----------------------------43')
                    # delete server token , if empty create one, otherwise delete than create one
                    token = Token.query.filter_by(username=username).first()
                    token_type = typeof(token)
                    print('----------------------exception happed',type(token),token_type)
                    try:
                        db.session.delete(token)
                        db.session.commit()
                    except:
                        print('deleted old cookie on server')
                    # save token
                    tokenid = generateToken()
                    token = Token(tokenid, username)
                    db.session.add(token)
                    db.session.commit()
                    resp.set_cookie('username', username)
                    resp.set_cookie('tokenid', tokenid)
                    #返回 client object below
                    return resp
                    #return render_template('index.html')
                else:
                    return '<h1>凭证错误</h1>'
                return '<h1>ID或密码错误，请回到登录页面</h1>'

        else:
            try:
                info = request.get_json(silent=True)
                user = User.query.filter_by(username=info['username']).first()
                if user.password == info['password']:
                    tokenid = generateToken()
                    token = Token(tokenid, user.username)
                    db.session.add(token)
                    db.session.commit()
                    return jsonify({'status': 'success', 'token': tokenid})
                else:
                    return jsonify({'status': 'failed'}), 401
            except Exception as e:
                print(e)
                return jsonify({'status': 'failed'}), 400
        

@login_bp.route('/logout', methods=['POST', 'GET'])
def logout_route():

    """
    在此处填写logout相关代码
    pass 可以删除
    """
    if request.method == 'GET':
        try:
            username = request.cookies.get('username')
            tokenid = request.cookies.get('tokenid')
            
            token = Token.query.filter_by(username=username).first()
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
                if token.tokenid == info['tokenid']:
                    db.session.delete(token)
                    db.session.commit()
                    return jsonify({'status': 'success', 'username': info['username']})
                else:
                    return jsonify({'status': 'failed'})
            except Exception as e:
                print(e)
                return jsonify({"status": "failed"}), 400
