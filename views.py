# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from farmInsightPro.powernestaepAlgorithm import powerNestAEP_noReport
# from models import User

from farmInsightPro import forms
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import json
import xlrd
import sys
import json as js

reload(sys)
sys.setdefaultencoding('UTF-8')


# Create your views here.

# 登录
def login(request):
    """
    用户登录视图，验证用户身份并登录系统。

    :param request: Django 请求对象
    :return: 登录成功重定向到首页，否则返回登录页面
    """

    if request.method == "POST":
        uf = forms.UserForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                response = HttpResponseRedirect('/index/')
                return response
            else:
                return HttpResponseRedirect('/login_error/')
    else:
        uf = forms.UserForm()
    return render(request, 'login.html', {'uf': uf})


# 登出
def logout(request):
    """
    用户登出视图，注销当前用户会话。

    :param request: Django 请求对象
    :return: 登出页面
    """

    auth.logout(request)
    return render(request, 'logout.html')


# 侧边栏
# @login_required  # 此行逻辑是：只有登录之后，才可以访问主页，否则拒绝
@login_required
def index(request):
    """
    首页（侧边栏）视图，登录后可访问。

    :param request: Django 请求对象
    :return: 首页模板
    """

    return render(request, 'index.html')


# 主页
@login_required
def index_v1(request):
    """
    主页 V1 版本视图，登录后可访问。

    :param request: Django 请求对象
    :return: 主页 V1 模板
    """

    return render(request, 'index_v1.html')


# ——————————————以下是单风参比对(旧版风参)—————————————————— #
@login_required  # 单风参比对上传(旧版风参)
def wind_check_upload(request):
    """
    单风参比对文件上传视图（旧版风参），处理文件上传并保存到数据库。

    :param request: Django 请求对象
    :return: 上传页面及文件列表
    """

    from models import WindCheck_upload
    if request.method == 'POST':
        files = request.FILES.getlist("files")
        for f in files:
            file_model = WindCheck_upload()
            file_model.file_field = f
            file_model.save()
    else:
        my_form = forms.windcheck_upload()
    file_list = WindCheck_upload.objects.all()
    return render(request, 'windcheck/wind_check_upload.html',
                  {'file_list': file_list})


@login_required  # 单风参比对(旧版风参)
def wind_check(request):
    """
    单风参比对视图（旧版风参），调用算法进行风参比对计算。

    :param request: Django 请求对象
    :return: 比对结果页面或比对页面
    """

    from models import WindCheck_upload
    from farmInsightPro.windcheckAlgorithm import windcheck
    if request.method == 'POST':
        wcwindfilepath1 = request.POST.get("wcwindfilepath", None)
        windturchose1 = request.POST['windturchose1']  # 选取下拉菜单值
        windturchose2 = request.POST['windturchose2']  # 选取下拉菜单值
        wcwindfilepath = r'//1002DZ050487X/FarmInsight_DataAndReport/' + wcwindfilepath1

        # 调用windcheck函数
        context = windcheck.windCheck(wcwindfilepath, windturchose1, windturchose2)
        context["wcwindfilepath"] = wcwindfilepath1
        if wcwindfilepath is not None:
            return render(request, 'windcheck/wind_check_result.html', context)
        else:
            return HttpResponseRedirect('/wind_check/')
    file_list = WindCheck_upload.objects.all()
    return render(request, 'windcheck/wind_check.html', {'file_list': file_list})


@login_required  # 单风参比对结果(旧版风参)
def wind_check_result(request):
    """
    单风参比对结果视图（旧版风参）。

    :param request: Django 请求对象
    :return: 比对结果模板
    """

    return render(request, 'windcheck/wind_check_result.html')


# ————————————————————————————————————————————— #


# ——————————————以下是单风参比对(新版风参)—————————————————— #
@login_required  # 单风参比对上传(新版风参)
def wind_check_upload_newIEC(request):
    """
    单风参比对文件上传视图（新版风参），处理文件上传并保存到数据库。

    :param request: Django 请求对象
    :return: 上传页面及文件列表
    """

    from models import WindCheck_upload_newIEC
    if request.method == 'POST':
        files = request.FILES.getlist("files")
        for f in files:
            file_model = WindCheck_upload_newIEC()
            file_model.file_field = f
            file_model.save()
    else:
        my_form = forms.windcheck_upload_newIEC()
    WindCheck_upload_newIEC.objects.order_by("file_time")  # 按时间排序
    file_list = WindCheck_upload_newIEC.objects.all()
    return render(request, 'windcheck_newIEC/wind_check_upload_newIEC.html',
                  {'file_list': file_list})


@login_required  # 单风参比对(新版风参)
def wind_check_newIEC(request):
    """
    单风参比对视图（新版风参），调用算法进行风参比对计算。

    :param request: Django 请求对象
    :return: 比对结果页面或比对页面
    """

    from models import WindCheck_upload_newIEC
    from farmInsightPro.windcheckAlgorithm_newIEC import windcheck_newIEC
    if request.method == 'POST':
        wcwindfilepath1 = request.POST.get("wcwindfilepath", None)
        windturchose1 = request.POST['windturchose1']  # 选取下拉菜单值
        windturchose2 = request.POST['windturchose2']  # 选取下拉菜单值
        wcwindfilepath = r'//1002DZ050487X/FarmInsight_DataAndReport/' + wcwindfilepath1

        # 调用windcheck函数
        context = windcheck_newIEC.windCheck_newIEC(wcwindfilepath, windturchose1, windturchose2)
        context["wcwindfilepath"] = wcwindfilepath1
        # fi = {"wcwindfilepath": wcwindfilepath}
        if wcwindfilepath is not None:
            return render(request, 'windcheck_newIEC/wind_check_result_newIEC.html', context)
        else:
            return HttpResponseRedirect('/wind_check_newIEC/')
    file_list = WindCheck_upload_newIEC.objects.all()
    return render(request, 'windcheck_newIEC/wind_check_newIEC.html', {'file_list': file_list})


@login_required  # 单风参比对结果(新版风参)
def wind_check_result_newIEC(request):
    """
    单风参比对结果视图（新版风参）。

    :param request: Django 请求对象
    :return: 比对结果模板
    """

    return render(request, 'windcheck_newIEC/wind_check_result_newIEC.html')


