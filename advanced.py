"""进阶段 - Advanced coding agent."""
from flask import Blueprint, render_template, request,send_from_directory

advanced_bp = Blueprint('advanced_bp', __name__)


@advanced_bp.route('/advanced', methods=['GET', 'POST'])
def advanced_route():
    
    return send_from_directory('static', 'step2.html')
