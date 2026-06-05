#! /usr/bin/env python3

# import vtk
import argparse
import numpy as np
import pyvista as pv
import time
import multiprocessing


def add_missing_data(inp):
    """为网格添加缺失的点数据和单元数据数组。

        参数:
        inp (tuple): (mesh, pd, cd) 网格、点数据列表、单元数据列表

        返回:
        mesh: 添加数据后的网格"""
    mesh, pd, cd = inp
    for i in pd:
        mesh.point_data.set_array(i[1], i[0])
    for i in cd:
        mesh.cell_data.set_array(i[1], i[0])
    return mesh


def is_nonzero_array(arr):
    # check if there is any nonzero entry in the 1 column (thickness)
    """检查数组第二列是否存在非零项（用于厚度判断）。

        参数:
        arr (array): 输入数组

        返回:
        bool: 是否存在非零厚度"""
    if len(arr.shape) == 2 and arr.shape[1] == 3:
        return np.count_nonzero(arr[:, 1]) > 0
    return True


def main():
    # global meshes
    """主函数：将多个网格（壳体和腹板等）合并为单个VTU文件。

        参数:
        通过命令行传入多个网格文件和输出文件名"""
    p = argparse.ArgumentParser(
        description="Join a series of meshes, i.e. a shell and n web meshes together into a single vtu"
    )
    p.add_argument("meshes", nargs="*")
    p.add_argument("--out", default="__joined_mesh.vtu", help="output file name")
    args = p.parse_args()

    meshes = []
    for i in args.meshes:
        meshes.append(pv.read(i))

    all_pd = [
        (j, x.point_data[j].shape, x.point_data[j].dtype)
        for x in meshes
        for j in x.point_data.keys()
    ]
    all_cd = [
        (j, x.cell_data[j].shape, x.cell_data[j].dtype)
        for x in meshes
        for j in x.cell_data.keys()
        if is_nonzero_array(x.cell_data[j])
    ]

    tic = time.time()

    # for each mesh, find the missing point and cell arrays and create zero arrays
    dist = []
    for m in meshes:
        da = [m, [], []]
        for j in all_pd:
            if j[0] not in m.point_data:
                a = np.zeros((m.n_points, j[1][1] if len(j[1]) > 1 else 1), dtype=j[2])
                da[1].append((j[0], a))
        for j in all_cd:
            if j[0] not in m.cell_data:
                a = np.zeros((m.n_cells, j[1][1] if len(j[1]) > 1 else 1), dtype=j[2])
                da[2].append((j[0], a))
        dist.append(da)

    # add the zero arrays in parallel
    pool = multiprocessing.Pool()
    cmeshes = pool.map(add_missing_data, dist)
    toc = time.time()

    out = cmeshes[0].merge(cmeshes[1:])

    toc2 = time.time()

    print("time adding missing arrays: ", toc - tic, "\ntime merging:", toc2 - toc)

    out.save(args.out)
    print("written mesh to %s" % args.out)


if __name__ == "__main__":
    main()
