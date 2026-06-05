"""AI+专家 - AI plus expert agent."""
from flask import Blueprint, render_template, request

ai_expert_bp = Blueprint('ai_expert_bp', __name__)


@ai_expert_bp.route('/ai_expert', methods=['GET', 'POST'])
def ai_expert_route():
    """AI+专家路由"""
    info_dict = {}
    info_dict['title'] = "AI+专家"
    info_dict['description'] = "AI驱动的智能分析与优化专家"
    return render_template('ai_expert.html', info_dict=info_dict)
