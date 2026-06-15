"""AI+专家 - AI plus expert agent."""
from flask import Blueprint, render_template, request

ai_expert_bp = Blueprint('ai_expert_bp', __name__)


@ai_expert_bp.route('/ai_expert', methods=['GET', 'POST'])
def ai_expert_route():
    """AI+专家路由"""
    info_dict = {}
    info_dict['title'] = "智能体设计--基于多智能体协调的风电智能体设计"
    info_dict['description'] = ["1. 该风电智能体以 task_profile.yaml 为统一入口，读取任务版本、循环策略、分析目标和输出要求，并按六个独立智能体自动推进：源数据提取、运行仿真、数据清洗、Excel 输出、模型分析和结果分析",
    " 2.系统先校验模型、环境和版本数据，再启动仿真；仿真失败时只修复依赖、路径、权限、资源等运行环境，不修改仿真程序",
    " 3. 随后清洗标准化结果，登记 dataset path，生成可追溯 Excel，并分析模型性能、版本差异、关键指标和异常原因。各阶段记录输入、输出、日志、版本和校验结果，支持复跑、对比、审计和人工复核，形成从数据到结论的闭环工作流",
    ]
    return render_template('ai_expert.html', info_dict=info_dict)
