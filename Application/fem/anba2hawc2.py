
import argparse
import json
import re
import numpy as np


header = """1  [BLADENAME] 
	r	mass	  cogx	 cogy	trix	riy	strtw	aex	aey	K11		K12		K13		K14		K15		K16		K22		K23		K24		K25		K26		K33		K34		K35		K36		K44		K45		K46		K55		K56		K66 
	[m]	[Kg/m]	  [m] 	 [m] 	[m] 	[m] 	[deg]	[m]	[m]	[N]		[N]		[N]		[Nm]		[Nm]		[Nm]		[N]		[N]		[Nm]		[Nm]		[Nm]		[N]		[Nm]		[Nm]		[Nm]		[Nm^2]		[Nm^2]		[Nm^2]		[Nm^2]		[Nm^2]		[Nm^2]
	#1 
	$1 NSEC"""


def anba2hawc(r, sec):
    """将 ANBA 截面输出字典转换为 HAWC2 截面格式。

    :param r: 半径（单位：mm）
    :param sec: ANBA 截面输出字典，包含质量矩阵、刚度矩阵等
    :return: HAWC2 截面格式的字符串
    """
    r = float(r) * 1e-3
    m = sec["mass_matrix"]
    mass = m[0][0]
    cogx, cogy = sec["mass_center"]
    # https://en.wikipedia.org/wiki/Radius_of_gyration
    rix, riy = np.sqrt(m[3][3] / mass), np.sqrt(m[4][4] / mass)
    strtw = np.degrees(sec["principal_axes_rotation"])
    aex, aey = sec["tension_center"]
    k = []

    # TODO: check this
    dofmap = [1, 0, 2, 4, 3, 5]
    for i in range(6):
        for j in range(i, 6):
            k.append(1e-6 * sec["stiffness"][dofmap[i]][dofmap[j]])

    stl = [r, mass, cogx, cogy, rix, riy, strtw, aex, aey] + k

    out = "\t".join(["{:.5E}".format(i) for i in stl])
    return out


def main():
    """主函数。解析命令行参数，对一组截面运行 anba2hawc，并将结果合并为 HAWC2 .st 文件。"""

    da = """temp_b3ps/msec_10000.xdmf.json  temp_b3ps/msec_2000.xdmf.json   temp_b3ps/msec_40000.xdmf.json  temp_b3ps/msec_60000.xdmf.json  temp_b3ps/msec_80000.xdmf.json
temp_b3ps/msec_20000.xdmf.json  temp_b3ps/msec_30000.xdmf.json  temp_b3ps/msec_50000.xdmf.json  temp_b3ps/msec_70000.xdmf.json  temp_b3ps/msec_90000.xdmf.json"""

    p = argparse.ArgumentParser()
    p.add_argument(
        "--files", nargs="+", help="input json files from anba", default=da.split()
    )
    p.add_argument("--out", help="output hawc2 file", default="__s123_b3p.st")
    args = p.parse_args()

    scs = dict(
        [(int(re.findall(r"\d+", i)[-1]), json.load(open(i, "rb"))) for i in args.files]
    )

    kw = {"BLADENAME": "s123_b3p", "NSEC": "%i" % len(scs)}

    out = header
    for i in kw:
        out = out.replace(i, kw[i])

    for i in sorted(scs):
        out += "\n" + anba2hawc(i, scs[i])
        # print(i)

    open(args.out, "w").write(out)
    print("written output to %s" % args.out)


if __name__ == "__main__":
    main()
