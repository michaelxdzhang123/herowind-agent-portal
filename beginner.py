"""入门段 - Beginner coding agent."""
from flask import Blueprint, render_template, request,send_from_directory

beginner_bp = Blueprint('beginner_bp', __name__)


@beginner_bp.route('/beginner', methods=['GET', 'POST'])
def beginner_route():
  
    return send_from_directory('static', 'step1.html')
    #return render_template('beginner.html', info_dict=info_dict)
