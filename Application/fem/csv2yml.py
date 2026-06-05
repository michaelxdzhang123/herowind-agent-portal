#! /usr/bin/env python

import pandas as pd
import numpy as np
import os
import sys
import copy
from ruamel import yaml
import argparse
from ruamel.yaml import YAML


def condense(lofl):
    """将浮点数列表的列表进行压缩，移除两侧厚度相同的中间点。

    :param lofl: 浮点数列表的列表
    :return: 压缩后的列表的列表
    """
    l = len(lofl)
    out = []
    for i in range(l):
        if i > 0 and i < l - 1:
            t = lofl[i][1]
            tleft = lofl[i - 1][1]
            tright = lofl[i + 1][1]
            # if the thickness is the same as the thicknesses left and right, don't include in output
            if abs(t - tleft) >= 1e-7 or abs(t - tright) >= 1e-7:
                out.append(lofl[i])

        else:
            out.append(lofl[i])
    return out


def flowlist(listoflists):
    """将列表的列表设置为 ruamel.yaml 的流式样式（flow style）。

    :param listoflists: 浮点数列表的列表
    :return: ruamel.yaml 序列对象
    """
    y = YAML(typ='rt')
    y.preserve_quotes = True
    y.indent(mapping=2, sequence=4, offset=2)
    olist = []
    for i in listoflists:
        try:
            seq = y.seq([float(round(j, 8)) for j in i])
            seq.fa.set_flow_style()
            olist.append(seq)
        except Exception:
            continue
    if not olist:
        return y.seq([])
    oseq = y.seq(olist)
    oseq.fa.set_flow_style()
    return oseq


def block(l1, l2, datums):
    """根据 pblade CSV 的两行数据生成 b3p 的 slab 或 datum 字典。

    :param l1: pblade CSV 第一行数据
    :param l2: pblade CSV 第二行数据
    :param datums: 基准点字典
    :return: 类型字符串（slab/datum）、是否可用标志、两个字典对象
    """
    name = l1.iloc[0]

    if type(l1.iloc[1]) == str:
        name, material, mesh, coords, draping, key0, key1, inc1, rscale = l1.iloc[0:9].values

        key2, key3, inc2, ply_thickness = l2.iloc[5:9].values

        sl1 = l1.iloc[9:].values.astype(float)
        sl2 = l2.iloc[9:].values.astype(float)

        sl11 = sl1[~np.isnan(sl1)]
        sl21 = sl2[~np.isnan(sl2)]

        name = name.strip()
        plaincoords = copy.deepcopy(coords)

        for i in datums:
            coords = coords.replace(i, "np.array(%s)" % list(datums[i]))

        try:
            coord_dict = dict([(j[0], j[1:]) for j in eval(coords)])
        except Exception:
            coord_dict = {}

        out = {
            name: {
                "material": material,
                "cover": coord_dict,
                "grid": "shell" if mesh == "blade" else mesh,
                "slab": flowlist(
                    condense(
                        [
                            list(j)
                            for j in zip((sl11 / rscale).tolist(), (sl21).tolist())
                        ]
                    )
                ),
                "ply_thickness": float(ply_thickness),
                "draping": draping,
                "key": [int(key1), int(np.nan_to_num(key3, nan=-1))],
                "splitstack": [float(key0), float(np.nan_to_num(key2, nan=0))],
                "increment": [int(inc1), int(np.nan_to_num(inc2, nan=-1))],
            }
        }

        out2 = copy.deepcopy(out)
        out2[name]["cover"] = str(plaincoords)
        use = True
        try:
            evc = eval(plaincoords)
            out2[name]["cover"] = dict([(j[0], list(j[1:])) for j in evc])
            use = True
        except Exception:
            use = False

        return "slab", use, out, out2
    else:
        name = l1.iloc[0]
        s1, s2 = float(l1.iloc[8]), float(l2.iloc[8])
        x = np.array(list(filter(lambda v: v == v, l1.iloc[9:]))).astype(float)
        y = np.array(list(filter(lambda v: v == v, l2.iloc[9:]))).astype(float)

        out = np.interp(np.linspace(0, 1, 100), x / s1, y / s2)

        out2 = {
            name: {
                "scalex": s1,
                "scaley": s2,
                "xy": flowlist(
                    condense([list(j) for j in zip(x.tolist(), y.tolist())])
                ),
            }
        }

        return "datum", False, {name: out}, out2


def expand_multimaterial(slab):
    """将包含多种材料的 slab 拆分为多个单材料 slab。

    :param slab: 包含多种材料的 slab 字典（pblade 格式）
    :return: 单材料 slab 字典列表
    """
    z, t = [list(i) for i in zip(*slab["slab"])]
    mat = eval(slab["material"])
    y = YAML(typ='rt')
    y.preserve_quotes = True
    y.indent(mapping=2, sequence=4, offset=2)

    split_slabs = []
    for i in zip(mat[::2], mat[1::2]):
        zstart, zend = i[0][1], i[1][1]
        z_ext = np.unique(
            [j for j in (z + [zstart, zend]) if (j >= zstart and j <= zend)]
        )
        thick = np.interp(z_ext, z, t).astype(float)
        cop = copy.deepcopy(slab)
        cop["slab"] = flowlist([[float(j[0]), float(j[1])] for j in zip(z_ext, thick)])
        cop["material"] = str(i[0][0])

        split_slabs.append(cop)

    return split_slabs


if __name__ == "__main__":
    p = argparse.ArgumentParser(
        description="parse a pblade laminate plan and merge in b3p format with a b3p style yaml input file"
    )
    p.add_argument(
        "--csv_input",
        default="lamplan_S123_600_2.csv",
        help="csv input file pblade style",
    )
    p.add_argument(
        "--yaml_template",
        default="s123_geom.yaml",
        help="yaml template to add laminate plan to",
    )
    p.add_argument(
        "--matdb", default="materials_v9.yml", help="material db in yaml format"
    )
    p.add_argument("--output", default="blade_s123_mod.yml")

    args = p.parse_args()

    df = pd.read_csv(os.path.join(sys.path[0], args.csv_input))
    dat, dat2 = {}, {}
    slabs, slabs2 = {}, {}
    for i in range(0, df.shape[0], 2):
        t, use, o, o2 = block(df.loc[i, :], df.loc[i + 1, :], dat)
        if t == "datum":  # type(o) == dict:
            dat.update(o)
            dat2.update(o2)
        elif t == "slab":
            slabs.update(o)
            slabs2.update(o2)
    yaml = YAML(typ='rt')
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)
    with open(args.yaml_template, 'rb') as f:
        yml = yaml.load(f)

    yml["laminates"]["datums"] = dat2

    ss = {}

    for i in slabs2:
        mat = slabs2[i]["material"]
        if not mat.startswith("["):
            sub = slabs2[i]
            ss[i] = sub
        else:
            expanded_slabs = expand_multimaterial(slabs2[i])
            for j in enumerate(expanded_slabs):
                ss[i + f"_{j[0]}"] = j[1]

    yml["laminates"]["slabs"] = ss
    yml["general"]["workdir"] = "temp_b3ps"

    yml["materials"] = args.matdb

    yaml.dump(yml, open(args.output, 'w', encoding='utf-8'))
