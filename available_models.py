"""可用模型 - Available models."""
from flask import Blueprint, render_template, request

available_models_bp = Blueprint('available_models_bp', __name__)


@available_models_bp.route('/available_models', methods=['GET', 'POST'])
def available_models_route():
    """可用模型路由"""
    info_dict = {}
    info_dict['title'] = "可用模型"
    info_dict['descriptions'] = [
        "1. 分析和编程功能大模型：Qwen3, 具体型号：Qwen3.6-27B-FB8, 部署地址：http://172.28.21.22:8000",
        "2. embedding 大模型 Qwen3-Embedding-8B-Q4_K_M：http://172.28.21.22:11434",
        "3. 代码补全大模型：qwen2.5-coder-7b-instruct-q3_k_m：http://172.28.21.22:11434",
    ]
    info_dict['code_repo'] = "本地AI模型的部署与管理的代码开发记录（vllm, continue, litegateway）"
    info_dict['code_repo_url'] = "http://172.28.21.22:3000/AI-agent/AI-agent-logs.git"
    return render_template('available_models.html', info_dict=info_dict)
