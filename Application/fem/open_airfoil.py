#! /usr/bin/env python

import fire
import os
import pandas as pd
from scipy.interpolate import make_interp_spline
from matplotlib import pyplot as plt
import numpy as np
import pyvista as pv


def quad_open(x, start=0.7, val=1e-3):
    """使用二次函数打开翼型尾缘。

    :param x: 归一化弦向坐标数组
    :param start: 开始打开的位置（默认 0.7）
    :param val: 打开幅值（默认 1e-3）
    :return: 尾缘打开量数组
    """
    idx = np.linspace(0, 1, len(x))
    y = (x > start) * (x - start)
    y /= max(y)
    y *= val * (2 * (idx < 0.5) - 1.0)
    return y


class airfoil_open:
    """打开翼型文件的后缘，保存到新文件并绘制结果。"""

    def open(self, airfoil_name, output="__temp.dat", open_height=3e-3):
        """打开翼型文件的后缘。

        :param airfoil_name: 输入翼型文件路径
        :param output: 输出文件路径（默认 __temp.dat）
        :param open_height: 后缘打开高度（默认 3e-3）
        """
        t = pd.read_csv(airfoil_name, sep="\s+", names=["x", "y"])
        y1 = quad_open(t.x, start=0.7, val=open_height)
        fig, ax = plt.subplots(1, 1, figsize=(20, 20))
        ax.plot(t.x, y1, "o")
        ax.plot(t.x, t.y, ".")
        ax.plot(t.x, t.y + y1, ".")
        t.y += y1
        t.to_csv(output, sep="\t", index=False, header=False)
        print(f"written to {output}")
        fig.savefig(output.replace(".dat", ".png"))


if __name__ == "__main__":
    fire.Fire(airfoil_open)
