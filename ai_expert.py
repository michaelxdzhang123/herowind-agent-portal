"""AI+专家 - AI plus expert agent."""
from flask import Blueprint, render_template, request

ai_expert_bp = Blueprint('ai_expert_bp', __name__)


@ai_expert_bp.route('/ai_expert', methods=['GET', 'POST'])
def ai_expert_route():
    """AI+专家路由"""
    info_dict = {}
    info_dict['title'] = "智能体设计目标：能够帮助你完成日常工作任务并提高工作效率，是你的知识和技能的延伸，并自主迭代和进化"
    info_dict['content'] = "我是一个AI助手,可以帮助你完成日常工作任务并提高工作效率，是你的知识和技能的延伸。我可以帮助你处理各种任务，如数据分析、编程、写作等。我还可以帮助你学习新技能，提供学习资源和指导。我是一个智能体，可以不断学习和进化，以更好地满足你的需求。"
    info_dict['footer'] = "我的智能体 - AI时代个人必备工具(hernes)!"
    #return render_template('ai_expert.html', info_dict=info_dict)
    info_dict['header'] = "AI+专家 - AI plus expert agent"
    info_dict['subtitle'] = "我的智能体 - AI时代个人必备工具(hernes)!"
    info_dict['description'] = [
    "  该风电智能体以 task_profile.yaml 为统一入口,读取任务版本、循环策略、分析目标和输出要求,并按六个独立智能体自动推进:源数据提取、运行仿真、数据清洗、Excel 输出、模型分析和结果分析",
    "  系统先校验模型、环境和版本数据，再启动仿真；仿真失败时只修复依赖、路径、权限、资源等运行环境，不修改仿真程序",
    "  随后清洗标准化结果，登记 dataset path, 生成可追溯 Excel,并分析模型性能、版本差异、关键指标和异常原因。各阶段记录输入、输出、日志、版本和校验结果,支持复跑、对比、审计和人工复核，形成从数据到结论的闭环工作流",
    ]
    info_dict['header'] = "任务执行顺序"

    info_dict['content'] = [ 
    "各个模块独立发展自己的能力和skills,记忆系统，隔离边界，这样效率高，不会相互干扰，避免犯错", 

    " - 模块 source-raw-data     →  turbine, pipeline, herowind      + load raw input 数据源路径/版本  ",                                       
    " - 模块 run-simulation      →  turbine, pipeline                +  Execute simulation process: OpenFAST/Bladed/Herowind/OF 模型 参数/陷阱 ",                                     
    " - 模块post-data-clean     →  turbine, pipeline, herowind      + clean and validate output data, Yes/No 校验 loop (待细化)",                               
    " - 模块 post-data-2-excel   →  turbine, pipeline                + Bladed/Herowind/openfast Excel 格式映射",                             
    " - 模块 model-analysis      →  turbine, pipeline, herowind, ford + analysis of  NREL 5MW 全参数 + 14 深度参考",                          
    " - 模块 result-analysis     →  turbine, pipeline, herowind, cross-platform, chinese-doc + analysis final result to analysis findings, root reasons ",                                  

    " 每个 profile 的 skills 都是独立副本（非 symlink), 改了互不影响。"
    ]
    return render_template('ai_expert.html', info_dict=info_dict)
