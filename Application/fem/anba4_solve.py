import warnings
warnings.filterwarnings("ignore", message="pkg_resources is deprecated")

from dolfin import *
from anba4 import *
import argparse
import multiprocessing
import json
import numpy as np
import yaml
import os
from functools import partial
from datetime import datetime


def get_material_db(material_map):
    """从材料映射文件中读取材料数据库，并构建 ANBA4 可用的材料属性字典。

    :param material_map: 材料映射 JSON 文件路径
    :return: 以材料索引为键的材料对象字典
    """
    assert os.path.isfile(material_map)
    mm = json.load(open(material_map, "r"))
    gdir = os.path.dirname(material_map)

    mat_db = None
    if "matdb" in mm:  # check if the material map file points to a material db
        mat_db = yaml.load(open(os.path.join(gdir, os.path.basename(mm["matdb"]))), Loader=yaml.CLoader)

        # check if there is a -1 material in the matdb, and assign it
        # this material ID is used by the section mesher for the bondlines
        # that connect the webs to the shell
        if "-1" in mat_db:
            mm["-1"] = -1
    else:
        exit(
            "material map available, but no link to material db, need matdb definition to do FEA"
        )

    mm_inv = {v: k for k, v in mm.items()}

    materials = {}
    for i in mm_inv:
        if i != mm["matdb"]:
            matdb_entry = mat_db[mm_inv[i]]
            if "tEx" in matdb_entry:  # ortho material
                matMechanicProp = np.zeros((3, 3))
                matMechanicProp[0, 0] = matdb_entry["tEz"]  # e_xx
                matMechanicProp[0, 1] = matdb_entry["tEy"]  # e_yy
                matMechanicProp[0, 2] = matdb_entry["tEx"]  # e_zz

                matMechanicProp[1, 0] = matdb_entry["tGxz"]  # g_yz
                matMechanicProp[1, 1] = matdb_entry["tGxy"]  # g_xz
                matMechanicProp[1, 2] = matdb_entry["tGyz"]  # g_xy

                matMechanicProp[2, 0] = matdb_entry["tnuxz"]  # nu_zy
                matMechanicProp[2, 1] = matdb_entry["tnuxy"]  # nu_zx
                matMechanicProp[2, 2] = matdb_entry["tnuyz"]  # nu_xy

                materials[i] = material.OrthotropicMaterial(
                    matMechanicProp, matdb_entry["rho"]
                )
            else:
                materials[i] = material.IsotropicMaterial(
                    [
                        matdb_entry["E"]
                        if "E" in matdb_entry
                        else matdb_entry["Ex"],
                        matdb_entry["nu"],
                    ],
                    matdb_entry["rho"],
                )

    return materials


