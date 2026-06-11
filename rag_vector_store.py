"""RAG向量库 - RAG vector store management."""
from flask import Blueprint, render_template, request

rag_vector_store_bp = Blueprint('rag_vector_store_bp', __name__)


@rag_vector_store_bp.route('/rag_vector_store', methods=['GET', 'POST'])
def rag_vector_store_route():
    """RAG向量库路由"""
    info_dict = {}
    info_dict['title'] = "风机系统专家"
    info_dict['descriptions'] = [
        "自然语言交互，用户可快速获取仿真建议和技术说明，降低风机仿真系统的使用门槛，提高分析效率，为风力发电装备的设计验证提供支持",
        "运行仿真工具和分析结果（目前仅支持OpenFAST，如需支持其他工具需上传源码和配置文件）",
    ]
    info_dict['expert_url'] = "http://172.28.21.22/login"
    return render_template('rag_vector_store.html', info_dict=info_dict)
