# coding: utf-8

import os
from flask import Flask, redirect, render_template, request
from config import Config
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from pyecharts.charts import Line

from auth_token import token_bp
from login import login_bp
from register import register_bp
from model import db, User, Token
from index import index_bp
from index_v1 import index_v1_bp
#from run_show import run_show_bp
from setup_zone import setup_zone_bp
from bbs_aero import bbs_aero_bp
from wind_turbine_expert import wind_turbine_expert_bp
from certification_expert import certification_expert_bp
from ai_expert import ai_expert_bp
from beginner import beginner_bp
from advanced import advanced_bp
from self_evolution import self_evolution_bp
from rag_vector_store import rag_vector_store_bp
from local_model_deploy import local_model_deploy_bp
from available_models import available_models_bp
from runtime_monitor import runtime_monitor_bp
from key_management import key_management_bp
from guide_key import guide_key_bp
app = Flask(__name__,instance_relative_config=True)
#app.config.from_object(Config)
#app.config.from_pyfile('config.py')

basedir = os.path.abspath(os.path.dirname(__file__))
# 初始化数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data/data.sqlite')
db.init_app(app)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
#test env vars
app.register_blueprint(bbs_aero_bp)
app.register_blueprint(token_bp)
app.register_blueprint(login_bp)
app.register_blueprint(register_bp)
app.register_blueprint(index_bp)
app.register_blueprint(index_v1_bp)
app.register_blueprint(setup_zone_bp)
app.register_blueprint(wind_turbine_expert_bp)
app.register_blueprint(certification_expert_bp)
app.register_blueprint(ai_expert_bp)
app.register_blueprint(beginner_bp)
app.register_blueprint(advanced_bp)
app.register_blueprint(self_evolution_bp)
app.register_blueprint(rag_vector_store_bp)
app.register_blueprint(local_model_deploy_bp)
app.register_blueprint(available_models_bp)
app.register_blueprint(runtime_monitor_bp)
app.register_blueprint(key_management_bp, url_prefix='/flask_gateway')
app.register_blueprint(guide_key_bp)
admin = Admin(app, name='test', url='/stone_admin')
admin.add_view(ModelView(User, db))
admin.add_view(ModelView(Token, db))
#,index_view=MyAdminIndexView(),#官方案例中是通过实现这个类，进行登录登出控制
base_template='my_master.html'#基础模板的名字，默认会在全局templates文件夹根目录下寻找)

@app.route('/')
def index_route():
    """
    直接跳转管理系统
    """
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)
# check
    """
    try:
        username = request.cookies.get('username')
        tokenid = request.cookies.get('tokenid')
        token = Token.query.filter_by(username=username).first()
        if token.tokenid == tokenid:
            #已经登录了
            print('get : 已经登录了')
            return render_template('index.html')
        else:
            return '<h1>凭据错误 请联系管理员web administrator please</h'
    except Exception as e:
        # return '<h1>未登录</h1>'
        return 'add /loign'
    """
