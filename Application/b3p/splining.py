import vtk


def intp_k(x, points, const=2, clamp=True, tension=-0.3, bias=0, continuity=0):
    """
        Kochanek spline, wrapping `vtk.vtkKochanekSpline()
        <http://www.vtk.org/doc/nightly/html/classvtkKochanekSpline.html>`_

        args:
        x (list): t coordinate list (in range=[0,1])

        points (list) : coordinate x,y,z points

        const (int): constraint type for left and right of spline

        clamp (bool): flag on whether spline is clamped

        tension (float): tension parameter

        bias (float): bias parameter value

        continuity (int) : continuity parameter value

        returns:
        x : t coordinate list

        o : evaluated coordinate list

        中文说明:
        Kochanek样条插值，包装VTK的vtkKochanekSpline。

        参数:
        x (list): [0,1]范围内的参数坐标
        points (list): 输入坐标点
        const (int): 边界约束类型
        clamp (bool): 是否钳制
        tension (float): 张力参数
        bias (float): 偏置参数
        continuity (float): 连续性参数

        返回:
        tuple: (x, o) 参数坐标和插值结果"""
    sc = vtk.vtkKochanekSpline()
    sc.SetLeftConstraint(const)
    sc.SetRightConstraint(const)
    sc.SetDefaultTension(tension)
    sc.SetDefaultBias(bias)
    sc.SetDefaultContinuity(continuity)
    if clamp:
        sc.ClampValueOn()
    for i in points:
        sc.AddPoint(i[0], i[1])

    o = []
    for i in x:
        o.append(sc.Evaluate(i))
    return x, o


def intp_c(x, points, const=2, clamp=True):
    """
        Cardinal spline, wrapping `vtk.vtkCardinalSpline()
        <http://www.vtk.org/doc/nightly/html/classvtkCardinalSpline.html>`_

        args:
        x (list): t coordinate list (in range=[0,1])

        points (list) : coordinate x,y,z points

        const (int): constraint type for left and right of spline

        clamp (bool): flag on whether spline is clamped

        中文说明:
        Cardinal样条插值，包装VTK的vtkCardinalSpline。

        参数:
        x (list): [0,1]范围内的参数坐标
        points (list): 输入坐标点
        const (int): 边界约束类型
        clamp (bool): 是否钳制

        返回:
        tuple: (x, o) 参数坐标和插值结果"""

    sc = vtk.vtkCardinalSpline()
    sc.SetLeftConstraint(const)
    sc.SetRightConstraint(const)
    if clamp:
        sc.ClampValueOn()
    else:
        sc.ClampValueOff()
    for i in points:
        sc.AddPoint(i[0], i[1])

    o = []
    for i in x:
        o.append(sc.Evaluate(i))
    return x, o


def intp_sc(x, points):
    """
        SCurve spline based interpolation

        args:
        x (list) : t coordinate list

        points (list) : xyz coordinate input points

        returns:
        x (relative coordinate point list)

        o (xyz coordinate points list, resplined)

        中文说明:
        SCurve样条插值，包装VTK的vtkSCurveSpline。

        参数:
        x (list): 参数坐标列表
        points (list): 输入坐标点

        返回:
        tuple: (x, o) 参数坐标和插值结果"""
    sc = vtk.vtkSCurveSpline()
    for i in points:
        sc.AddPoint(i[0], i[1])
    o = []
    for i in x:
        o.append(sc.Evaluate(i))
    return x, o

