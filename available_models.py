"""可用模型 - Available models."""
from flask import Blueprint, render_template, request

available_models_bp = Blueprint('available_models_bp', __name__)


@available_models_bp.route('/available_models', methods=['GET', 'POST'])
def available_models_route():
    """可用模型路由"""
    info_dict = {}
    info_dict['title'] = "可用模型"
    info_dict['description'] = "查看和管理可用的AI模型列表"
    return render_template('available_models.html', info_dict=info_dict)
