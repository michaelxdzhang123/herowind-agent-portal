
import pyvista as pv
import argparse
from matplotlib import pyplot as plt
import os
import multiprocessing


def plot2d(meshname):
    """读取二维网格文件并生成截图（PNG）。

    :param meshname: 网格文件路径
    """
    # Load the 2D mesh from a file
    mesh = pv.read(meshname)

    # # Plot the mesh
    pl = pv.Plotter(off_screen=True)
    pl.add_mesh(mesh, smooth_shading=True, show_edges=True, color="white")

    pl.view_yx()
    pl.camera.zoom(1.3)
    pl.background_color = "white"
    # pl.view_yx()
    # print(o)
    of = meshname.replace(os.path.splitext(meshname)[-1], ".png")
    pl.screenshot(of)
    print("Written plot to", of)
    # # Save the plot as a PNG image
    # plotter.


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("meshname", nargs="+")
    args = p.parse_args()

    pl = multiprocessing.Pool()
    pl.map(plot2d, args.meshname)
    pl.close()
    pl.join()

    # plot2d(args.meshname)
