"""
    BladeAI.flask
    Author: MichaelZhang in beijing
    Licence: MIT
"""
from flask import Blueprint, render_template, request,redirect,Flask
from model import User, db
import time
import pickle
import pandas as pd
import os
import sys
import json
import random
import numpy as np
import re
from shutil import copyfile
from ruamel import yaml
from ruamel.yaml import YAML
import logging
import socket
from openpyxl import load_workbook

from werkzeug.utils import secure_filename
from config import Config
app = Flask(__name__,instance_relative_config=True)
app.config.from_object(Config)
#app.config.from_pyfile('config.py')

bbs_aero_bp = Blueprint('bbs_aero_bp', __name__)
@bbs_aero_bp.route('/bbs_aero', methods=['GET', 'POST'])
def bbs_aero_route():
    """
    BBS Aero 路由，处理 GET 和 POST 请求。
    获取当前登录用户并重定向到指定服务地址。

    :return: 重定向响应
    """

    my_user = request.cookies.get('username')
    #my_pub = os.path.join(app.config['WORKING_DIR'], my_user, 'pub.json')
    #fp = open(my_pub, 'r', encoding=u'utf-8', errors='ignore')
    #js_vars = json.load(fp)
    #fp.close()
    if request.method == 'GET':
        #give_status_bar(0, my_user)
        interface={}
        val_level_dict = {}
        return redirect("http://127.0.0.1:8551")
    else:
        if not request.is_json:
            return redirect("http://127.0.0.1:8551")
           

