.PHONY: help pbuild

help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
#PY=python
#PY=/home/mich/anaconda3/envs/lubanos2/bin/python
PY37?=/home/mich/miniconda3/envs/fenics/bin/python
PY=$(PY37)
export PKG_CONFIG_PATH := $(HOME)/miniconda3/envs/fenics/lib/pkgconfig:$(PKG_CONFIG_PATH)
B3PPATH?=$(HOME)/b3p
OUT=s123_lam.yml
I=$OUT
DATADIR=./data/
SYSDIR=../sys/
lamplan: ## translate the laminate plan from pblade to b3p
	$(PY37) csv2yml.py --csv_input $(DATADIR)lamplan_S123_600_2.csv --yaml_template $(DATADIR)s123_geom.yaml --matdb $(DATADIR)materials_v9.yml --output  $(DATADIR)$(OUT)

geomimport: ## import the geometry from the .cfg file 
	#$(PY37) cfg2yml.py --cfg $(SYSDIR)system.cfg --baseyaml $(B3PPATH)/examples/blade_test.yml --out $(DATADIR)s123_geom.yaml
	$(PY37) cfg2yml.py --cfg $(DATADIR)S123_test_1.cfg --baseyaml $(B3PPATH)/examples/blade_test.yml --out $(DATADIR)s123_geom.yaml
matdb: ## translate the matdb from pblade to b3p format from sys/system.cfg
	$(PY37) matdb_translate.py	

prep:  matdb  geomimport lamplan ## prepare the yaml model and corresponding matdb

# run the new plybook in b3p
#T = temp_b3ps
T = temp_b3ps
$(shell if [ ! -d "$(T)" ]; then mkdir -p $(T); fi)
$(shell cp ./data/materials_v9.yml $(T)/materials_v9.yml)
#I=s123_v6_g2_l1000.yml

geom: # build the geometry using b3p out dir is in .yml file could not change here
	$(PY) $(B3PPATH)/b3p/build_blade_geometry.py  $(OUT)
structure: ## build the structural mesh using b3p
	$(PY) $(B3PPATH)/b3p/build_blade_structure.py  $(OUT)
plybook: ## build plybook
	$(PY) $(B3PPATH)/b3p/build_plybook.py $(OUT) --out $(T)/plybook.pck
drape: ## drape the shell mesh and webs 
	$(PY) $(B3PPATH)/b3p/drape_mesh.py $(T)/plybook.pck $(T)/test_blade_web.vtp --key blade  --out $(T)/test_blade_shell1.vtu
	$(PY) $(B3PPATH)/b3p/drape_mesh.py  $(T)/plybook.pck $(T)/test_blade_w1.vtp --key w1  --out $(T)/test_blade_w1.vtu 
	$(PY) $(B3PPATH)/b3p/drape_mesh.py  $(T)/plybook.pck $(T)/test_blade_w2.vtp --key w2  --out $(T)/test_blade_w2.vtu
combine: ## add the meshes together 
	#$(PY) $(B3PPATH)/b3p/combine_meshes.py $(T)/test_blade_shell1.vtu   $(T)/test_blade_w1.vtu $(T)/test_blade_w2.vtu --out $(T)/joinedup_mesh.vtu
	$(PY) $(B3PPATH)/b3p/combine_meshes.py $(T)/test_blade_shell1.vtu   $(T)/test_blade_w1.vtu $(T)/test_blade_w2.vtu --out $(T)/test_blade_joined.vtu

pbuild: geom structure plybook drape combine ## build the geometry and structural mesh


mesh2d: # extract 2D meshes 
	#b3p --yml=$(I) mesh2d
	$(PY) $(B3PPATH)/b3p/mesh_2d.py --vtu $(T)/test_blade_joined.vtu --r "[.1,1,2,5,10,20,30,40,50,60,70,80,90,100,110,115]" --var $(T)/test_blade.var --verbose 
	
plot2d: # plot 2d meshes 
	$(PY) ./plot_2d_mesh.py $(T)/msec_*vtp

anbaprep: # run anba prep script (translate meshes from vtp to xdmf)
	$(PY) ./anba4_prep.py $(T)/msec_*.vtp

anba2hawc2: ## convert anba output to hawc2 format
	$(PY) anba2hawc2.py --files $(T)/msec_*.xdmf.json --out $(T)/hawc2_input.st

anbaplot: ## plot anba results
	./compare_st_files.py S123_E_Blade.st temp_b3ps_portable/hawc2_input.st 

panba: ## paralell solver 
	$(PY) $(B3PPATH)/b3p/anba4_solve.py $(T)/msec_*.xdmf $(T)/material_map.json --debug  
p_anba: ## paralell solver 
	$(PY37) anba4_solve.py $T/msec_*.xdmf $(T)/material_map.json --debug   

ccx: ## run ccx on the model
	b3p --yml=$I ccxsolve max_0
	b3p --yml=$I ccxpost max_0

s6x6:  prep build mesh2d anbaprep panba

# ccxpost: ## postprocess ccx output
# 	b3p_frd2vtu $(T)/ccxmodel_lc_max_0.frd --out $(T)/ccx_lc_max_0.vtu
# # b3p_frd2vtu $(T)/ccxmodel_lc_forward_edge.frd --out $(T)/ccx_fe.vtu
# # b3p_frd2vtu $(T)/ccxmodel_lc_forward_flap.frd --out $(T)/ccx_ff.vtu

# # #ccxmodel_lc_forward_flap
# # ccx $(T)/ccxmodel_lc_forward_edge


# ccx: ccxpre ccxsolve ## run ccxpre and ccxsolve

#new run anba file at home fem here
p_all: ## make old b3p 
	make prep pbuild  mesh2d anbaprep p_anba anba2hawc2

