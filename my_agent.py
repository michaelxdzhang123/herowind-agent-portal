"""我的智能体 — 个人 AI Agent 管理面板."""
from flask import Blueprint, render_template, request

my_agent_bp = Blueprint('my_agent_bp', __name__)


@my_agent_bp.route('/my-agent', methods=['GET', 'POST'])
def my_agent():
    info_dict = {}
    info_dict['title'] = "能力展示对话和结果："
    info_dict['subtitle'] = "我的智能体 - AI时代个人必备工具（hernes）！"
    info_dict['header'] = ""
    info_dict['subheader'] = "在这里，您可以查看和管理分配给您的智能体的任务、进度以及与它们的历史对话。"
    info_dict['content'] = [
        "会话完成任务运行：通过各种方式，命令行方式、微信方式 让智能体为你工作",
        "分析仿真模型和结果数据对比：浏览与各智能体的历史对话记录，以便更好地理解智能体的行为和决策过程。",
        "让智能体按任务列表执行：科研通过对话告诉任务有什么，或者按照那个文件的列表里面的工作进行工作。",
        "智能体已有部分分析输出： http://172.28.21.141:3004/s/Test",
        "我的智能体开发代码：http://172.28.21.22:3000/AI-agent/hermes-post-expert.git ",
        "下面的例子是 让智能体计算openfast DLC1.2 工况并把结果输出到Excel文件的会话",
    ]
    return render_template('my_agent.html', info_dict=info_dict)
