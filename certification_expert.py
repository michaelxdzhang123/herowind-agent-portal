"""认证专家 - Certification expert agent."""
from flask import Blueprint, render_template, request

certification_expert_bp = Blueprint('certification_expert_bp', __name__)


@certification_expert_bp.route('/certification_expert', methods=['GET', 'POST'])
def certification_expert_route():
    """认证专家路由"""
    info_dict = {}
    info_dict['title'] = "风电认证专家 - Certification expert agent."
    info_dict['h1'] = "风电认证专家"
    info_dict['keywords'] = "风电认证专家, 认证，标准，认证最新信息"
    info_dict['descriptions'] = [
        "自然语言交互，用户可快速获取仿真建议和技术说明，降低风机仿真系统的使用门槛，提高分析效率，为风力发电装备的设计验证提供支持",
        "运行仿真工具和分析结果（目前仅支持OpenFAST，如需支持其他工具需上传源码和配置文件）",
    ]
    info_dict['expert_url'] = "http://172.28.21.235:9998"
    return render_template('certification_expert.html', info_dict=info_dict)
