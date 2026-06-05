#! /usr/bin/env python3
import pyvista as pv
import argparse
import multiprocessing


def conv3d_2d(mesh):
    """将三维网格文件 hack 转换为二维格式（FEniCS/ANBA需要）。

    参数:
        mesh (str): 网格文件路径"""
    "hack to translate a mesh to 2D format, which is what fenics/anba needs"
    x = open(mesh, "r").read()
    nb = x[: x.find("Topology")]
    rest = x[x.find("Topology") :]
    nb = nb.replace("0.0000000e+00\n", "\n")
    nb = nb.replace(' 3"', ' 2"')
    nb = nb.replace("XYZ", "XY")
    open(mesh, "w").write(nb + rest)


def vtp2xdmf(vtp):
    """将VTP截面网格转换为XDMF格式，并转为二维。

        参数:
        vtp (str): VTP输入文件路径"""
    assert vtp.endswith(".vtp")
    mesh = pv.read(vtp)
    tri = mesh.triangulate()  # fenics doesn't do mixed element types
    tri.points[:, 2] = 0
    xd = vtp.replace(".vtp", ".xdmf")
    pv.save_meshio(xd, tri, data_format="XML")
    conv3d_2d(xd)
    print("converted %s to %s" % (vtp, xd))


def main():
    """主函数：批量将截面网格从VTK格式转换为XDMF和二维格式。

        参数:
        通过命令行传入多个.vtp格式截面网格文件"""
    p = argparse.ArgumentParser(
        description="translate section meshes from vtk to XDMF and 2D"
    )
    p.add_argument("sections", nargs="*", help="section meshes in .vtp format")
    args = p.parse_args()
    p = multiprocessing.Pool()
    p.map(vtp2xdmf, args.sections)
    p.close()


if __name__ == "__main__":
    main()
