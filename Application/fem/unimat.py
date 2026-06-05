#! /usr/bin/env python


import fire
from ruamel import yaml


def unimat(yml_file):
    """将 YAML 文件中所有层合板 slab 的材料统一设置为 "11"，并输出到新文件。

    :param yml_file: 输入的 YAML 文件路径
    """
    y = yaml.YAML()
    dd = y.load(open(yml_file, "r"))
    lams = dd["laminates"]["slabs"]
    for i in lams:
        lams[i]["material"] = "11"
    y.dump(dd, open(yml_file.replace(".yml", "_unimat.yml"), "w"))


def main():
    """主函数，通过 fire 模块暴露 unimat 命令行接口。"""
    fire.Fire(unimat)


if __name__ == "__main__":
    main()
