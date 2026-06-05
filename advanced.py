"""进阶段 - Advanced coding agent."""
from flask import Blueprint, render_template, request

advanced_bp = Blueprint('advanced_bp', __name__)


@advanced_bp.route('/advanced', methods=['GET', 'POST'])
def advanced_route():
    """进阶段路由"""
    info_dict = {}
    info_dict['title'] = "进阶段"
    info_dict['description'] = "编程进阶智能体，适合有经验的开发者"
    return render_template('advanced.html', info_dict=info_dict)
