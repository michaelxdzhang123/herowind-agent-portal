"""我的智能体 — 个人 AI Agent 管理面板."""
from flask import Blueprint, render_template, request

my_agent_bp = Blueprint('my_agent_bp', __name__)


@my_agent_bp.route('/my-agent', methods=['GET', 'POST'])
def my_agent():
    info_dict = {}
    info_dict['title'] = "能力展示对话和结果："
    info_dict['subtitle'] = "我的智能体 - AI"
    info_dict['header'] = ""
    info_dict['subheader'] = "在这里，您可以查看和管理分配给您的智能体的任务、进度以及与它们的历史对话。"
    info_dict['content'] = [
        "任务运行：查看当前分配给智能体的任务列表，并跟踪其进度。",
        "会话历史：浏览与各智能体的历史对话记录，以便更好地理解智能体的行为和决策过程。",
        "设置与配置：调整智能体的参数和行为，以满足特定需求。"
    ]
    return render_template('my_agent.html', info_dict=info_dict)
