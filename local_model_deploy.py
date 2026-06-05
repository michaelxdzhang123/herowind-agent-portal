"""本地模型部署 - Local model deployment."""
from flask import Blueprint, render_template, request

local_model_deploy_bp = Blueprint('local_model_deploy_bp', __name__)


@local_model_deploy_bp.route('/local_model_deploy', methods=['GET', 'POST'])
def local_model_deploy_route():
    """本地模型部署路由"""
    info_dict = {}
    info_dict['title'] = "本地模型部署"
    info_dict['description'] = "本地AI模型的部署与管理"
    return render_template('local_model_deploy.html', info_dict=info_dict)