def run_mesh(meshname, matdb):
    """读取二维截面网格，使用 ANBA4 计算刚度矩阵、质量矩阵及相关截面属性，并输出为 JSON。

    :param meshname: 二维截面网格文件路径（.xdmf）
    :param matdb: 材料数据库字典
    """
    print(f"run {meshname}")

    infile = XDMFFile(meshname)
    mesh = Mesh()
    infile.read(mesh)

    # Read cell data from companion JSON file (written by anba4_prep.py)
    json_file = meshname.replace(".xdmf", "_cell_data.json")
    if not os.path.isfile(json_file):
        # Fallback: try to read from XDMF using DOLFIN MeshFunction
        # This supports legacy XDMF files with embedded cell data
        json_file = None
    
    if json_file:
        with open(json_file, "r") as f:
            cell_data = json.load(f)
    else:
        cell_data = {}
        # Attempt to read cell data from XDMF directly
        for attr_name in ["mat", "angle", "angle2"]:
            try:
                mf = MeshFunction("double", mesh, mesh.topology().dim())
                with XDMFFile(meshname) as xf:
                    xf.read(mf, attr_name)
                cell_data[attr_name] = [mf[i] for i in range(mesh.num_cells())]
            except Exception:
                pass

    # Basic material parameters. 9 is needed for orthotropic materials.
    # TODO materials and orientations
    # Meshing domain.
    materials = MeshFunction("size_t", mesh, mesh.topology().dim())
    fiber_orientations = MeshFunction("double", mesh, mesh.topology().dim())
    plane_orientations = MeshFunction("double", mesh, mesh.topology().dim())

    mat_values = cell_data.get("mat", [0] * mesh.num_cells())
    angle2_values = cell_data.get("angle2", [0.0] * mesh.num_cells())

    matuniq = np.unique(mat_values)  # material indices (from material_map)

    # map for materials in anba (index in matuniq)
    mat_map_0 = dict(zip(matuniq, range(len(matuniq))))

    matids = [mat_map_0[i] for i in mat_values]

    plane_angles = list(angle2_values)

    materials.set_values(matids)

    # TODO, doesn't work for off axis laminates for now
    fiber_orientations.set_all(0.0)

    # transverse orientations
    plane_orientations.set_values(plane_angles)

    # Build material property library.
    matLibrary = [matdb[i] for i in matuniq]

    # Debug: Check material properties
    print(f"Processing {meshname} with {len(matuniq)} unique materials: {matuniq}")
    for i, mat_id in enumerate(matuniq):
        if mat_id in matdb:
            print(f"  Material {mat_id}: {type(matdb[mat_id])}")
        else:
            print(f"  Warning: Material {mat_id} not found in material database")

    anba = anbax(mesh, 2, matLibrary, materials, plane_orientations, fiber_orientations)
    stiff = anba.compute()

    stiffness_matrix = stiff.getDenseArray()

    # Debug: Check for NaN or inf values in stiffness matrix
    if np.any(np.isnan(stiffness_matrix)) or np.any(np.isinf(stiffness_matrix)):
        print(f"Warning: NaN or inf values found in stiffness matrix for {meshname}")
        print(f"NaN count: {np.sum(np.isnan(stiffness_matrix))}")
        print(f"Inf count: {np.sum(np.isinf(stiffness_matrix))}")
        print(f"Stiffness matrix:\n{stiffness_matrix}")
        return  # Skip this mesh if there are numerical issues

    mass = anba.inertia()

    mass_matrix = mass.getDenseArray()

    decoupled_stiff = DecoupleStiffness(stiff)

    # Debug: Check for NaN or inf values in decoupled stiffness matrix
    if np.any(np.isnan(decoupled_stiff)) or np.any(np.isinf(decoupled_stiff)):
        print(f"Warning: NaN or inf values found in decoupled stiffness matrix for {meshname}")
        print(f"NaN count: {np.sum(np.isnan(decoupled_stiff))}")
        print(f"Inf count: {np.sum(np.isinf(decoupled_stiff))}")
        print(f"Decoupled stiffness matrix:\n{decoupled_stiff}")
        return  # Skip this mesh if there are numerical issues

    angle = PrincipalAxesRotationAngle(decoupled_stiff)

    mass_center = ComputeMassCenter(mass)
    tension_center = ComputeTensionCenter(stiffness_matrix)
    shear_center = ComputeShearCenter(stiffness_matrix)
    output = {
        "name": meshname,
        "stiffness": stiffness_matrix.tolist(),
        "mass_matrix": mass_matrix.tolist(),
        "decoupled_stiffness": decoupled_stiff.tolist(),
        "principal_axes_rotation": angle,
        "mass_center": mass_center,
        "tension_center": tension_center,
        "shear_center": shear_center,
    }

    with open(f"{meshname}.json", "w") as write_file:
        json.dump(output, write_file, indent=4)

    

def main():
    """主函数。解析命令行参数，加载材料数据库，并并行运行多个截面的 ANBA4 计算。"""
    p = argparse.ArgumentParser(description="run a series of sections through anba4")
    p.add_argument("meshes", nargs="*")
    p.add_argument("matdb", help="material map json file")
    p.add_argument("--debug", action="store_true")
    args = p.parse_args()

    mdb = get_material_db(args.matdb)

    part = partial(run_mesh, matdb=mdb)
    if args.debug:
        for i in args.meshes:
            part(i)
    else:
        p = multiprocessing.Pool()
        # run async seems to avoid a sporadic blocking error
        r = p.map_async(part, args.meshes)
        r.wait()
# With timestamp
    with open("check_status.log", "w") as status_file:
        status_file.write("anba4_done")
    

if __name__ == "__main__":
    main()
