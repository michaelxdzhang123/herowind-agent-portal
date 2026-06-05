#! /usr/bin/env python

import configparser
#from ruamel import yaml
import argparse
from ruamel.yaml import YAML
from csv2yml import flowlist
import numpy as np
import ploads2yml


def main():
    """主函数。解析命令行参数并调用 cfg2yml 将 pblade 配置文件转换为 b3p yaml 文件。"""
    p = argparse.ArgumentParser()
    p.add_argument(
        "--cfg", default="./data/S123_test_1.cfg", help="config file in pblade format"
    )
    p.add_argument(
        "--baseyaml",
        default="/home/mich/b3p/examples/blade_test.yml",
        help="base yaml file in b3p format",
    )
    p.add_argument(
        "--out", default="./data/s123_geom.yml", help="output yaml file in b3p format"
    )
    args = p.parse_args()
    cfg2yml(args)


def cfg2yml(args):
    """将 pblade 配置文件转换为 b3p yaml 文件，目前翼型数据为硬编码。

    :param args: argparse 参数对象，包含 cfg、baseyaml 和 out 等字段
    """

    keys = ["chord", "thickness", "twist", "dx", "dy"]

    config = configparser.ConfigParser()
    config.read(args.cfg)

    ad = eval(config["mesh"]["added_datums"])

    scl = {
        i: {
            "base": ad[i][0],
            "points": flowlist(np.array(ad[i][1:]).T.tolist()),
        }
        for i in ad
    }
    yaml = YAML(typ='rt')
    with open(args.baseyaml, 'rb') as f:
        ymdoc = yaml.load(f)  # Use load() instead of load_all() for round-trip loader

    for i in ymdoc["planform"]:
        if i in keys:
            dt = eval(config["planform"][i])
            ymdoc["planform"][i] = flowlist(dt)
    ymdoc["planform"]["dy"] = [
        [0.0, 0.0],
        [0.01, 0.0],
        [0.3, 1.2847920485195055],
        [0.43, 1.05612884152284],
        [0.5599999999999999, 0.7372261242530547],
        [0.6900000000000001, 0.5260722687201442],
        [0.8199999999999998, 0.3739086064883998],
        [0.95, 0.22893207266219948],
    ]
    ymdoc["mesh"]["coordinates"] = scl

    ymdoc["mesh"][
        "radii"
    ] = "np.linspace(0,7,20).tolist() + np.linspace(7.4,121, 120).tolist()"

    ymdoc["mesh"]["webs"] = {
        "w0": {
            "origin": [0, -0.3, 0],
            "orientation": [0, 1, 0],
            "z_start": 0,
            "z_follow_blade": 100,
            "z_end": 105,
        },
        "w1": {
            "origin": [0, -0.22, 0],
            "orientation": [0, 1, 0],
            "z_start": 0,
            "z_follow_blade": 100,
            "z_end": 105,
        },
        "center": {
            "origin": [0, 0, 0],
            "orientation": [0, 1, 0],
            "z_start": 0,
            "z_follow_blade": 100,
            "z_end": 105,
        },
        "w2": {
            "origin": [0, 0.22, 0],
            "orientation": [0, 1, 0],
            "z_start": 0,
            "z_follow_blade": 100,
            "z_end": 105,
        },
        "w3": {
            "origin": [0, 0.3, 0],
            "orientation": [0, 1, 0],
            "z_start": 0,
            "z_follow_blade": 100,
            "z_end": 105,
        },
        "w4": {
            "origin": [0, 1.4, 0],
            "orientation": [0, 1, -0.05],
            "z_start": 0,
            "z_follow_blade": 25,
            "z_end": 100,
        },
    }

    """hard code airfoil data for now"""
    #for test = true
    test = True
    if test:
        ymdoc["aero"]["airfoils"] = {
        0.21: "../data/Airfoil/NickBarlow-021.dat",
        0.27: "../data/Airfoil/NickBarlow-027.dat",
        0.36: "../data/Airfoil/NickBarlow-036.dat",
        0.47: "../data /Airfoil/NickBarlow-047.dat",
        0.57: "../data/Airfoil/NickBarlow-057.dat",
        1.00: "../data/Airfoil/NickBarlow-100.dat"
        ,}
        
    else:
        #load from system.cfg and set to here
        ymdoc["aero"]["airfoils"] = eval(config["airfoils"]["airfoils"])
    

    ymdoc["loads"] = ploads2yml.load_pblade_loads(config["structural"]["loads"])
    print(ymdoc["loads"])

    #ploads2yml.plot_loads(ymdoc["loads"])  #commented out for now

    yaml = YAML(typ='rt')
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)
    yaml.dump(ymdoc, open(args.out, 'w', encoding='utf-8'))
    print(f"written yaml with geometry imported to {args.out}")


if __name__ == "__main__":
    main()
