
import pyvista as pv
import argparse
import json
import os
import numpy as np
import yaml

"""
:author: Wout Ruijter <w@blade3.io>
Compute the mass of each material in the cross section from the mesh and the material database input. 
This is a sanity check to make sure that anba4_solve.py is computing the correct mass of the cross section.

"""


def compute_cross_section_mass(mesh, matmap):
    """计算截面中每种材料的质量。

    :param mesh: 网格文件路径
    :param matmap: 材料映射文件路径
    """
    mesh = pv.read(mesh).compute_cell_sizes()

    mm = json.load(open(matmap, "r"))
    mdb = yaml.load(
        open(os.path.join(os.path.dirname(matmap), mm["matdb"]), "r"),
        Loader=yaml.CLoader,
    )

    mm["-1"] = -1
    invmd = {mm[i]: i for i in mm}
    sum_mass, sum_area = 0.0, 0.0
    for i in np.unique(mesh.cell_data["mat"]):
        mat_area = (mesh.cell_data["mat"] == i) * mesh.cell_data["Area"]
        mass = (mat_area * mdb[invmd[i]]["rho"]).sum()
        print(
            i,
            invmd[i],
            mdb[invmd[i]]["name"],
            mdb[invmd[i]]["rho"],
            f"{mass=:.3f}, {mat_area.sum()=:.3f}",
        )

        sum_mass += mass
        sum_area += mat_area.sum()

    print("Total mass:", sum_mass)
    print("Total area:", sum_area)


def main():
    """主函数。解析命令行参数并调用 compute_cross_section_mass 计算截面质量。"""
    p = argparse.ArgumentParser()
    p.add_argument("mesh", default="temp_b3ps/msec_2000.xdmf", help="mesh")
    args = p.parse_args()

    compute_cross_section_mass(
        args.mesh, os.path.join(os.path.dirname(args.mesh), "material_map.json")
    )


if __name__ == "__main__":
    main()
