"""RAG向量库 - RAG vector store management."""
from flask import Blueprint, render_template, request

rag_vector_store_bp = Blueprint('rag_vector_store_bp', __name__)


@rag_vector_store_bp.route('/rag_vector_store', methods=['GET', 'POST'])
def rag_vector_store_route():
    """RAG向量库路由"""
    info_dict = {}
    info_dict['title'] = "RAG向量库"
    info_dict['description'] = "检索增强生成的向量知识库管理"
    return render_template('rag_vector_store.html', info_dict=info_dict)
