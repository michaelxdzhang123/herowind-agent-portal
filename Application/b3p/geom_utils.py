import vtk
import math


def spline_interp(x, y, newx):
    """使用VTK Cardinal样条进行一维插值。

        参数:
        x (list): 原始坐标
        y (list): 原始值
        newx (list): 目标插值坐标

        返回:
        list: 插值结果"""
    spl = vtk.vtkCardinalSpline()
    spl.SetLeftConstraint(2)
    spl.SetRightConstraint(2)
    for i in zip(x, y):
        spl.AddPoint(i[0], i[1])

    newy = []
    for i in newx:
        newy.append(spl.Evaluate(i))

    return newy


def spline_interp_k(x, y, newx):
    """使用VTK Kochanek样条进行一维插值。

        参数:
        x (list): 原始坐标
        y (list): 原始值
        newx (list): 目标插值坐标

        返回:
        list: 插值结果"""
    spl = vtk.vtkKochanekSpline()
    spl.SetLeftConstraint(2)
    spl.SetRightConstraint(2)
    spl.SetDefaultTension(0.0)
    spl.SetDefaultContinuity(0.2)
    for i in zip(x, y):
        spl.AddPoint(i[0], i[1])

    newy = []
    for i in newx:
        newy.append(spl.Evaluate(i))

    return newy


def distance(point1, point2):
    """计算两点之间的欧几里得距离。

        参数:
        point1 (tuple): 第一点坐标
        point2 (tuple): 第二点坐标

        返回:
        float: 两点间距离"""
    return math.sqrt(sum((i[1] - i[0]) ** 2 for i in zip(point1, point2)))
