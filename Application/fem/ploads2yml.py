#! /usr/bin/env python
import argparse
from numpy import array
from ruamel.yaml import YAML
from matplotlib import pyplot as plt


def ylist(arr):
    """将浮点数列表设置为 ruamel.yaml 的流式样式（flow style）。

    :param arr: 浮点数数组或列表
    :return: ruamel.yaml 序列对象
    """
    y = YAML()
    seq = y.seq([j for j in arr.tolist()])
    seq.fa.set_flow_style()
    return seq


def load_pblade_loads(txtfile):
    """加载 pblade 载荷文件并转换为 b3p 格式的字典。

    :param txtfile: pblade 载荷文件路径
    :return: 载荷数据的字典
    """
    loads = eval(open(txtfile, "r").read())
    out_dataset = {}

    for i in loads:
        o = {
            "z": ylist(loads[i][0]),
            "my": ylist(loads[i][2]),
            "mx": ylist(loads[i][3]),
            "twist": ylist(loads[i][1]),
            "apply": {"d_w0": [-0.5, 0.1]},
        }
        out_dataset[i] = o
    return out_dataset


def plot_loads(dct, out="loads.png"):
    """绘制 pblade 载荷文件中的弯矩载荷曲线。

    :param dct: 载荷数据字典
    :param out: 输出图片路径（默认 loads.png）
    """
    fig, ax = plt.subplots(2, 1, figsize=(12, 12))
    for i in dct:
        ax[0].plot(dct[i]["z"], dct[i]["mx"], label=i)
        ax[1].plot(dct[i]["z"], dct[i]["my"])

    ax[0].legend(loc="best")
    ax[0].grid()
    ax[0].set_title("mx")
    ax[1].set_title("my")
    ax[1].grid()
    fig.savefig(out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("txtfile", help="pblade loads file")
    args = parser.parse_args()
    outdb = load_pblade_loads(args.txtfile)

    y = YAML()
    y.dump(outdb, open("__lds.yml", "w"))
