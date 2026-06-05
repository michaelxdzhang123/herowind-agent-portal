#! /usr/bin/env python3

import fire
from ruamel import yaml
import numpy as np
from cfg2yml import flowlist


def coarsen_loads(yml, r=[0, 20, 40, 60, 80, 100]):
    """对载荷数据进行粗化处理，通过插值将原始载荷缩减到指定的半径位置。

    :param yml: 输入的 YAML 文件路径
    :param r: 粗化后的半径列表（默认 [0, 20, 40, 60, 80, 100]）
    """
    # y = yaml.YAML()
    dt = yaml.round_trip_load(open(yml, "rb"))
    loads = dt["loads"]
    coarseloads = {}

    for i in loads:
        z = np.array(loads[i]["z"])
        myn = np.interp(r, z, loads[i]["my"])
        mxn = np.interp(r, z, loads[i]["mx"])
        mtw = np.interp(r, z, loads[i]["twist"])

        coarseloads[i] = {
            "mx": mxn.tolist(),
            "my": myn.tolist(),
            "twist": mtw.tolist(),
            "z": r,
            "apply": loads[i]["apply"],
        }

    dt["loads"] = coarseloads
    dt["general"]["workdir"] += "_coarse"
    out = yml.replace(".yml", "_coarseloads.yml")
    yaml.round_trip_dump(dt, open(out, "w"))
    print(f"** written to {out }")
    # print(coarseloads)


if __name__ == "__main__":
    fire.Fire(coarsen_loads)
