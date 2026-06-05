from flask import Blueprint, render_template, request,redirect,g
from model import User, Token, db

index_v1_bp = Blueprint('index_v1_bp', __name__)
@index_v1_bp.route('/index_v1', methods=['GET', 'POST'])
def index_v1_route():
    """
    首页 V1 版本路由，处理 GET 和 POST 请求。
    验证用户登录状态，若已登录则渲染 index_v1.html 模板，否则重定向到登录页面。

    :return: index_v1.html 模板或重定向响应
    """

    #print('------------------g.name', g.name)
    if request.method == 'GET':
        try:
            username = request.cookies.get('username')
            tokenid = request.cookies.get('tokenid')
            token = Token.query.filter_by(username=username).first()
            if token.tokenid == tokenid:
                #已经登录了
                print('get : 已经登录了 now index_v1')
                return render_template('index_v1.html')
            else:
                return redirect("login")
        except Exception as e:
            #return '<h1>未登录</h1>'
            return 'add /loign'

    else:
        return render_template('index_v1.html')



if __name__ == '__main__':
    jql_name = 'project = CR AND status = 需求确认 ORDER BY key ASC'
    myjira = JIRA (Jiras['url1'], basic_auth=(Jiras['username1'], Jiras['password1']))  # 创建jira链接



    te
    issue = myjira.issue('CR-35')
    transitions = myjira.transitions(issue)
    #[(t['id'],t['name']) for t in transitions]
    print (transitions)

    id_trans_verify = {'CR-需求开发':{'yes':'31', 'no':101},
               'CR-中高风速产品团队':{'yes':'61', 'no':81}}
    """try:
        username = request.cookies.get('username')
        tokenid = request.cookies.get('tokenid')

        token = Token.query.filter_by(username=username).first()
        if token.tokenid == tokenid:
            return render_template('index_v1.html')
        else:
            return '<h1>凭据错误 请联系管理员web administrator please</h'
    except Exception as e:
        # return '<h1>未登录</h1>'
        return render_template('login.html')
    """