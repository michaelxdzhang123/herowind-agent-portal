import vtk
import numpy
from b3p import geom_utils


def equals(v1, v2):
    """判断两个浮点数是否在容差范围内相等。

        参数:
        v1, v2 (float): 两个比较值

        返回:
        bool: 是否相等"""
    tol = 1e-6
    if (v1 - v2) ** 2 < tol:
        return True
    else:
        return False


def mesh_line(pnt1, pnt2, np, id):
    """
        utility to mesh a line, adds a couple of parametric coordinates to aid
        draping

        中文说明:
        对线段进行网格划分，并添加铺覆辅助坐标数组。

        参数:
        pnt1, pnt2 (tuple): 线段两端点
        np (int): 点数
        id (str): 坐标标识

        返回:
        tuple: (点坐标列表, 坐标数组字典)"""
    xyz = []
    tol = 1e-6
    web_height = vtk.vtkGeoMath().DistanceSquared(pnt1, pnt2) ** 0.5

    for i in zip(pnt1, pnt2):
        mm = min(0.3, 0.06 / web_height)
        rel = sorted([0, 1] + list(numpy.linspace(mm, 1.0 - mm, np - 2)))
        ab = [j * (i[1] - i[0]) + i[0] for j in rel]
        xyz.append(numpy.array(ab))

    dst = [i[1:] - i[:-1] for i in xyz]  # distances between points in 3 dimensions
    sl = (dst[0] ** 2 + dst[1] ** 2 + dst[2] ** 2) ** 0.5  # length of the line segments

    pl = [0] + [
        sum(sl[:i]) for i in range(1, len(sl) + 1)
    ]  # path location from the first web point

    ppl = [-i + pl[-1] for i in pl]
    ml = [abs(i - 0.5 * web_height) for i in pl]  # distance from the web centerline

    wh = [web_height for i in ml]

    rad = numpy.mean(xyz[2])
    r = [rad for i in range(np)]

    arrays = {
        "d_te": pl,
        "d_le": ppl,
        "d_le_r": [i / max(ppl) for i in ppl],
        "d_%s_r" % id: [i / max(ml) for i in ml],
        "d_%s" % id: ml,
        "d_along_airfoil": ml,
        "web_height": wh,
        "radius": r,
        "is_web": [1 for i in ppl],
    }

    return list(zip(*xyz)), arrays


