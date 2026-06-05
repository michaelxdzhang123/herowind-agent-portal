import vtk
import numpy as np
import math
import os


class section:
    def __init__(self, x, y):
        """初始化二维截面对象。

            参数:
            x (list): x坐标列表
            y (list): y坐标列表"""
        self.x, self.y = x, y
        pnts = vtk.vtkPoints()
        for i in zip(x, y):
            pnts.InsertNextPoint(i[0], i[1], 0.0)
        self.polydata = vtk.vtkPolyData()
        self.polydata.SetPoints(pnts)

        cells = vtk.vtkCellArray()
        for i in range(1, pnts.GetNumberOfPoints()):
            cells.InsertNextCell(2)
            cells.InsertCellPoint(i - 1)
            cells.InsertCellPoint(i)
        self.polydata.SetLines(cells)

    def plot(self, label=""):
        """绘制截面形状（使用全局pl对象）。

            参数:
            label (str): 图例标签"""
        x, y, z = list(
            zip(
                *[
                    self.polydata.GetPoint(i)
                    for i in range(self.polydata.GetNumberOfPoints())
                ]
            )
        )
        pl.plot(x, y, label=label)

    def local_to_global(self):
        """将局部坐标转换为全局坐标（交换x,y）。"""
        pnts = vtk.vtkPoints()
        for i in range(self.polydata.GetNumberOfPoints()):
            pnt = self.polydata.GetPoint(i)
            new_point = (pnt[1], pnt[0], pnt[2])
            pnts.InsertNextPoint(new_point)

        self.polydata.SetPoints(pnts)

    def get_max_thickness(self, web_angle=0, n_points=50):
        """
            get the location (x) where the airfoil is thickest, used to offset the
            section for maximum building height.

            中文说明:
            获取截面最大厚度位置（x坐标），用于偏移优化。

            参数:
            web_angle (float): 腹板角度（度）
            n_points (int): 采样点数

            返回:
            float: 最大厚度对应的x坐标"""
        bounds = self.polydata.GetBounds()
        dx = bounds[1] - bounds[0]
        px = np.linspace(bounds[0] + 0.15 * dx, bounds[1] - 0.4 * dx, n_points)
        plane = vtk.vtkPlane()
        clip = vtk.vtkCutter()

        clip.SetInputData(self.polydata)
        plane.SetNormal(
            np.cos(math.radians(web_angle)), math.sin(math.radians(web_angle)), 0
        )
        t = []
        tb = []
        for i in px:
            plane.SetOrigin(i, 0.5 * (bounds[2] + bounds[3]), 0)
            clip.SetCutFunction(plane)
            clip.Update()
            section = clip.GetOutput()
            top, bot = section.GetPoint(0), section.GetPoint(1)
            t.append(section.GetPoint(0)[1] - section.GetPoint(1)[1])
            tb.append((top, bot))

        return px[t.index(max(t))]

    def scale(self, scalefactor):
        """对截面进行缩放变换。

            参数:
            scalefactor (tuple): 各方向缩放因子"""
        transform = vtk.vtkTransform()
        transform.Scale(scalefactor)
        transformfilter = vtk.vtkTransformFilter()
        transformfilter.SetTransform(transform)
        transformfilter.SetInputData(self.polydata)
        transformfilter.Update()
        self.polydata = transformfilter.GetOutput()

    def twist(self, rz):
        """对截面进行绕Z轴扭转。

            参数:
            rz (float): 扭转角度（度）"""
        transform = vtk.vtkTransform()
        transform.RotateZ(rz)
        transformfilter = vtk.vtkTransformFilter()
        transformfilter.SetTransform(transform)
        transformfilter.SetInputData(self.polydata)
        transformfilter.Update()
        self.polydata = transformfilter.GetOutput()

    def translate(self, dx, dy, dz):
        """对截面进行平移变换。

            参数:
            dx, dy, dz (float): 各方向平移量"""
        transform = vtk.vtkTransform()
        transform.Translate(dx, dy, dz)
        transformfilter = vtk.vtkTransformFilter()
        transformfilter.SetTransform(transform)
        transformfilter.SetInputData(self.polydata)
        transformfilter.Update()
        self.polydata = transformfilter.GetOutput()

    def get_point(self, xy):
        """获取指定xy坐标处最近的点坐标。

            参数:
            xy (tuple): 查询坐标

            返回:
            tuple: 最近点三维坐标"""
        return self.polydata.GetPoint(self.polydata.FindPoint((xy[0], xy[1], 0.0)))

    def get_pointlist(self, z_rotation=0):
        """获取变换后的所有点列表。

            参数:
            z_rotation (float): 绕z轴旋转角度

            返回:
            list: 点坐标列表"""
        transform = vtk.vtkTransform()
        transform.RotateZ(z_rotation)
        transformfilter = vtk.vtkTransformFilter()
        transformfilter.SetTransform(transform)
        transformfilter.SetInputData(self.polydata)
        transformfilter.Update()
        output = transformfilter.GetOutput()
        return [output.GetPoint(i) for i in range(output.GetNumberOfPoints())]

    def to_xfoil(self, fname):
        """将截面坐标导出为XFOIL格式文件。

            参数:
            fname (str): 输出文件名"""
        if not os.path.isdir(os.path.dirname(fname)):
            os.makedirs(os.path.dirname(fname))
        f = open(fname, "w")
        for i in zip(self.x, self.y):
            f.write("%f      %f\n" % (i[0], i[1]))
        f.close()

    def get_te(self):
        """获取尾缘中点坐标和尾缘厚度。

            返回:
            tuple: (尾缘中点坐标, 尾缘厚度)"""
        te1 = self.polydata.GetPoint(0)
        te2 = self.polydata.GetPoint(self.polydata.GetNumberOfPoints() - 1)
        return (
            [0.5 * (i[0] + i[1]) for i in zip(te1, te2)],
            vtk.vtkMath.Distance2BetweenPoints(te1, te2) ** 0.5,
        )