# ————————————————————————————————————————————— #


@login_required  # 多风参统计
def winds_check(request):
    """
    多风参统计视图。

    :param request: Django 请求对象
    :return: 多风参统计页面
    """

    return render(request, 'winds_check.html')


# ——————————————以下是功率曲线定制化—————————————— #
@login_required  # 功率曲线定制化文件上传
def power_fit_upload(request):
    """
    功率曲线定制化文件上传视图，处理风资源、推力、标准及湍流文件的上传。

    :param request: Django 请求对象
    :return: 上传页面及文件列表
    """

    from models import Powerfit_upload, Powerfit_thrust_upload, Powerfit_standard_upload, Powerfit_turbulence_upload
    if request.method == 'POST':
        windresource_files = request.FILES.getlist("files")
        thrust_files = request.FILES.getlist("thrustfiles")
        standard_files = request.FILES.getlist("standardfiles")
        turbulence_files = request.FILES.getlist("turbulencefiles")
        for f in windresource_files:
            file_model = Powerfit_upload()
            file_model.file_field = f
            file_model.save()
        for i in thrust_files:
            file_model_thrust = Powerfit_thrust_upload()
            file_model_thrust.file_field = i
            file_model_thrust.save()
        for j in standard_files:
            file_model_standard = Powerfit_standard_upload()
            file_model_standard.file_field = j
            file_model_standard.save()
        for k in turbulence_files:
            file_model_turbulence = Powerfit_turbulence_upload()
            file_model_turbulence.file_field = k
            file_model_turbulence.save()
    else:
        my_form = forms.powerfit_upload()
        my_form_thrust = forms.powerfit_thrust_upload()
        my_form_standard = forms.powerfit_standard_upload()
        my_form_turbulence = forms.powerfit_turbulence_upload()
    file_list = Powerfit_upload.objects.all()
    file_list_thrust = Powerfit_thrust_upload.objects.all()
    file_list_standard = Powerfit_standard_upload.objects.all()
    file_list_turbulence = Powerfit_turbulence_upload.objects.all()
    return render(request, 'powerfit/power_fit_upload.html',
                  {'file_list': file_list, 'file_list_thrust': file_list_thrust,
                   'file_list_standard': file_list_standard, 'file_list_turbulence': file_list_turbulence})


@login_required  # 功率曲线定制化
def power_fit(request):
    """
    功率曲线定制化视图，调用算法进行功率曲线定制化计算。

    :param request: Django 请求对象
    :return: 计算结果页面或功率曲线页面
    """

    from farmInsightPro.powerfitAlgorithm import powerFit
    from models import Powerfit_upload, Powerfit_thrust_upload, Powerfit_standard_upload, Powerfit_turbulence_upload
    if request.method == 'POST':
        pfwindfilepath1 = request.POST.get("pfwindfilepath", None)
        pfthrustpath1 = request.POST.get("pfthrustfilepath", None)
        pfstandardpath1 = request.POST.get("pfstandardfilepath", None)
        pfturbulencepath1 = request.POST.get("pfturbulencefilepath", None)
        pfwindfilepath = r'//1002DZ050487X/FarmInsight_DataAndReport/' + pfwindfilepath1
        pfthrustpath = r'//1002DZ050487X/FarmInsight_DataAndReport/' + pfthrustpath1
        pfstandardpath = r'//1002DZ050487X/FarmInsight_DataAndReport/' + pfstandardpath1
        pfturbulencepath = r'//1002DZ050487X/FarmInsight_DataAndReport/' + pfturbulencepath1

        resultfilepath = pfwindfilepath1.lstrip(u'power_fit/power_fit_data/')
        resultfilepath1 = resultfilepath.replace(u'/', u'_')

        # 调用powerFit函数
        context = powerFit.powerfit(pfwindfilepath, pfthrustpath, pfstandardpath, pfturbulencepath, resultfilepath1)

        if pfwindfilepath is not None:
            return render(request, 'powerfit/power_fit_result.html', context)
        else:
            return HttpResponseRedirect('/power_Fit/')
    file_list = Powerfit_upload.objects.all()
    file_list_thrust = Powerfit_thrust_upload.objects.all()
    file_list_standard = Powerfit_standard_upload.objects.all()
    file_list_turbulence = Powerfit_turbulence_upload.objects.all()
    return render(request, 'powerfit/power_fit.html',
                  {'file_list': file_list, 'file_list_thrust': file_list_thrust,
                   'file_list_standard': file_list_standard,
                   'file_list_turbulence': file_list_turbulence})


@login_required  # 功率曲线定制化计算结果
def power_fit_result(request):
    """
    功率曲线定制化计算结果视图。

    :param request: Django 请求对象
    :return: 计算结果模板
    """

    return render(request, 'powerfit/power_fit_result.html')


@login_required
def powerfit_result_download(request):
    """
    功率曲线定制化结果下载视图，返回计算结果文件。

    :param request: Django 请求对象
    :return: 文件下载响应
    """

    from django.http import FileResponse
    from farmInsightPro.powerfitAlgorithm import powerFit
    the_path = powerFit.get_path()
    the_file = open(the_path, 'rb')
    the_name = the_path.lstrip(r'//1002DZ050487X/FarmInsight_DataAndReport/power_fit/power_fit_resultdata/')
    response = FileResponse(the_file)
    # print the_name
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="' + the_name.encode("utf-8") + '"'
    return response


# —————————————————————————————————————————————— #


# ——————————————以下AEP计算—————————————————————— #
@login_required  # AEP上传
def AEP_calculation_upload(request):
    """
    AEP 计算文件上传视图，处理风资源和功率曲线文件的上传。

    :param request: Django 请求对象
    :return: 上传页面及文件列表
    """

    from models import AEP_upload, AEP_power_upload
    if request.method == 'POST':
        windresource_files = request.FILES.getlist("windresourcefiles")
        powercurve_files = request.FILES.getlist("powercurvefiles")
        for f in windresource_files:
            file_model = AEP_upload()
            file_model.file_field = f
            file_model.save()
        for j in powercurve_files:
            file_model_power = AEP_power_upload()
            file_model_power.file_field = j
            file_model_power.save()
    else:
        my_form = forms.aepcalculation_upload()
        my_form_power = forms.aepcalculation_powercurve_upload()
    file_list = AEP_upload.objects.all()
    file_list_power = AEP_power_upload.objects.all()
    return render(request, 'AEPcalculation/AEP_calculation_upload.html',
                  {'file_list': file_list, 'file_list_power': file_list_power})


