"""认证专家 - Certification expert agent."""
from flask import Blueprint, render_template, request

certification_expert_bp = Blueprint('certification_expert_bp', __name__)


@certification_expert_bp.route('/certification_expert', methods=['GET', 'POST'])
def certification_expert_route():
    """认证专家路由"""
    info_dict = {}
    info_dict['title'] = "认证专家"
    info_dict['description'] = "风机认证与合规性分析专家"
    return render_template('certification_expert.html', info_dict=info_dict)
