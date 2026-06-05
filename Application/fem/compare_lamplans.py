#! /usr/bin/env python

import pyvista as pv
import sys
import os

shv1 = pv.read(os.path.join(sys.path[0], "temp_b3ps/test_blade_shell1.vtu"))
pbl1 = pv.read(os.path.join(sys.path[0], "temp/test_100/S123_web_drape.vtu"))


if shv1.points.shape != pbl1.points.shape:
    exit("not same level of mesh refinement, cannot compare")


k1 = shv1.cell_data.keys()
k2 = pbl1.cell_data.keys()


for i in k1:
    if i in k2 and i.startswith("ply"):
        vv = shv1.cell_data[i]
        vv1 = pbl1.cell_data[i]

        diff = vv - vv1

        print(i, diff[:, 1:].sum(axis=0))


print((shv1.points - pbl1.points).sum())

# for i in shv1.cell_data:
#     print(i)
# print(k1, k2)