@login_required  # AEP计算
def AEP_calculation(request):
    """
    AEP 计算视图，调用算法进行年发电量计算。

    :param request: Django 请求对象
    :return: 计算结果页面或 AEP 计算页面
    """

    from models import AEP_upload, AEP_power_upload
    from farmInsightPro.AEPcalculation import aepcalculation
    if request.method == 'POST':
        acwindfilepath1 = request.POST.get("acwindfilepath", None)
        acpowercurvepath1 = request.POST.get("acpowerfilepath", None)
        acwindfilepath = r'//1002DZ050487X/FarmInsight_DataAndReport/' + acwindfilepath1
        acpowercurvepath = r'//1002DZ050487X/FarmInsight_DataAndReport/' + acpowercurvepath1

        # 调用windcheck函数
        context = aepcalculation.AEP_Calculation(acwindfilepath, acpowercurvepath)
        context["acwindfilepath"] = acwindfilepath1
        if acwindfilepath is not None:
            return render(request, 'AEPcalculation/AEP_calculation_result.html', context)
        else:
            return HttpResponseRedirect('/AEP_calculation/')
    file_list = AEP_upload.objects.all()
    file_list_power = AEP_power_upload.objects.all()
    return render(request, 'AEPcalculation/AEP_calculation.html',
                  {'file_list': file_list, 'file_list_power': file_list_power})


@login_required  # AEP计算计算结果
def AEP_calculation_result(request):
    """
    AEP 计算结果视图。

    :param request: Django 请求对象
    :return: 计算结果模板
    """

    return render(request, 'AEPcalculation/AEP_calculation_result.html')


# —————————————————————————————————————————————— #


# 塔架定制化

# towerfit数据上传
@login_required
def tower_fit_upload(request):
    """
    塔架定制化数据上传视图，处理塔架相关文件的上传。

    :param request: Django 请求对象
    :return: 上传页面及文件列表
    """

    from models import TowerFit_upload
    if request.method == "POST":
        file_list = request.FILES.getlist("files")
        for f in file_list:
            file_model = TowerFit_upload()
            file_model.file_field = f
            file_model.save()
    else:
        my_form = forms.towerfit_upload()
    TowerFit_upload.objects.order_by("file_time")
    file_list = TowerFit_upload.objects.all()
    return render(request, 'towerfit/towerfit_info_update/tower_fit_upload.html', {"file_list": file_list})


# towerfit数据库更新
@login_required
def tower_fit_update(request):
    """
    塔架定制化数据库更新视图，将塔架参数写入数据库。

    :param request: Django 请求对象
    :return: 更新结果页面或更新页面
    """

    from farmInsightPro.towerfitAlgorithm import towerfit_update
    from models import TowerFit_upload
    database = r'\\1002DZ050487X\FarmInsight_DataAndReport\controller_fit\controller_fit_database\Controller_Fit_Projects.xlsx'
    if request.method == "POST":
        date = request.POST.get("date")
        turbineType = request.POST.get("turbineType")
        towerType = request.POST.get("towerType")
        bladeType = request.POST.get("bladeType")
        project_name = request.POST.get("project_name")
        tower_ID = request.POST.get("tower_ID")
        towerWeight = request.POST.get("towerWeight")
        towerDiameter = request.POST.get("towerDiameter")
        towerFreq = request.POST.get("towerFreq")
        province = request.POST.get("province")
        controller_name = request.POST.get("controllername")
        parameter_name = request.POST.get("parametername")
        project_author = request.POST.get("projectauthor")
        remark = request.POST.get("remark")
        windfile1 = request.POST["wcwindfilepath"]
        windfile = r'//1002DZ050487X/FarmInsight_DataAndReport/' + windfile1
        towerfit_update.writeValue(windfile, date, turbineType, towerType, tower_ID, towerDiameter, towerWeight,
                                   towerFreq, bladeType, province, project_name, controller_name, parameter_name,
                                   project_author, remark)
        return render(request, 'towerfit/towerfit_info_update/tower_fit_update_result.html')
    TowerFit_upload.objects.order_by("file_time")
    file_list = TowerFit_upload.objects.all()
    context = towerfit_update.get_options(database)
    context["file_list"] = file_list
    return render(request, 'towerfit/towerfit_info_update/tower_fit_update.html', context)


# towerfit数据库更新结果
@login_required
def tower_fit_update_result(request):
    """
    塔架定制化数据库更新结果视图。

    :param request: Django 请求对象
    :return: 更新结果模板
    """

    return render(request, 'towerfit/towerfit_info_update/tower_fit_update_result.html')


