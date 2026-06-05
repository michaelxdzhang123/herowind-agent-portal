#! /usr/bin/env python3

import argparse
import numpy as np
import yaml
import os
from itertools import chain, zip_longest
import pickle
import json
import shutil
from numpy import array


def plyify(r, t, ply_thickness, reverse=False):
    """Fill thickness distribution using plies.

        中文说明:
        用铺层填充厚度分布，将连续厚度离散化为铺层段。

        参数:
        r (list): 半径位置列表
        t (list): 厚度列表
        ply_thickness (float): 单层厚度
        reverse (bool): 是否反转铺层顺序

        返回:
        list: 铺层段列表 [半径起点, 半径终点]"""
    active = []
    done = []
    np = len(r)
    for i in range(np):
        while t[i] > len(active) * ply_thickness:
            active.append([r[i], -1])
        while t[i] <= (len(active) - 1) * ply_thickness:
            pop = active.pop()
            pop[-1] = r[i]
            done.append(pop)
    for j in active:
        j[-1] = r[i]
        done.append(j)
    for i in done:
        i[0] = round(i[0] * 1e3, -1) * 1e-3
        i[1] = round(i[1] * 1e3, -1) * 1e-3
    # reverse the stack so that longest plies get the lowest ply numbers
    if reverse:
        return done
    else:
        return [i for i in reversed(done)]


def ply_stack(r, t, t_ply=1.0, reverse=False, subdivisions=5000, material=11):
    """
        Taking in a r,t thickness over radius distribution, split it up in
        plies, note that it rounds down in thickness (if the last ply does not fit
        in the thickness it does not go on), so if you have thick plies,
        make sure that the mm thickness is slightly up from a whole number of plies.

        中文说明:
        将厚度分布拆分为离散铺层（适用于层合板）或块（适用于芯材）。

        参数:
        r (list): 半径位置
        t (list): 厚度值
        t_ply (float): 单层厚度
        reverse (bool): 是否反转
        subdivisions (int): 细分数量
        material (int): 材料编号

        返回:
        list: 铺层栈列表，每项为 [材料, 厚度, 起点, 终点]"""
    x = np.linspace(min(r), max(r), subdivisions)
    y = np.interp(x, list(r), t)
    st = plyify(x, y, t_ply, reverse)
    return [[material, t_ply] + i for i in st]


def coreblock(r, t, subdivisions=200, material=11):
    """Make a thickness distribution into a block divisions.

        中文说明:
        将厚度分布转换为块分段（适用于芯材）。

        参数:
        r (list): 半径位置
        t (list): 厚度值
        subdivisions (int): 细分数量
        material (int): 材料编号

        返回:
        list: 块栈列表"""
    assert len(r) == len(t)
    lr = len(r)
    x = np.array(sorted(list(np.linspace(min(r), max(r), int(subdivisions))) + list(r)))
    y = np.interp(0.5 * (x[:-1] + x[1:]), list(r), t)

    stack = []
    for i in range(lr - 1):
        rmin, rmax = r[i], r[i + 1]
        tmin, tmax = t[i], t[i + 1]
        if tmin == tmax:
            tt = tmin
        else:  # TODO this assumes only short rampups of core in the spanwise direction
            tt = 0.5 * (tmin + tmax)

        if tt > 0:
            stack.append([material, tt, rmin, rmax])

    return stack


def number_stack(stack, splitstack, key, increment):
    """Create ply numbering for the plies in the stack, depends on the start key and increment as well as the above/below ratio (splitstack).

        中文说明:
        为铺层栈中的铺层创建编号，基于起始键、增量和上下比例。

        参数:
        stack (list): 铺层栈
        splitstack (array): 上下层比例
        key (array): 起始键
        increment (array): 增量

        返回:
        list: 铺层编号序列"""
    sp = np.nan_to_num(splitstack.astype(float))
    if sp.sum() != 1.0:
        exit("sum %s not 1." % splitstack)

    ky = np.nan_to_num(key.astype(float)).astype(int)
    inc = np.nan_to_num(increment.astype(float), nan=1).astype(int)

    ss = (len(stack) * sp).round().astype(int)
    st, sb = np.array(range(ss[0])), np.array(range(ss[1]))
    stt = ky[0] + st * inc[0]
    sbt = ky[1] + sb * inc[1]
    seq = [i for i in chain.from_iterable(zip_longest(stt, sbt)) if i is not None]

    return seq


