#! /usr/bin/env python

import os
import numpy as np
import vtk


def load(fl, normalise=False):
    """
        load airfoil

        args:
        fl (str): filename

        kwargs:
        normalise (bool): flag determining whether the airfoil is normalised to
        unit length

        returns:
        [(x,y),...] airfoil point coordinates

        中文说明:
        加载翼型坐标文件。

        参数:
        fl (str): 文件名
        normalise (bool): 是否归一化为单位弦长

        返回:
        list: [(x,y),...] 翼型点坐标列表"""
    d = []
    print("loading airfoil %s" % fl)
    for i in open(fl, "r").readlines():
        try:
            xy = [float(j) for j in i.split()]
            if len(xy) in [2, 3]:
                d.append(xy)
        except:
            pass
    x, y = list(zip(*d))
    if normalise:
        mx = min(x)
        dx = max(x) - min(x)
        print("normalise factor %f" % dx)
        x = [(i - mx) / dx for i in x]
        y = [i / dx for i in y]

    return list(zip(x, y))


def optspace(n_points, base=0.2):
    """
        alternative to linspace for sampling that puts more points near the TE and
        LE of an airfoil

        中文说明:
        生成优化采样点分布，在尾缘和前缘附近更密集。

        参数:
        n_points (int): 点数
        base (float): 基准偏移量

        返回:
        array: 优化后的采样坐标"""
    lep = 0.5
    x = np.linspace(0, 4.0 * np.pi, n_points)
    sp = 1.0 + base - np.cos(x)
    x1 = np.array([sum(sp[:i]) for i in range(len(x))])
    x1 = x1 / max(x1)
    return x1


def interp(x, points):
    """
        Interpolate airfoil points using 3D vtkParametricSpline

        args:

        x : List of points in range [0,1]

        points: List of 3d points [(x,y,z),...] to interpolate through

        中文说明:
        使用3D VTK参数化样条插值翼型点。

        参数:
        x (list): [0,1]范围内的参数坐标
        points (list): 待插值的3D点列表

        返回:
        tuple: (x坐标列表, y坐标列表, z坐标列表)"""
    pnts = vtk.vtkPoints()
    for i in points:
        pnts.InsertNextPoint(i[0], i[1], 0 if len(i) == 2 else i[2])
    spline = vtk.vtkParametricSpline()
    spline.SetPoints(pnts)
    spline.SetLeftConstraint(3)
    spline.SetLeftValue(1.0)
    spline.SetRightConstraint(3)
    spline.SetRightValue(1.0)
    p, du = [0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]
    spline.DerivativesAvailableOn()
    out = []
    for i in x:
        p[0] = i
        u = [0, 0, 0]
        spline.Evaluate(p, u, du)
        out.append(u)
    return list(zip(*out))
