#! /usr/bin/env python

import fire
from ruamel import yaml
import numpy as np


def multloads(yml, factor, out="__tmp.yml"):
    """将 YAML 文件中的载荷数据按给定倍数进行缩放。

    :param yml: 输入的 YAML 文件路径
    :param factor: 载荷缩放因子
    :param out: 输出 YAML 文件路径（默认 __tmp.yml）
    """
    y = yaml.YAML()
    dt = y.load(open(yml, "r"))
    for i in dt["loads"]:
        for k in ["mx", "my"]:
            dt["loads"][i][k] = (np.array(dt["loads"][i][k]) * factor).tolist()
        print(dt["loads"][i])
    dt["general"]["workdir"] += f"_lm{factor}"
    y.dump(dt, open(out, "w"))

    print(f"""** Wrote {out} with factor {factor} on loads set in {yml}""")


def main():
    """主函数，通过 fire 模块暴露 multloads 命令行接口。"""
    fire.Fire(multloads)


if __name__ == "__main__":
    main()