def get_coverage(slab, datums, rr):
    """获取铺层的弦向覆盖范围，支持从datums解析表达式。

        参数:
        slab (dict): 铺层定义字典
        datums (dict): 基准数据字典
        rr (array): 相对半径数组

        返回:
        dict: 覆盖范围字典"""
    assert "cover" in slab
    cov = slab["cover"]
    if type(cov) == str:
        for i in datums:
            if cov.find(i) != -1:
                print(f"DEBUG: datums[{i}]['xy'] = {datums[i]['xy']} (type: {type(datums[i]['xy'])})")
                print(f"DEBUG: datums[{i}]['scalex'] = {datums[i]['scalex']} (type: {type(datums[i]['scalex'])})")
                print(f"DEBUG: datums[{i}]['scaley'] = {datums[i]['scaley']} (type: {type(datums[i]['scaley'])})")
                xy = np.array(datums[i]["xy"], dtype=float)
                scalex = float(datums[i]["scalex"])
                scaley = float(datums[i]["scaley"])
                dst = np.interp(
                    rr, xy[:, 0] / scalex, xy[:, 1] * scaley
                )
                cov = cov.replace(i, "np.array(%s)" % dst.tolist())

        return dict([(i[0], i[1:]) for i in eval(cov)])
    else:
        return cov


def lamplan2plies(blade):
    """将基于slab的层合板计划拆分为铺层（层合板）和块（芯材）。

        参数:
        blade (dict): 叶片配置字典

        返回:
        list: 所有铺层栈的列表"""
    root_radius = blade["planform"]["z"][0][1]

    tip_radius = blade["planform"]["z"][-1][1]

    slabs = blade["laminates"]["slabs"]

    datums = blade["laminates"]["datums"] if "datums" in blade["laminates"] else {}

    allstacks = []

    # use a multiple of lamplan length as radius grid to interpolate geometric variables to
    n_s = round(tip_radius * 4)

    radius = np.linspace(0, tip_radius - root_radius, n_s)
    radius_relative = np.linspace(0, 1, n_s)
    material_map = {}

    for i in slabs:
        name = i

        material = slabs[i]["material"]

        if material not in material_map:
            material_map[material] = len(material_map) + 1

        grid = "lamplan" if "grid" not in slabs[i] else slabs[i]["grid"]

        cover = get_coverage(slabs[i], datums, radius_relative)

        draping = "plies" if "draping" not in slabs[i] else slabs[i]["draping"]
        splitstack = (
            np.array([1, 0])
            if "splitstack" not in slabs[i]
            else np.array(slabs[i]["splitstack"])
        )
        key = (
            np.array([0, 4000]) if "key" not in slabs[i] else np.array(slabs[i]["key"])
        )
        increment = (
            np.array([1, -1])
            if "increment" not in slabs[i]
            else np.array(slabs[i]["increment"])
        )
        scale = (
            tip_radius - root_radius if "rscale" not in slabs[i] else slabs[i]["rscale"]
        )
        ply_thickness = (
            1.0 if "ply_thickness" not in slabs[i] else slabs[i]["ply_thickness"]
        )
        r, t = np.array(slabs[i]["slab"]).T
        r *= scale
        t *= ply_thickness

        if draping == "blocks":
            stack = coreblock(r, t, material=material_map[material])
        elif draping == "plies":
            stack = ply_stack(
                r, t, float(ply_thickness), material=material_map[material]
            )

        # assigns keys to the plies in the stack depending on how the stack is split up
        # what increment the ply keys are stacked with (non-1 increment allowing interleaving of plies)
        stack_numbering = number_stack(stack, splitstack, key, increment)
        allstacks.append(
            {
                "name": name.strip(),
                "grid": grid.strip(),
                "cover": cover,
                "numbering": stack_numbering,
                "stack": stack,
                "r": radius,
            }
        )

    if "materials" in blade:
        mdb = blade["materials"]

        assert (os.path.isfile(mdb), "mdb {mdb} not a file")
        material_map["matdb"] = mdb
        # copy the material db over to the working directory, this means that rerunning
        # a model in a workdir is not affected by changes in the source matdb, this is
        # the desired behaviour
        shutil.copyfile(
            #blade["materials"], os.path.join(blade["general"]["workdir"], os.path.basename(mdb))
            blade["materials"], os.path.join(blade["general"]["workdir"], os.path.basename(mdb))
        )
    else:
        print("no material db defined in blade file")
    matmap = os.path.join(blade["general"]["workdir"], "material_map.json")
    json.dump(material_map, open(matmap, "w"))
    print("written material map to %s" % matmap)
    return allstacks


def main():
    """主函数：将层合板计划拆分并输出到.pck文件供铺覆使用。

        参数:
        通过命令行传入yaml层合板计划文件"""
    parser = argparse.ArgumentParser(
        description="Split up the slab based laminate plan into plies (for laminae) and blocks (for core materials), write to a .pck file for use in draping"
    )
    parser.add_argument("yaml", help="Laminate plan yaml file")
    parser.add_argument("--out", default="__lamplan.pck", help="Output file name")
    args = parser.parse_args()

    blade = yaml.load(open(args.yaml, "r"), Loader=yaml.CLoader)

    allstacks = lamplan2plies(blade)

    of = args.out
    pickle.dump(allstacks, open(of, "wb"))

    print("written plydrape to %s" % of)


if __name__ == "__main__":
    main()
