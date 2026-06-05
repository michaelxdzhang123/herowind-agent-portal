import yaml
import os
namemap = {
    "e11": "tEx",
    "g12": "tGxy",
    "nu12": "tnuxy",
    "e22": "tEy",
    "e33": "tEz",
    "g23": "tGyz",
    "g31": "tGxz",
    "nu23": "tnuyz",
    "nu31": "tnuxz",
}

if __name__ == "__main__":
    data_file = "./data/v9_materials.dat"
    matdb = eval(open(data_file, "r").read())

    for i in matdb:
        k = matdb[i].keys()
        for j in namemap:
            matdb[i][namemap[j]] = matdb[i][j]

    of = "./data/materials_v9.yml"
    print("writing to %s" % of)
    yaml.dump(matdb, open(of, "w"))
