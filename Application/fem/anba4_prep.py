#! /usr/bin/env python3
import pyvista as pv
import argparse
import multiprocessing
import json
import numpy as np


def vtp2xdmf(vtp):
    """将 .vtp 格式的截面网格转换为 2D XDMF 格式，并导出单元数据到 JSON 侧载文件。

    :param vtp: 输入的 .vtp 网格文件路径
    """
    assert vtp.endswith(".vtp")
    mesh = pv.read(vtp)
    tri = mesh.triangulate()
    tri.points[:, 2] = 0

    # Keep only triangle cells
    faces = []
    lines = []
    for i in range(tri.n_cells):
        cell = tri.get_cell(i)
        if cell.type == pv.CellType.TRIANGLE:
            faces.extend(list(cell.point_ids))
        elif cell.type == pv.CellType.LINE:
            lines.extend(list(cell.point_ids))

    n_faces = len(faces) // 3
    if n_faces == 0:
        print(f"Warning: No triangles found in {vtp}, skipping")
        return

    faces_arr = np.array(faces).reshape(-1, 3)

    # Extract cell data only for face cells
    cell_data = {}
    for key in tri.cell_data.keys():
        all_vals = tri.cell_data[key]
        face_vals = []
        for i in range(tri.n_cells):
            cell = tri.get_cell(i)
            if cell.type == pv.CellType.TRIANGLE:
                face_vals.append(all_vals[i])
        cell_data[key] = np.array(face_vals)

    # Remove unused vertices and renumber
    used_vertices = sorted(set(faces_arr.flatten()))
    old_to_new = {old: new for new, old in enumerate(used_vertices)}
    new_points = tri.points[used_vertices, :2]
    new_faces = np.array([[old_to_new[v] for v in f] for f in faces_arr])

    # Save cell data to JSON sidecar
    json_path = vtp.replace(".vtp", "_cell_data.json")
    with open(json_path, "w") as f:
        json.dump({k: v.tolist() for k, v in cell_data.items()}, f)

    # Write clean 2D XDMF manually
    xd = vtp.replace(".vtp", ".xdmf")

    xdmf_content = f'''<?xml version="1.0"?>
<!DOCTYPE Xdmf SYSTEM "Xdmf.dtd" []>
<Xdmf Version="3.0">
  <Domain>
    <Grid Name="Grid">
      <Geometry GeometryType="XY">
        <DataItem DataType="Float" Dimensions="{new_points.shape[0]} 2" Format="XML" Precision="8">
'''
    for p in new_points:
        xdmf_content += f"          {p[0]:.16e} {p[1]:.16e}\n"

    xdmf_content += f'''        </DataItem>
      </Geometry>
      <Topology TopologyType="Triangle" NumberOfElements="{new_faces.shape[0]}" NodesPerElement="3">
        <DataItem DataType="Int" Dimensions="{new_faces.shape[0]} 3" Format="XML" Precision="8">
'''
    for f in new_faces:
        xdmf_content += f"          {f[0]} {f[1]} {f[2]}\n"

    xdmf_content += '''        </DataItem>
      </Topology>
    </Grid>
  </Domain>
</Xdmf>
'''

    with open(xd, "w") as f:
        f.write(xdmf_content)

    print(f"converted {vtp} to {xd} ({json_path})")


def main():
    """主函数。解析命令行参数，将一组 .vtp 截面网格批量转换为 XDMF 格式。"""
    p = argparse.ArgumentParser(description="translate section meshes from vtk to XDMF and 2D")
    p.add_argument("sections", nargs="*", help="section meshes in .vtp format")
    args = p.parse_args()
    for s in args.sections:
        vtp2xdmf(s)


if __name__ == "__main__":
    main()
