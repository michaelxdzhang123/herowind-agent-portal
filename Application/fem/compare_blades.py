import pyvista as pv

from matplotlib import pyplot as plt
import numpy as np


def check_node_locations(mesh1, mesh2):
    """比较两个网格的节点位置。

    :param mesh1: 第一个网格文件路径
    :param mesh2: 第二个网格文件路径
    :return: 节点位置数组、位置差数组、是否匹配标志
    """
    b1 = pv.read(mesh1)
    b2 = pv.read(mesh2)
    print("reading blade1 %s and blade2 %s" % (mesh1, mesh2))
    diff = b1.points - b2.points
    isok = np.abs(diff).sum() < 1e-9
    return b1.points, diff, isok


def plot_diff(p, diff, out="__test.png"):
    """绘制节点位置差异图。

    :param p: 节点位置数组
    :param diff: 节点位置差异数组
    :param out: 输出图片路径（默认 __test.png）
    """

    plt.figure(figsize=(12, 8))
    plt.plot(p[:, 2], diff)
    plt.xlabel("z-location (m)")
    plt.ylabel("difference in coordinates (m)")
    plt.legend(loc="best", labels=["x", "y", "z"])
    plt.savefig(out)


def test_blade_geometry_difference():
    """测试：比较 b3p 与 pblade 的叶片几何网格节点差异。

    :return: 无
    """

    b3blade = "temp_b3ps/test_blade.vtp"
    pbblade = "temp/test_100/S123_sca.vtp"

    p, diff, isok = check_node_locations(b3blade, pbblade)
    plot_diff(p, diff, out="blade_geometry_test.png")

    assert isok
    if isok:
        print("blade node locations match")


def test_blade_structure_difference():
    """测试：比较 b3p 与 pblade 的叶片结构网格节点差异。

    :return: 无
    """
    b3blade = "temp_b3ps/test_blade_web.vtp"
    pbblade = "temp/test_100/S123_web.vtp"
    p, diff, isok = check_node_locations(b3blade, pbblade)
    assert isok
    if isok:
        print("blade node locations match")

    plot_diff(p, diff, out="blade_structure_mesh.png")


def test_blade_structure_difference_w0():
    """测试：比较 b3p 与 pblade 的 w0 腹板结构网格节点差异。"""
    b3blade = "temp_b3ps/test_blade_w0.vtp"
    pbblade = "temp/test_100/S123_w0.vtp"
    p, diff, isok = check_node_locations(b3blade, pbblade)
    assert isok
    if isok:
        print("blade node locations match")

    plot_diff(p, diff, out="blade_w0.png")


def test_blade_structure_difference_w1():
    """测试：比较 b3p 与 pblade 的 w1 腹板结构网格节点差异。"""
    b3blade = "temp_b3ps/test_blade_w1.vtp"
    pbblade = "temp/test_100/S123_w1.vtp"
    p, diff, isok = check_node_locations(b3blade, pbblade)
    assert isok
    if isok:
        print("blade node locations match")

    plot_diff(p, diff, out="blade_w1.png")


def test_blade_structure_difference_w2():
    """测试：比较 b3p 与 pblade 的 w2 腹板结构网格节点差异。"""
    b3blade = "temp_b3ps/test_blade_w2.vtp"
    pbblade = "temp/test_100/S123_w2.vtp"
    p, diff, isok = check_node_locations(b3blade, pbblade)
    assert isok
    if isok:
        print("blade node locations match")

    plot_diff(p, diff, out="blade_w2.png")


def test_blade_structure_difference_w3():
    """测试：比较 b3p 与 pblade 的 w3 腹板结构网格节点差异。"""
    b3blade = "temp_b3ps/test_blade_w3.vtp"
    pbblade = "temp/test_100/S123_w3.vtp"
    p, diff, isok = check_node_locations(b3blade, pbblade)
    assert isok
    if isok:
        print("blade node locations match")

    plot_diff(p, diff, out="blade_w3.png")


def test_blade_structure_difference_w4():
    """测试：比较 b3p 与 pblade 的 w4 腹板结构网格节点差异。"""
    b3blade = "temp_b3p/test_blade_w4.vtp"
    pbblade = "temp/test_100/S123_w4.vtp"
    p, diff, isok = check_node_locations(b3blade, pbblade)
    assert isok
    if isok:
        print("blade node locations match")

    plot_diff(p, diff, out="blade_w4.png")


def test_blade_structure_difference_center():
    """测试：比较 b3p 与 pblade 的中心腹板结构网格节点差异。"""
    b3blade = "temp_b3ps/test_blade_center.vtp"
    pbblade = "temp/test_100/S123_center.vtp"
    p, diff, isok = check_node_locations(b3blade, pbblade)
    assert isok
    if isok:
        print("blade node locations match")

    plot_diff(p, diff, out="blade_center.png")


if __name__ == "__main__":
    test_blade_geometry_difference()