class web:
    def __init__(
        self, points, web_root, web_tip, web_name, coordinate, flip_normal=False
    ):
        """初始化腹板对象。

            参数:
            points (list): 腹板定义点列表
            web_root (float): 腹板根部半径
            web_tip (float): 腹板尖部半径
            web_name (str): 腹板名称
            coordinate (str): 坐标标识
            flip_normal (bool): 是否翻转法向"""
        self.points = points
        self.web_root = web_root
        self.web_tip = web_tip
        spl1, spl2 = vtk.vtkSCurveSpline(), vtk.vtkSCurveSpline()
        for i in points:
            spl1.AddPoint(i[0], i[1])
            spl2.AddPoint(i[0], i[2])

        self.splines = (spl1, spl2)
        self.evaluations = {}
        self.name = web_name
        self.coordinate = coordinate
        self.flip_normal = flip_normal

    def average_splits(self):
        """
            routine to define the average of the split position (averaged over
            radius), this is used to calculate the number of points for a shell
            part (which can't be done on the local split positions, since then it
            would vary over R and require the ability to drop and gain element
            strips)

            中文说明:
            计算腹板分割位置的半径平均值，用于确定壳体面片点数。

            返回:
            tuple: 平均分割位置"""
        g = list(zip(*self.points))
        return numpy.mean(g[1]), numpy.mean(g[2])

    def splits(self, r, r_relative):
        """
            a split is a point at which the airfoil section has a set point where
            there needs to be a spline evaluation, this ensures that there is a line
            of nodes on the shell to which the web can be attached (or at least
            lined up)

            中文说明:
            获取指定半径处腹板在截面上的分割点坐标。

            参数:
            r (float): 半径位置
            r_relative (float): 相对半径位置

            返回:
            tuple: 腹板在截面上的两个分割点坐标"""
        out = (0, 0)
        out = (self.splines[0].Evaluate(r), self.splines[1].Evaluate(r))
        # log the evaluations of the web position, so that it can be used later
        # to look up the 3D coordinates, store in mm, so that it can be used as
        # an integer key to look up corresponding web split locations
        self.evaluations[int(round(r * 1e3))] = [out]
        return out

    def _find_top_and_bottom_points(self, mesh):
        """
            loop through the mesh (which represents a shell), when it has been
            constructed to accomodate this web, it will have points on the shell
            where the web starts and ends, this routine finds those points for the
            radius locations where the web is. Note that the length of the web is
            only exact down to the element size
            @mesh shell mesh to find web points in

            中文说明:
            在壳体网格中查找腹板起点和终点的对应节点。

            参数:
            mesh: 壳体网格对象"""

        rad = mesh.GetPointData().GetArray("radius")
        rel_dist = mesh.GetPointData().GetArray("d_rel_dist_from_te")

        for i in range(mesh.GetNumberOfPoints()):
            rm = rad.GetValue(i)
            rmm = int(round(rm * 1e3))
            if self.web_root <= rm <= self.web_tip:
                rd = rel_dist.GetValue(i)
                pnt = mesh.GetPoint(i)
                if equals(rd, self.evaluations[rmm][0][0]) or equals(
                    rd, self.evaluations[rmm][0][1]
                ):
                    self.evaluations[rmm].append(pnt)

    def _create_quad_connectivity(self, n_points, n_total):
        """
            create the connectivity of the points that make up the mesh

            中文说明:
            创建腹板四边形单元的连接关系。

            参数:
            n_points (int): 每行点数
            n_total (int): 总点数"""
        quads = vtk.vtkCellArray()
        for i in range(1, int(n_total / n_points)):
            np = range((i - 1) * n_points, i * n_points)  # previous row point ids
            nc = range(i * n_points, (i + 1) * n_points)  # current row point ids
            for j in range(n_points - 1):
                quads.InsertNextCell(4)
                if not self.flip_normal:
                    quads.InsertCellPoint(np[j])
                    quads.InsertCellPoint(nc[j])
                    quads.InsertCellPoint(nc[(j + 1) % n_points])
                    quads.InsertCellPoint(np[(j + 1) % n_points])
                else:
                    quads.InsertCellPoint(np[(j + 1) % n_points])
                    quads.InsertCellPoint(nc[(j + 1) % n_points])
                    quads.InsertCellPoint(nc[j])
                    quads.InsertCellPoint(np[j])

        self.mesh.SetPolys(quads)

    def _create_points(self, n_cells):
        """
            generate the points needed to build the mesh

            中文说明:
            生成腹板网格所需的所有点及其坐标数组。

            参数:
            n_cells (int): 单元数"""
        ev = self.evaluations
        vp = vtk.vtkPoints()
        mesh = vtk.vtkPolyData()
        added_arrays = {}
        for i in sorted(ev):
            if len(ev[i]) == 3:
                pnts, data = mesh_line(ev[i][1], ev[i][2], n_cells, self.coordinate)
                for pnt in pnts:
                    vp.InsertNextPoint(pnt)
                for j in data:
                    if j not in added_arrays:
                        added_arrays[j] = vtk.vtkFloatArray()
                        added_arrays[j].SetName(j)
                    for k in data[j]:
                        added_arrays[j].InsertNextValue(k)

        mesh.SetPoints(vp)
        for i in added_arrays:
            mesh.GetPointData().AddArray(added_arrays[i])
        self.mesh = mesh

    def write_mesh(self, vtpfile):
        """将腹板网格写入VTP文件。

            参数:
            vtpfile (str): 输出文件名"""
        writer = vtk.vtkXMLPolyDataWriter()
        writer.SetFileName(vtpfile)
        writer.SetInputData(self.mesh)
        writer.Write()
        print("# wrote mesh to %s" % vtpfile)

    def mesh(self, mesh, n_cells=20):
        """
            main interface for meshing a web

            中文说明:
            腹板网格生成的主接口。

            参数:
            mesh: 壳体网格
            n_cells (int): 腹板厚度方向单元数"""
        self._find_top_and_bottom_points(mesh)
        self._create_points(n_cells)
        self._create_quad_connectivity(n_cells, self.mesh.GetNumberOfPoints())
