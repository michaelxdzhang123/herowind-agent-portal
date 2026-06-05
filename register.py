from flask import Blueprint, render_template, request, jsonify
from model import User, db

register_bp = Blueprint('register_bp', __name__)

@register_bp.route('/register', methods=['GET', 'POST'])
def register_endpoint():
    """
    用户注册路由，处理 GET 和 POST 请求。
    GET 请求返回注册页面，POST 请求处理表单或 JSON 格式的注册数据。

    :return: 注册结果页面或 JSON 响应
    """

    if request.method == 'GET':
        return render_template('register.html')
    else:
        if not request.is_json:
            try:
                username = request.form['username']
                password = request.form['password']
                user = User(username, password)
                db.session.add(user)
                db.session.commit()
                return '<h1>注册成功</h1>'
            except Exception as e:
                return '<h1>用户名重复</h1>'
            
        else:
            try:
                info = request.get_json(silent=True)
                user = User(info['username'], info['password'])
                db.session.add(user)
                db.session.commit()
                return jsonify({'status': 'success'})
            except Exception as e:
                return jsonify({'status': 'failed'})