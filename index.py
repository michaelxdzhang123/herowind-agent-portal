from flask import Blueprint, render_template, request,redirect
from model import User, Token, db
import os
import sys

index_bp = Blueprint('index_bp', __name__)
@index_bp.route('/index', methods=['GET', 'POST'])
def index_route():
    """
    首页路由，处理 GET 和 POST 请求。
    验证用户登录状态，若已登录则渲染首页模板，否则返回错误提示。

    :return: 首页模板或错误提示页面
    """

    if request.method == 'GET':
        try:
            username = request.cookies.get('username')
            tokenid = request.cookies.get('tokenid')

            token = Token.query.filter_by(username=username).first()
            if token.tokenid == tokenid:
                #已经登录了
                # 已经登陆了,mkdirs
                #username = request.cookies.get('username')
                my_user = username
                # print('username==', my_user)
                dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
                # check my_user dir and create if no
                my_working_dir = os.path.join(dirname, 'templates/users', my_user)
                print('--------------------------',my_user)
                if not os.path.isdir(my_working_dir):
                    os.system("./create_user.sh %s" % (my_user))
                print('get : 已经登录了')
                return render_template('index.html')
            else:
                return '<h1>凭据错误 请联系管理员web administrator please</h'
        except Exception as e:
            #return '<h1>未登录</h1>'
            return 'add /loign'

    else:
        if not request.is_json:
            try:
                username = request.cookies.get('username')
                tokenid = request.cookies.get('tokenid')

                token = Token.query.filter_by(username=username).first()
                if token.tokenid == tokenid:
                    print('post : 已经登录了')
                    return render_template('index.html')
                else:
                    return '<h1>凭据错误 请联系管理员web administrator please</h'
            except Exception as e:
                # return '<h1>未登录</h1>'
                return 'add `/loign'
