import os
import pickle
from b3p import (
    build_blade_geometry,
    build_blade_structure,
    build_plybook,
    drape_mesh,
    combine_meshes,
    mesh_2d,
)
import numpy as np
from ruamel import yaml
import copy


# def set_mesh_to_coarse(bladedict):
#     """"""


def set_mesh_to_fine(bladedict):
    """将网格设置为精细模式（当前为空实现）。

    :param bladedict: 叶片参数字典
    """


def build_blade(wdir, inp):
    """根据输入参数构建叶片几何、结构、铺层，并生成二维截面网格。

    :param wdir: 工作目录路径
    :param inp: 叶片输入参数字典
    """
    pref = os.path.join(wdir, inp["general"]["prefix"])
    inp["general"]["workdir"] = wdir
    build_blade_geometry.build_blade_geometry(inp)
    build_blade_structure.build_blade_structure(inp)
    stacks = build_plybook.lamplan2plies(inp)
    meshes = []
    for i in [
        ("_web.vtp", "blade", "_shell1.vtu"),
        ("_w1.vtp", "w1", "_w1.vtu"),
        ("_w2.vtp", "w2", "_w2.vtu"),
    ]:
        drape_mesh.drape_mesh(pref + i[0], stacks, i[1], pref + i[2])
        meshes.append(pref + i[2])

    combine_meshes.combine_meshes(meshes, f"{pref}_joined.vtu")
    mesh_2d.cut_blade_parallel(
        f"{pref}_joined.vtu",
        np.arange(0.1, 100, 5).tolist(),
        if_bondline=False,
        rotz=0.0,
        var=pref + ".var",
    )


if __name__ == "__main__":
    # inp = yaml.round_trip_load(
    #     open("../../../b3p/examples/blade_test_portable.yml", "r")
    # )

    inp = yaml.round_trip_load(open("s123_lam.yml", "r"))

    prefix = "s123_modif"

    for maxchord in enumerate([0.0, 0.2, 0.5, 1.0]):
        for bladelength in enumerate(range(2)):
            sub = copy.deepcopy(inp)
            sub["planform"]["chord"][2][1] += maxchord[1]
            sub["planform"]["z"][1][1] += bladelength[1]
            build_blade(f"{prefix}_{maxchord[0]}_{bladelength[0]}", sub)

    # build_blade("temp_py", input)
#! /usr/bin/env python3

import os
import pickle
from b3p import (
    build_blade_geometry,
    build_blade_structure,
    build_plybook,
    drape_mesh,
    combine_meshes,
    mesh_2d,
)
import numpy as np
from ruamel import yaml
import copy
import argparse

# def set_mesh_to_coarse(bladedict):
#     """"""


def set_mesh_to_fine(bladedict):
    """将网格设置为精细模式（当前为空实现）。

    :param bladedict: 叶片参数字典
    """


def build_blade(wdir, inp):
    """根据输入参数构建叶片几何、结构、铺层，并生成二维截面网格。

    :param wdir: 工作目录路径
    :param inp: 叶片输入参数字典
    """
    pref = os.path.join(wdir, inp["general"]["prefix"])
    inp["general"]["workdir"] = wdir
    build_blade_geometry.build_blade_geometry(inp)
    build_blade_structure.build_blade_structure(inp)
    stacks = build_plybook.lamplan2plies(inp)
    meshes = []
    for i in [
        ("_web.vtp", "blade", "_shell1.vtu"),
        ("_w1.vtp", "w1", "_w1.vtu"),
        ("_w2.vtp", "w2", "_w2.vtu"),
    ]:
        drape_mesh.drape_mesh(pref + i[0], stacks, i[1], pref + i[2])
        meshes.append(pref + i[2])

    combine_meshes.combine_meshes(meshes, f"{pref}_joined.vtu")
    mesh_2d.cut_blade_parallel(
        f"{pref}_joined.vtu",
        np.arange(0.1, 100, 5).tolist(),
        if_bondline=False,
        rotz=0.0,
        var=f"{pref}.var",
    )


if __name__ == "__main__":
    # inp = yaml.round_trip_load(
    #     open("../../../b3p/examples/blade_test_portable.yml", "r")
    # )

    p = argparse.ArgumentParser()
    p.add_argument("--input", help="yml input file", default="s123_lam.yml")
    p.add_argument("--prefix", help="output prefix")
    args = p.parse_args()

    inp = yaml.round_trip_load(open(args.input, "r"))

    prefix = "s123_modif"

    for maxchord in enumerate([0.0, 0.2, 0.5, 1.0]):
        for bladelength in enumerate(range(2)):
            sub = copy.deepcopy(inp)
            sub["planform"]["chord"][2][1] += maxchord[1]
            sub["planform"]["z"][1][1] += bladelength[1]
            build_blade(f"{prefix}_{maxchord[0]}_{bladelength[0]}", sub)

    # build_blade("temp_py", input)
