#! /usr/bin/env python

import fire
import json
from ruamel import yaml
import pandas as pd
from csv2yml import flowlist


def sparsify(lst):
    """对列表进行稀疏化：保留首尾各 3 个元素，中间按间隔取样。

    :param lst: 输入列表
    :return: 稀疏化后的列表
    """
    l = len(lst)
    return lst[:3] + lst[3 : -3 : round(l / 10)] + lst[-3:]


def spfl(arr):
    """将数组稀疏化后转换为 ruamel.yaml 流式样式序列。

    :param arr: 输入数组
    :return: ruamel.yaml 流式序列对象
    """
    return flowlist(sparsify(arr.tolist()))


def j2y(
    jsonfile="V6A_Loop02.1_20220126_MulMem.$PJ.json",
    yml="s123_v6.yml",
    out="__temp.yml",
    oname="__temp",
):
    """将 JSON 格式的叶片截面数据转换为 b3p YAML 输入文件。

    :param jsonfile: 输入 JSON 文件路径
    :param yml: 基础 YAML 模板路径
    :param out: 输出 YAML 文件路径
    :param oname: 工作目录名称
    """
    x = json.load(open(jsonfile, "r"))
    d = pd.DataFrame(x["Blade"]["Sections"])

    d["rr"] = d["Dist_from_root"] / d["Dist_from_root"].max()
    d["rthick"] = d["Thick"] / 1e2

    print(d)

    Y = yaml.YAML()

    inp = Y.load(open(yml, "r"))

    inp["general"]["workdir"] = oname

    inp["planform"]["chord"] = spfl(d[["rr", "Chord"]].values)
    inp["planform"]["twist"] = spfl(d[["rr", "Twist"]].values)
    inp["planform"]["thickness"] = spfl(d[["rr", "rthick"]].values)
    inp["planform"]["z"] = spfl(d[["rr", "Dist_from_root"]].values)
    inp["planform"]["dx"] = spfl(d[["rr", "Pitch_axis_x"]].values)
    inp["planform"]["dy"] = spfl(d[["rr", "Pitch_axis_y"]].values)

    Y.dump(inp, open(out, "w"))


def main():
    """主函数，通过 fire 模块暴露命令行接口。"""
    fire.Fire()


if __name__ == "__main__":
    main()
