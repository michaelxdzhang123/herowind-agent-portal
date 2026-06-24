"""目标分解 — 将复杂编程任务分解为可执行的子任务."""
from flask import Blueprint, render_template, request

goal_decomposition_bp = Blueprint('goal_decomposition_bp', __name__)


@goal_decomposition_bp.route('/goal_decomposition', methods=['GET', 'POST'])
def goal_decomposition():
    info_dict = {}
    info_dict['title'] = "智能编程是最终目标--知识和代码同时自学习--任务完成"
    info_dict['description'] = ["1.  入门段：以交互对话生成代码，可以看到产生的代码并只有你点击,<approve> 或绿色对号后才放入代码文件,测试需要人工点击<Run>按钮 ",\
     " 2. 进阶段: 首先可以在<plan> 阶段写好AGENTS.md/Claude.md后告诉智能体自动生成代码和测试,如遇到错误可以自动修复代码和环境来完成任务", \
     " 3. 自进化段:智能体自学习并不断补充甚至帮你产生技能skills, 包括学习知识，代码库有专门的知识图谱，能够闭环完成较大的项目，这个特点是每个人都要有这样的智能体，这是一个互动和学习进化的过程，这个时候编程已经不是瓶颈，你的主要精力放到：提出问题 定义目标 评价结果 创新决策 上面了"

    ]
    return render_template('goal_decomposition.html', info_dict=info_dict)