# towerfit数据库下载
@login_required
def tower_database_download(request):
    """
    塔架定制化数据库下载视图，返回数据库 Excel 文件。

    :param request: Django 请求对象
    :return: 文件下载响应
    """

    from django.http import StreamingHttpResponse
    def file_iterator(file_name, chunk_size=512):
        """
        文件迭代器，按块读取文件内容用于流式下载。

        :param file_name: 文件路径
        :type file_name: str
        :param chunk_size: 每次读取的字节数，默认 512
        :type chunk_size: int
        :return: 文件内容块生成器
        """
        with open(file_name, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    the_file_name = "//1002DZ050487X/FarmInsight_DataAndReport/controller_fit/controller_fit_database/Controller_Fit_Projects.xlsx"
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/vnd.ms-excel'
    response['Content-Disposition'] = 'attachment;filename=" 定制化模板.xlsx"'
    return response


# towerfit分析
@login_required
def tower_fit_analysis(request):
    """
    塔架定制化分析视图，根据条件查询并比对塔架数据库。

    :param request: Django 请求对象
    :return: 分析结果页面或分析页面
    """

    from models import TowerFit_upload
    from farmInsightPro.towerfitAlgorithm import towerfit_calculation_new
    # 数据库路径，固定值
    database = r'\\1002DZ050487X\FarmInsight_DataAndReport\controller_fit\controller_fit_database\Controller_Fit_Projects.xlsx'
    if request.method == "POST":
        windfile1 = request.POST["wcwindfilepath"]
        turbine_type = request.POST["turbine_type"]
        tower_type = request.POST["tower_type"]
        tower_id = request.POST["tower_id"]
        blade_type = request.POST["blade_type"]
        project_name = request.POST["project_name"]
        item_to_show = request.POST["item_to_show"]
        if item_to_show == '':
            item_to_show = 0
        else:
            item_to_show = int(item_to_show)
        windfile = r'//1002DZ050487X/FarmInsight_DataAndReport/' + windfile1
        context = towerfit_calculation_new.compareValue2(item_to_show, database, windfile, project_name, turbine_type,
                                                         tower_type, tower_id, blade_type)
        # the_name = context["the_name"]
        # the_num = context["the_num"]
        context["project_name"] = project_name
        context["turbine_type"] = turbine_type
        context["tower_type"] = tower_type
        context["tower_id"] = tower_id
        context["blade_type"] = blade_type
        context["wcwindfilepath"] = windfile1
        the_list = context["info"]
        # 若搜索无结果
        if len(the_list) == 0:
            # the_list = 0
            context["info"] = 0
        # suggest = context["suggest"]
        return render(request, 'towerfit/towerfit_analysis/tower_fit_result.html', context)

    TowerFit_upload.objects.order_by("file_time")
    file_list = TowerFit_upload.objects.all()
    context = towerfit_calculation_new.get_options(database)
    context["file_list"] = file_list
    return render(request, 'towerfit/towerfit_analysis/tower_fit_analysis.html', context)


# towerfit分析结果
@login_required
def tower_fit_result(request):
    """
    塔架定制化分析结果视图。

    :param request: Django 请求对象
    :return: 分析结果模板
    """

    return render(request, 'towerfit/towerfit_analysis/tower_fit_result.html')


# 风参边界比对
@login_required
def turbine_check(request):
    """
    风参边界比对视图。

    :param request: Django 请求对象
    :return: 风参边界比对页面
    """

    return render(request, 'turbine_check.html')


# ———————————————以下能巢方案—————————————————————— #
# @login_required()
# def power_nest_AEP_upload(request):
#     from models import PowerNestAEP_upload
#     if request.method == 'POST':
#         files = request.FILES.getlist("files")
#         for f in files:
#             file_model = PowerNestAEP_upload()
#             file_model.file_field = f
#             file_model.save()
#             # return HttpResponse('ok')
#     else:
#         my_form = forms.powernestAEP_upload()
#     file_list = PowerNestAEP_upload.objects.all()
#     return render(request, 'powernestAEP/power_nest_AEP_upload.html',
#                   {'file_list': file_list})
#
#
# @login_required  # 能巢方案
# def power_nest_AEP(request):
#     from models import PowerNestAEP_upload
#
#     if request.method == 'POST':
#         windfilepath = request.POST.get("windfilepath", None)
#         project_name = request.POST.get("projectname", None)
#         # projectinfo = request.POST.get("projectinfo", None)
#         protitlename = project_name
#         author_name = request.POST.get("reportauthor", None)
#         # outputfile = request.POST.get("outputfile", None)
#
#         yawerror_choose = request.POST.get("yawerror_choose", None)
#         power_choose = request.POST.get("power_choose", None)
#         kopt_choose = request.POST.get("kopt_choose", None)
#
#         windfilepath = r'//1002DZ050487X/FarmInsight_DataAndReport/' + windfilepath
#
#         # ——此行准备添加机型选择——20180425———— #
#         # ********************************* #
#         # ————————————————————————————————— #
#
#         # 调用powerNestAEP函数
#         # context = powerNestAEP.powernestAEP(windfilepath, projectname, projectinfo, protitlename, reportauthor,
#         # outputfile)
#         context = powerNestAEP_noReport.powernestAEP(windfilepath, protitlename, project_name, author_name,
#                                                      yawerror_choose, power_choose, kopt_choose)
#         if windfilepath is not None:
#             return render(request, 'powernestAEP/power_nest_AEP_result.html', context)
#         else:
#             return HttpResponseRedirect('/power_nest_AEP/')
#     file_list = PowerNestAEP_upload.objects.all()
#     return render(request, 'powernestAEP/power_nest_AEP.html', {'file_list': file_list})
#
#
# @login_required  # 能巢方案计算结果
# def power_nest_AEP_result(request):
#     return render(request, 'powernestAEP/power_nest_AEP_result.html')
#
#
# @login_required  # 能巢方案报告下载
# def power_nest_AEP_download(request):
#     from django.http import FileResponse
#     from farmInsightPro.powernestaepAlgorithm import powerNestAEP_noReport
#     the_path = powerNestAEP_noReport.get_aep_path()
#     the_file = open(the_path, 'rb')
#     the_name = the_path.lstrip(r'//1002DZ050487X/FarmInsight_DataAndReport/power_nest_AEP/power_nest_AEP_report/')
#     response = FileResponse(the_file)
#     # print the_name
#     response['Content-Type'] = 'application/octet-stream'
#     response['Content-Disposition'] = 'attachment;filename="' + the_name.encode("utf-8") + '"'
#
#     return response


# 2018.6.20
@login_required
# 厂商功率曲线汇总-2MW
def power_line_2mw(request):
    """
    厂商功率曲线汇总视图（2MW），读取并展示功率、推力及功率系数数据。

    :param request: Django 请求对象
    :return: 功率曲线汇总页面
    """

    # request.POST
    # request.GET

    power = []
    ct = []
    cp = []

    path1 = r'\\1002DZ050487X\FarmInsight_DataAndReport\power_curve_look\power_curve_look_data\turbine_info_2mw.xlsx'
    work = xlrd.open_workbook(path1)

    sheet_power = work.sheet_by_name("power")
    sheet_ct = work.sheet_by_name("ct")
    sheet_cp = work.sheet_by_name("cp")

    for rownum in range(0, sheet_power.nrows):
        rowvalue = sheet_power.row_values(rownum)
        power.append(rowvalue)

    for rownum in range(0, sheet_ct.nrows):
        rowvalue = sheet_ct.row_values(rownum)
        ct.append(rowvalue)

    for rownum in range(0, sheet_power.nrows):
        rowvalue = sheet_cp.row_values(rownum)
        cp.append(rowvalue)

    return render(request, 'PowerLine/power_line_2mw.html',
                  {'power': json.dumps(power), 'ct': json.dumps(ct), 'cp': json.dumps(cp)})


@login_required
# 厂商功率曲线汇总-3MW
def power_line_3mw(request):
    """
    厂商功率曲线汇总视图（3MW），读取并展示功率、推力及功率系数数据。

    :param request: Django 请求对象
    :return: 功率曲线汇总页面
    """

    # request.POST
    # request.GET

    power = []
    ct = []
    cp = []

    path1 = r'//1002DZ050487X/FarmInsight_DataAndReport/power_curve_look/power_curve_look_data/turbine_info_3mw.xlsx'
    work = xlrd.open_workbook(path1)

    sheet_power = work.sheet_by_name("power")
    sheet_ct = work.sheet_by_name("ct")
    sheet_cp = work.sheet_by_name("cp")

    for rownum in range(0, sheet_power.nrows):
        rowvalue = sheet_power.row_values(rownum)
        power.append(rowvalue)

    for rownum in range(0, sheet_ct.nrows):
        rowvalue = sheet_ct.row_values(rownum)
        ct.append(rowvalue)

    for rownum in range(0, sheet_power.nrows):
        rowvalue = sheet_cp.row_values(rownum)
        cp.append(rowvalue)

    return render(request, 'PowerLine/power_line_3mw.html',
                  {'power': json.dumps(power), 'ct': json.dumps(ct), 'cp': json.dumps(cp)})


@login_required
# 厂商功率曲线汇总-6MW
def power_line_6mw(request):
    """
    厂商功率曲线汇总视图（6MW），读取并展示功率、推力及功率系数数据。

    :param request: Django 请求对象
    :return: 功率曲线汇总页面
    """

    # request.POST
    # request.GET

    power = []
    ct = []
    cp = []

    path1 = r'//1002DZ050487X/FarmInsight_DataAndReport/power_curve_look/power_curve_look_data/turbine_info_6mw.xlsx'
    work = xlrd.open_workbook(path1)

    sheet_power = work.sheet_by_name("power")
    sheet_ct = work.sheet_by_name("ct")
    sheet_cp = work.sheet_by_name("cp")

    for rownum in range(0, sheet_power.nrows):
        rowvalue = sheet_power.row_values(rownum)
        power.append(rowvalue)

    for rownum in range(0, sheet_ct.nrows):
        rowvalue = sheet_ct.row_values(rownum)
        ct.append(rowvalue)

    for rownum in range(0, sheet_power.nrows):
        rowvalue = sheet_cp.row_values(rownum)
        cp.append(rowvalue)

    return render(request, 'PowerLine/power_line_6mw.html',
                  {'power': json.dumps(power), 'ct': json.dumps(ct), 'cp': json.dumps(cp)})


# ————————————————————————————————————————————————— #


# ——————————————以下是定制化报告(新版风参)—————————————————— #
@login_required  # 定制化报告上传(新版风参)
def auto_report_upload(request):
    """
    定制化报告文件上传视图（新版风参），处理报告相关文件的上传。

    :param request: Django 请求对象
    :return: 上传页面及文件列表
    """

    from models import WindCheck_upload_newIEC
    if request.method == 'POST':
        files = request.FILES.getlist("files")
        for f in files:
            file_model = WindCheck_upload_newIEC()
            file_model.file_field = f
            file_model.save()
    else:
        my_form = forms.windcheck_upload_newIEC()
    WindCheck_upload_newIEC.objects.order_by("file_time")  # 按时间排序
    file_list = WindCheck_upload_newIEC.objects.all()
    return render(request, 'autoreport/auto_report_upload.html',
                  {'file_list': file_list})


@login_required  # 定制化报告(新版风参)
def auto_report(request):
    """
    定制化报告视图（新版风参），调用算法生成定制化控制策略报告。

    :param request: Django 请求对象
    :return: 报告结果页面或报告页面
    """

    from models import WindCheck_upload_newIEC
    from farmInsightPro.auto_report import autoreport
    if request.method == 'POST':
        wcwindfilepath1 = request.POST.get("wcwindfilepath", None)
        windturchose1 = request.POST['windturchose1']  # 选取下拉菜单值
        windturchose2 = request.POST['windturchose2']  # 选取下拉菜单值
        project_name = request.POST.get("projectname", None)
        author_name = request.POST.get("authorname", None)
        wcwindfilepath = r'//1002DZ050487X/FarmInsight_DataAndReport/' + wcwindfilepath1
        figurefilepath = wcwindfilepath1.lstrip(u'wind_check_newIEC/wind_check_newIEC_data/')  # 数据图像保存的路径
        # 调用windcheck函数
        context = autoreport.Auto_Report(wcwindfilepath, figurefilepath, windturchose1, windturchose2, project_name,
                                         author_name)
        context["wcwindfilepath"] = wcwindfilepath1
        global the_path
        the_path = context["save_name"]
        # fi = {"wcwindfilepath": wcwindfilepath}
        template_path = r'//1002DZ050487X/FarmInsight_DataAndReport/auto_report/report_templates/XXX项目定制化控制策略报告模板.docx'
        picture_path = r'//1002DZ050487X/FarmInsight_DataAndReport/auto_report/data_figure/' + figurefilepath
        if wcwindfilepath is not None:
            return render(request, 'autoreport/auto_report_result.html', context)
            # return HttpResponse("OK!")
        else:
            return HttpResponseRedirect('/auto_report/')

    def get_path():
        """
        获取报告保存路径。

        :return: 报告文件保存路径
        """
        return context["save_name"]

    file_list = WindCheck_upload_newIEC.objects.all()
    return render(request, 'autoreport/auto_report.html', {'file_list': file_list})


@login_required  # 定制化报告结果(新版风参)
def auto_report_result(request):
    """
    定制化报告结果视图（新版风参）。

    :param request: Django 请求对象
    :return: 报告结果模板
    """

    return render(request, 'autoreport/auto_report_result.html')


@login_required  # 定制化报告下载(新版风参)
def auto_report_download(request):
    """
    定制化报告下载视图（新版风参），返回生成的报告文件。

    :param request: Django 请求对象
    :return: 文件下载响应
    """

    from django.http import FileResponse
    from farmInsightPro.auto_report import autoreport
    the_path = autoreport.get_path()
    the_file = open(the_path, 'rb')
    the_name = the_path.lstrip(r'//1002DZ050487X/FarmInsight_DataAndReport/auto_report/reports/')
    response = FileResponse(the_file)
    # print the_name
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="' + the_name.encode("utf-8") + '"'

    return response


# ————————————————————————————————————————————— #



@login_required
def layouts(request):
    """
    布局页面视图。

    :param request: Django 请求对象
    :return: 布局模板
    """

    return render(request, 'layouts.html')


@login_required
def search_results(request):
    """
    搜索结果页面视图。

    :param request: Django 请求对象
    :return: 搜索结果模板
    """

    return render(request, 'search_results.html')


def login_error(request):
    """
    登录错误页面视图。

    :param request: Django 请求对象
    :return: 登录错误模板
    """

    return render(request, 'login_error.html')

######################
# 定版塔架归档与推荐

# towerfit数据上传
@login_required
def tower_fit_upload2(request):
    """
    定版塔架归档数据上传视图，处理塔架相关文件的上传。

    :param request: Django 请求对象
    :return: 上传页面及文件列表
    """

    from models import TowerFit_upload2
    if request.method == "POST":
        file_list = request.FILES.getlist("files")
        for f in file_list:
            file_model = TowerFit_upload2()
            file_model.file_field = f
            file_model.save()
    else:
        my_form = forms.towerfit_upload2()
    TowerFit_upload2.objects.order_by("file_time")
    file_list = TowerFit_upload2.objects.all()
    return render(request, 'towerfit2/towerfit_info_update2/tower_fit_upload2.html', {"file_list": file_list})


# towerfit数据库更新
@login_required
def tower_fit_update2(request):
    """
    定版塔架归档数据库更新视图，将塔架参数写入 Excel 数据库及 MySQL 数据库。

    :param request: Django 请求对象
    :return: 更新结果页面或更新页面
    """

    from farmInsightPro.towerfitAlgorithm2 import towerfit_update2
    from models import TowerFit_upload2
    import MySQLdb
    database = r'\\1002DZ050487X\FarmInsight_DataAndReport\controller_fit2\controller_fit_database\Controller_Fit_Projects.xlsx'
    if request.method == "POST":
        date = request.POST.get("date")
        turbineType = request.POST.get("turbineType")
        towerType = request.POST.get("towerType")

        project_name = request.POST.get("project_name")
        tower_ID = request.POST.get("tower_ID")
        towerWeight = request.POST.get("towerWeight")
        towerDiameter = request.POST.get("towerDiameter")
        towerFreq = request.POST.get("towerFreq")

        tower_section_number = request.POST.get("tower_section_number")
        rotational_stiffness = request.POST.get("rotational_stiffness")

        wind_speed_band = request.POST.get("wind_speed_band")
        turbulence_m1_band = request.POST.get("turbulence_m1_band")
        turbulence_m10_band = request.POST.get("turbulence_m10_band")
        turbulence_mETM_band = request.POST.get("turbulence_mETM_band")

        density = request.POST.get("density")
        Vave = request.POST.get("Vave")
        Weibull_A = request.POST.get("Weibull_A")
        Weibull_K = request.POST.get("Weibull_K")
        Ieff15_m1 = request.POST.get("Ieff15_m1")
        Ieff15_m10 = request.POST.get("Ieff15_m10")
        wind_shear = request.POST.get("wind_shear")
        inflow_angle = request.POST.get("inflow_angle")
        V50 = request.POST.get("V50")

        foundation_type=request.POST.get("foundation_type")
        bladeType = request.POST.get("bladeType")
        substation_location = request.POST.get("substation_location")

        project_author = request.POST.get("projectauthor")
        remark = request.POST.get("remark")
        foundation_report_PLM_id = request.POST.get("foundation_report_PLM_id")
        foundation_report_name = request.POST.get("foundation_report_name")
        EL_Mxy_SF = request.POST.get("EL_Mxy_SF")
        EL_Mxy_NSF = request.POST.get("EL_Mxy_NSF")
        m4_FL_My = request.POST.get("m4_FL_My")
        platform = request.POST.get("platform")




        db = MySQLdb.connect("localhost", "root", "xuxinwei811@", "farm_insight", charset='utf8')
        cursor = db.cursor()
        sql = """INSERT INTO 定版塔架数据库(作者,塔架编号,机组名称,叶片名称,塔架类型,塔架重量,注释,风速带,m为1湍流带,m为10湍流带,m为ETM湍流带,空气密度,年平均风速,威布尔分布A值,威布尔分布K值,m为1湍流强度_I15,m为10湍流强度_I15,风剪切,入流角,V50,塔架频率,塔架截面数,基础类型,塔架直径,箱变位置,扭转刚度,项目名称,基础载荷报告编号,基础载荷报告名称,归档日期,带安全系数塔底极限载荷Mxy,不带安全系数极限载荷Mxy,m为4等效疲劳载荷My,机组平台)
                  VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")""" %\
                  (project_author,tower_ID,turbineType,bladeType,towerType,towerWeight,remark,wind_speed_band,turbulence_m1_band,turbulence_m10_band,turbulence_mETM_band,density,Vave,Weibull_A,Weibull_K,Ieff15_m1,Ieff15_m10,wind_shear,inflow_angle,V50,towerFreq,tower_section_number,foundation_type,towerDiameter,substation_location,rotational_stiffness,project_name,foundation_report_PLM_id,foundation_report_name,date,EL_Mxy_SF,EL_Mxy_NSF,m4_FL_My,platform)

        # sql = """INSERT INTO tower_database(作者,塔架编号,机组名称,叶片名称,塔架类型,塔架重量,注释,风速带,m为1湍流带,m为10湍流带,m为ETM湍流带,空气密度,年平均风速,威布尔分布A值,威布尔分布K值,m为1湍流强度_I15,m为10湍流强度_I15,风剪切,入流角,V50,塔架频率,塔架截面数,基础类型,塔架直径,箱变位置,扭转刚度,项目名称,基础载荷报告编号,基础载荷报告名称,归档日期)
        #           VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")""" %\
        #           (project_author,tower_ID,turbineType,bladeType,towerType,towerWeight,remark,wind_speed_band,turbulence_m1_band,turbulence_m10_band,turbulence_mETM_band,density,Vave,Weibull_A,Weibull_K,Ieff15_m1,Ieff15_m10,wind_shear,inflow_angle,V50,towerFreq,tower_section_number,foundation_type,towerDiameter,substation_location,rotational_stiffness,project_name,foundation_report_PLM_id,foundation_report_name,date)
        # # try:
        # # 执行sql语句
        cursor.execute(sql)
        # # 提交到数据库执行
        db.commit()






        towerfit_update2.writeValue( date=date, turbineType=turbineType, towerType=towerType, tower_ID=tower_ID, towerDiameter=towerDiameter, towerWeight=towerWeight,towerFreq=towerFreq,
                                    tower_section_number=tower_section_number,rotational_stiffness=rotational_stiffness,density=density,Vave=Vave,Weibull_A=Weibull_A,
                                    Weibull_K=Weibull_K,Ieff15_m1=Ieff15_m1,Ieff15_m10=Ieff15_m10,wind_shear=wind_shear,inflow_angle=inflow_angle,V50=V50,
                                    foundation_type=foundation_type, bladeType=bladeType, substation_location=substation_location,
                                    project_name=project_name,
                                   project_author=project_author, remark=remark,
                                     wind_speed_band=wind_speed_band,turbulence_m1_band=turbulence_m1_band,turbulence_m10_band=turbulence_m10_band,turbulence_mETM_band=turbulence_mETM_band,
                                     foundation_report_PLM_id=foundation_report_PLM_id,foundation_report_name=foundation_report_name)
        return render(request, 'towerfit2/towerfit_info_update2/tower_fit_update_result2.html')
    TowerFit_upload2.objects.order_by("file_time")
    file_list = TowerFit_upload2.objects.all()
    context = towerfit_update2.get_options(database)
    context["file_list"] = file_list
    return render(request, 'towerfit2/towerfit_info_update2/tower_fit_update2.html', context)


# towerfit数据库更新结果
@login_required
def tower_fit_update_result2(request):
    """
    定版塔架归档数据库更新结果视图。

    :param request: Django 请求对象
    :return: 更新结果模板
    """

    return render(request, 'towerfit2/towerfit_info_update2/tower_fit_update_result2.html')


# towerfit数据库下载
@login_required
def tower_database_download2(request):
    """
    定版塔架归档数据库下载视图，返回数据库 Excel 文件。

    :param request: Django 请求对象
    :return: 文件下载响应
    """
    from django.http import StreamingHttpResponse
    def file_iterator(file_name, chunk_size=512):
        """
        文件迭代器，按块读取文件内容用于流式下载。

        :param file_name: 文件路径
        :type file_name: str
        :param chunk_size: 每次读取的字节数，默认 512
        :type chunk_size: int
        :return: 文件内容块生成器
        """
        with open(file_name, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    the_file_name = "//1002DZ050487X/FarmInsight_DataAndReport/controller_fit2/controller_fit_database/Controller_Fit_Projects.xlsx"
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/vnd.ms-excel'
    response['Content-Disposition'] = 'attachment;filename=" 定制化模板.xlsx"'
    return response


# towerfit分析
@login_required
def tower_fit_analysis2(request):
    """
    定版塔架归档分析视图，根据条件查询并比对塔架数据库。

    :param request: Django 请求对象
    :return: 分析结果页面或分析页面
    """

    from models import TowerFit_upload2
    from farmInsightPro.towerfitAlgorithm2 import towerfit_calculation_new2
    # 数据库路径，固定值
    database = r'\\1002DZ050487X\FarmInsight_DataAndReport\controller_fit2\controller_fit_database\Controller_Fit_Projects.xlsx'
    if request.method == "POST":
        windfile1 = request.POST["wcwindfilepath"]
        turbine_type = request.POST["turbine_type"]
        tower_type = request.POST["tower_type"]
        tower_id = request.POST["tower_id"]
        blade_type = request.POST["blade_type"]
        project_name = request.POST["project_name"]
        item_to_show = request.POST["item_to_show"]
        if item_to_show == '':
            item_to_show = 0
        else:
            item_to_show = int(item_to_show)
        windfile = r'//1002DZ050487X/FarmInsight_DataAndReport/' + windfile1
        context = towerfit_calculation_new2.compareValue2(item_to_show, database, windfile, project_name, turbine_type,
                                                         tower_type, tower_id, blade_type)
        # the_name = context["the_name"]
        # the_num = context["the_num"]
        context["project_name"] = project_name
        context["turbine_type"] = turbine_type
        context["tower_type"] = tower_type
        context["tower_id"] = tower_id
        context["blade_type"] = blade_type
        context["wcwindfilepath"] = windfile1
        the_list = context["info"]
        # 若搜索无结果
        if len(the_list) == 0:
            # the_list = 0
            context["info"] = 0
        # suggest = context["suggest"]
        return render(request, 'towerfit2/towerfit_analysis2/tower_fit_result2.html', context)

    TowerFit_upload2.objects.order_by("file_time")
    file_list = TowerFit_upload2.objects.all()
    context = towerfit_calculation_new2.get_options(database)
    context["file_list"] = file_list
    return render(request, 'towerfit2/towerfit_analysis2/tower_fit_analysis2.html', context)


# towerfit分析结果
@login_required
def tower_fit_result2(request):
    """
    定版塔架归档分析结果视图。

    :param request: Django 请求对象
    :return: 分析结果模板
    """

    return render(request, 'towerfit2/towerfit_analysis2/tower_fit_result2.html')


#定版塔架推荐
# towerfit数据上传
@login_required
def tower_fit_upload3(request):
    """
    定版塔架推荐数据上传视图，处理塔架相关文件的上传。

    :param request: Django 请求对象
    :return: 上传页面及文件列表
    """

    from models import TowerFit_upload3
    if request.method == "POST":
        file_list = request.FILES.getlist("files")
        for f in file_list:
            file_model = TowerFit_upload3()
            file_model.file_field = f
            file_model.save()
    else:
        my_form = forms.towerfit_upload3()
    TowerFit_upload3.objects.order_by("file_time")
    file_list = TowerFit_upload3.objects.all()
    return render(request, 'towerfit3/towerfit_info_update3/tower_fit_upload3.html', {"file_list": file_list})


# towerfit数据库更新
@login_required
def tower_fit_update3(request):
    """
    定版塔架推荐数据库更新视图，根据风参条件推荐合适的塔架方案。

    :param request: Django 请求对象
    :return: 推荐结果页面或更新页面
    """

    from farmInsightPro.towerfitAlgorithm3 import towerfit_update3
    from models import TowerFit_upload3
    database = r'\\1002DZ050487X\FarmInsight_DataAndReport\controller_fit2\controller_fit_database\Controller_Fit_Projects.xlsx'

    if request.method == "POST":
        turbineType = request.POST.get("turbine_type")
        tower_section_number = request.POST.get("tower_section_number")
        foundation_type=request.POST.get("foundation_type")
        hub_height = request.POST.get("hub_height")
        windfile1 = request.POST["wcwindfilepath"]
        windfile1 = request.POST["wcwindfilepath"]
        windfile = r'//1002DZ050487X/FarmInsight_DataAndReport/' + windfile1
        tower_dict=towerfit_update3.choose_tower(windpara_file=windfile,input_model=turbineType,input_tower_height=hub_height,
                                      input_tower_base=foundation_type,input_tower_segment=tower_section_number)

        return render(request, 'towerfit3/towerfit_info_update3/tower_fit_update_result3.html',tower_dict)
    TowerFit_upload3.objects.order_by("file_time")
    file_list = TowerFit_upload3.objects.all()
    context = towerfit_update3.get_options(database)
    context["file_list"] = file_list
    return render(request, 'towerfit3/towerfit_info_update3/tower_fit_update3.html', context)


# towerfit数据库更新结果
@login_required
def tower_fit_update_result3(request):
    """
    定版塔架推荐数据库更新结果视图。

    :param request: Django 请求对象
    :return: 更新结果模板
    """

    return render(request, 'towerfit3/towerfit_info_update3/tower_fit_update_result3.html')


# towerfit数据库下载
@login_required
def tower_database_download3(request):
    """
    定版塔架推荐数据库下载视图，返回数据库 Excel 文件。

    :param request: Django 请求对象
    :return: 文件下载响应
    """
    from django.http import StreamingHttpResponse
    def file_iterator(file_name, chunk_size=512):
        """
        文件迭代器，按块读取文件内容用于流式下载。

        :param file_name: 文件路径
        :type file_name: str
        :param chunk_size: 每次读取的字节数，默认 512
        :type chunk_size: int
        :return: 文件内容块生成器
        """
        with open(file_name, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    the_file_name = "//1002DZ050487X/FarmInsight_DataAndReport/controller_fit2/controller_fit_database/Controller_Fit_Projects.xlsx"
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/vnd.ms-excel'
    response['Content-Disposition'] = 'attachment;filename=" 定制化模板.xlsx"'
    return response


# towerfit分析
@login_required
def tower_fit_analysis3(request):
    """
    定版塔架推荐分析视图，根据条件查询并比对塔架数据库。

    :param request: Django 请求对象
    :return: 分析结果页面或分析页面
    """

    from models import TowerFit_upload3
    from farmInsightPro.towerfitAlgorithm3 import towerfit_calculation_new3
    # 数据库路径，固定值
    database = r'\\1002DZ050487X\FarmInsight_DataAndReport\controller_fit2\controller_fit_database\Controller_Fit_Projects.xlsx'
    if request.method == "POST":
        windfile1 = request.POST["wcwindfilepath"]
        turbine_type = request.POST["turbine_type"]
        tower_type = request.POST["tower_type"]
        tower_id = request.POST["tower_id"]
        blade_type = request.POST["blade_type"]
        project_name = request.POST["project_name"]
        item_to_show = request.POST["item_to_show"]
        if item_to_show == '':
            item_to_show = 0
        else:
            item_to_show = int(item_to_show)
        windfile = r'//1002DZ050487X/FarmInsight_DataAndReport/' + windfile1
        context = towerfit_calculation_new3.compareValue2(item_to_show, database, windfile, project_name, turbine_type,
                                                         tower_type, tower_id, blade_type)
        # the_name = context["the_name"]
        # the_num = context["the_num"]
        context["project_name"] = project_name
        context["turbine_type"] = turbine_type
        context["tower_type"] = tower_type
        context["tower_id"] = tower_id
        context["blade_type"] = blade_type
        context["wcwindfilepath"] = windfile1
        the_list = context["info"]
        # 若搜索无结果
        if len(the_list) == 0:
            # the_list = 0
            context["info"] = 0
        # suggest = context["suggest"]
        return render(request, 'towerfit3/towerfit_analysis3/tower_fit_result3.html', context)

    TowerFit_upload3.objects.order_by("file_time")
    file_list = TowerFit_upload3.objects.all()
    context = towerfit_calculation_new3.get_options(database)
    context["file_list"] = file_list
    return render(request, 'towerfit3/towerfit_analysis3/tower_fit_analysis3.html', context)


# towerfit分析结果
@login_required
def tower_fit_result3(request):
    """
    定版塔架推荐分析结果视图。

    :param request: Django 请求对象
    :return: 分析结果模板
    """

    return render(request, 'towerfit3/towerfit_analysis3/tower_fit_result3.html')
