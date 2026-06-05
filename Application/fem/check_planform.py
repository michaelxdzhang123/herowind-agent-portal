import yaml
import sys
import os


def check_planform():
    """检查 geom 文件中的 planform 是否与 lam 文件中的 planform 一致。"""

    x1 = yaml.load(
        open(os.path.join(sys.path[0], "s123_geom.yaml"), "r"), Loader=yaml.FullLoader
    )
    x2 = yaml.load(
        open(os.path.join(sys.path[0], "s123_lam.yml"), "r"), Loader=yaml.FullLoader
    )

    print(x1["planform"] == x2["planform"])
    for i in x1["planform"]:
        print(x1["planform"][i], x2["planform"][i])

    print(x1["mesh"] == x2["mesh"])


if __name__ == """__main__""":
    check_planform()
