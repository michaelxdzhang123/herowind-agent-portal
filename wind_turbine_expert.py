"""风机系统专家 - Wind turbine system expert agent."""
from flask import Blueprint, render_template, request

wind_turbine_expert_bp = Blueprint('wind_turbine_expert_bp', __name__)


@wind_turbine_expert_bp.route('/wind_turbine_expert', methods=['GET', 'POST'])
def wind_turbine_expert_route():
    """风机系统专家路由"""
    info_dict = {}
    info_dict['title'] = "风机系统专家"
    info_dict['description'] = "风力发电机组系统设计与分析专家"
    return render_template('wind_turbine_expert.html', info_dict=info_dict)
