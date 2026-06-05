from flask import Blueprint, render_template, request,redirect
from model import User, db

setup_zone_bp = Blueprint('setup_zone_bp', __name__)
@setup_zone_bp.route('/setup_zone', methods=['GET', 'POST'])
def setup_zone_route():
    """
    设置区域路由，处理 GET 和 POST 请求。
    返回 IPD 流程相关的简介信息并渲染 setup_zone.html 模板。

    :return: setup_zone.html 模板及信息字典
    """

    if request.method == 'GET':
        info_dict={}
        info_dict['简介:'] = "针对风力发电机组集成开发IPD流程，其核心体系流程包括需求管理（RM）、市场规划 (MP)、产品立项管理 (CDP)， 及产品开发管理体系 (IPD)其中，需求管理是所有流程体系的基础，其独立又和其余三大流程体系紧密相关，不可或缺。"
        info_dict['总体图:'] = "需求管理由5个阶段组成：需求开发、需求分析、需求分发、需求实现和需求验证，4个阶段都要设计相应的流程和具体内容；需求管理流程以需求的信息流转为主线，贯穿整个需求的开发、分析、分发、实现、验证等全过程，并且涵盖需求变更的可能行。"
        #info_dict['阶段介绍'] = ""
        #info_dict['需求开发--'] = ""
        #info_dict['需求分析--'] = ""
        #info_dict['需求分发--'] = ""
        #info_dict['需求验证--'] = ""
        return render_template ('setup_zone.html', info_dict=info_dict)

    else:
        if not request.is_json:
            info_dict = {}
            info_dict['简介'] = "针对风力发电机组集成开发IPD流程，其核心体系流程包括需求管理（RM）、市场规划 (MP)、产品立项管理 (CDP)， 及产品开发管理体系 (IPD)其中，需求管理是所有流程体系的基础，其独立又和其余三大流程体系紧密相关，不可或缺。"
            info_dict['需求管理总体图'] = "需求管理由5个阶段组成：需求开发、需求分析、需求分发、需求实现和需求验证，4个阶段都要设计相应的流程和具体内容；需求管理流程以需求的信息流转为主线，贯穿整个需求的开发、分析、分发、实现、验证等全过程，并且涵盖需求变更的可能行。"
            return render_template ('setup_zone.html', info_dict=info_dict)


if __name__ == '__main__':
    jql_name = 'project = CR AND status = 需求确认 ORDER BY key ASC'
    myjira = JIRA (Jiras['url1'], basic_auth=(Jiras['username1'], Jiras['password1']))  # 创建jira链接
    issue = myjira.issue('CR-35')
    transitions = myjira.transitions(issue)
    #[(t['id'],t['name']) for t in transitions]
    print (transitions)

    id_trans_verify = {'CR-需求开发':{'yes':'31', 'no':101},
               'CR-中高风速产品团队':{'yes':'61', 'no':81}}
