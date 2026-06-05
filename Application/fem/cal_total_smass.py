#! /usr/bin/env python
import pandas as pd
import pyvista as pv
import argparse
import json
import os
import numpy as np
import yaml

"""
:author: michael copy from blac_3p file and make total section mass cal and add together
call check mass which compute the mass of each material in the cross section from the mesh and the material database input. 
"""
def compute_cross_section_mass(mesh, matmap):
    """计算截面中每种材料的质量。

    :param mesh: 网格文件路径
    :param matmap: 材料映射文件路径
    :return: 截面总质量
    """
    mesh = pv.read(mesh).compute_cell_sizes()

    mm = json.load(open(matmap, "r"))
    mdb = yaml.load(
        open(os.path.join(os.path.dirname(matmap), mm["matdb"]), "r"),
        Loader=yaml.CLoader,
    )

    mm["-1"] = -1
    invmd = {mm[i]: i for i in mm}
    sum_mass, sum_area = 0.0, 0.0
    for i in np.unique(mesh.cell_data["mat"]):
        mat_area = (mesh.cell_data["mat"] == i) * mesh.cell_data["Area"]
        mass = (mat_area * mdb[invmd[i]]["rho"]).sum()
        print(
            i,
            invmd[i],
            mdb[invmd[i]]["name"],
            mdb[invmd[i]]["rho"],
            f"{mass=:.3f}, {mat_area.sum()=:.3f}",
        )

        sum_mass += mass
        sum_area += mat_area.sum()

    #print("Total mass:", sum_mass)
    #print("Total area:", sum_area)
    return sum_mass

def main():
    """主函数：计算叶片各截面的总质量，并输出为 CSV 文件。"""
    p = argparse.ArgumentParser()
    p.add_argument("mesh", default="temp_b3ps/msec_*.xdmf", help="mesh")
    args = p.parse_args()
    matdbjson = os.path.join(os.getcwd(),"temp_b3ps", "material_map.json")
    path_cur = os.path.join(os.getcwd(),"./temp_b3ps")
    for folder_path, folders, files in os.walk(path_cur):
        print(folder_path,folders)
        total_mass=0.0
        sec_mass = []
        for file in files:
            nfile = os.path.join(os.getcwd(), "temp_b3ps", file)
            sfile = os.path.splitext(file)
            if sfile[1] == ".xdmf":
                sum_mass = compute_cross_section_mass(nfile, matdbjson)
                print(file,sum_mass)
                total_mass = total_mass + float(sum_mass)
                sec_mass.append([sum_mass,sfile[0]])
        #write to file
        df=pd.DataFrame(sec_mass,columns=["mass","section"])
        df.to_csv("3p_mass_section.csv")
        print("total mass of sections is", total_mass)
        print(sec_mass)
        break
    #load loop25 blade file to calculate mass section
    each_file = os.path.join(os.getcwd(), 'loop25', 'inputs', "Blades.json")
    fp = open(each_file, 'r', encoding=u'utf-8', errors='ignore')
    js_vars = json.load(fp)
    sections = js_vars['Blade']['Sections']
    list = []
    radius = []
    gh_mass = 0.0
    for section in sections:
        list.append([section["Mass"],section["Dist_from_root"]])
        gh_mass = gh_mass + float(section["Mass"])
    fp.close()
    print("total gh blade loop25 mass of sections ", gh_mass)
    df = pd.DataFrame(list, columns=["mass", "section"])
    df.to_csv("gh_lp25_mass_section.csv")
    print("------finish--------------")

if __name__ == "__main__":
    main()
