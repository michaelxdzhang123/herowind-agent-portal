"""入门段 - Beginner coding agent."""
from flask import Blueprint, render_template, request

beginner_bp = Blueprint('beginner_bp', __name__)


@beginner_bp.route('/beginner', methods=['GET', 'POST'])
def beginner_route():
    """入门段路由"""
    info_dict = {}
    info_dict['title'] = "入门段"
    info_dict['description'] = "编程入门智能体，适合初学者"
    return render_template('beginner.html', info_dict=info_dict)
