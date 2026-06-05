
import pyvista as pv
import argparse
import numpy as np

HEADER = """/COM,ANSYS RELEASE 2022 R1           BUILD 22.1      UP20211129       12:24:02
/PREP7
/NOPR
/TITLE,                                                                        
NUMOFF,NODE,   1
NUMOFF,ELEM,   1
NUMOFF,MAT ,     1
NUMOFF,TYPE,        1
NUMOFF,CSYS,   1
DOF,DELETE
ET,        1,181
KEYOP,        1, 8,        1
CSYS,   0
MAT ,       1
TYPE,        1\n"""


def cells2cdb(mesh):
    """将网格单元转换为 ANSYS cdb 格式的 EBLOCK 字符串。

    :param mesh: pyvista 网格对象
    :return: EBLOCK 字符串
    """
    cells = mesh.cells.reshape(-1, 5)
    buf = f"EBLOCK,15,SOLID,1,{cells.shape[0]:d}\n(19i10)\n"
    return (
        buf
        + "".join(
            f"{1:10d}{1:10d}{1:10d}{1:10d}{1:10d}{0:10d}{0:10d}{0:10d}{i[0]:10d}{0:10d}{n:10d}{i[1]+1:10d}{i[2]+1:10d}{i[3]+1:10d}{i[4]+1:10d}\n"
            for n, i in enumerate(cells, start=1)
        )
        + "        -1"
    )


def points2cdb(mesh):
    """将网格节点转换为 ANSYS cdb 格式的 NBLOCK 字符串。

    :param mesh: pyvista 网格对象
    :return: NBLOCK 字符串
    """
    return (
        f"NBLOCK,6,SOLID,    1,      {mesh.points.shape[0]}\n(3i9,6e21.13e3)\n"
        + "".join(
            (
                f"{n:9d}{1:9d}{1:9d}"
                + "".join(
                    [
                        np.format_float_scientific(
                            j,
                            exp_digits=3,
                            precision=13,
                            min_digits=13,
                            pad_left=2,
                            trim="k",
                        ).upper()
                        for j in i
                    ]
                )
                + "\n"
            )
            for n, i in enumerate(mesh.points, start=1)
        )
        + "N,UNBL,LOC,       -1,"
    )


def blockformat(ids):
    """将单元 ID 列表格式化为 ANSYS CMBLOCK 的数据块格式。

    :param ids: 单元 ID 数组或列表
    :return: 格式化后的字符串
    """
    buf = f"{len(ids)}\n(8i10)\n"
    for n, i in enumerate(ids):
        buf += f"{i:10d}"
        if n % 8 == 7:
            buf += "\n"
    return buf + ("\n" if buf[-1] != "\n" else "")


def groups2cdb(mesh):
    """将网格中 ply 相关的单元数据分组为 ANSYS CMBLOCK 字符串。

    :param mesh: pyvista 网格对象
    :return: CMBLOCK 组合字符串
    """
    cmblocks = {}
    for i in mesh.cell_data:
        if i.startswith("ply_"):
            pd = mesh.cell_data[i]
            ids = np.where(pd[:, 1] > 0.0)[0] + 1
            cmblocks[i] = blockformat(ids)

    return "".join(f"CMBLOCK,{i.upper()},{value}" for i, value in cmblocks.items())


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Convert vtu to cdb")
    p.add_argument("mesh", help="Mesh file to load in vtu format")
    p.add_argument("--output", help="Output file name", default="__test.cdb")
    args = p.parse_args()

    # Load the mesh
    mesh = pv.read(args.mesh)
    cbuf = cells2cdb(mesh)
    pbuf = points2cdb(mesh)
    blck = groups2cdb(mesh)

    open(args.output, "w").write(HEADER + pbuf + "\n" + cbuf + "\n" + blck)
    print(f"written cdb to {args.output}")
