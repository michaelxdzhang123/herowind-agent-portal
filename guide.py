#__package__="Luban.Models.Generator"
from ModelMagnet_structure_cooling import GeneratorSys
from LubanToolBox.ExcelAPI import Data2excel
from flask import Blueprint, render_template, request,redirect,Flask
import numpy as np
import time
import re
import os
import json
import codecs
import random
import sys
from collections import OrderedDict
import demjson
import pandas as pd
from config import Config
app = Flask(__name__,instance_relative_config=True)
app.config.from_object(Config)
app.config.from_pyfile('config.py')

guide_bp = Blueprint('guide_bp', __name__)
@guide_bp.route('/guide', methods=['GET', 'POST'])
def guide_route():
        """
        :param P_grid:
        :param P_rated (Generator rated power[MW]):
        :param n_rated (Generator rated speed[rpm]):
        :param Eta (Generator Efficiency[%]):
        :param D_trans (Outer diameter limit of transportation[m])
        :param sys_vars(Generator_Rated_Power[kw]):
        :return: massCost({Generator:{weight[kg],cost[ten thousands]}};Lgenerator[mm])
        """
        my_user = request.cookies.get('username')
        # check if the person in dict.Generator,
        #if my_user not in Generator.dict
            #reuturn 'ask admin to add you in this Model)
        # input_path = os.getcwd() + input +'generator_material_price_list.xlsx'
        #output_path = os.getcwd() + '/results/Generator.xlsx'

        my_sys_path = os.path.join(app.config['WORKING_MODEL_DIR'], my_user)
        if not os.path.isdir(my_sys_path):
            os.mkdir(my_sys_path)
        my_model_dir = os.path.join(my_sys_path,'DeGenerator')
        if not os.path.isdir(my_model_dir):
            os.mkdir(my_model_dir)
        my_model_input = os.path.join(my_model_dir,'input')
        my_model_output = os.path.join(my_model_dir,'output')
        if not os.path.isdir(my_model_input):
            os.mkdir(my_model_input)
        if not os.path.isdir(my_model_output):
            os.mkdir(my_model_input)
        my_sys_vars = os.path.join(my_model_input, 'sys_vars.json')
        fp = open(my_sys_vars, 'r', encoding=u'utf-8', errors='ignore')
        try:
            sys_vars = json.load(fp)
        except:
            # return 'sys variables  xlsx file Error '
            print('sys variables  xlsx file Error ')
        output_values={}
        Print_level = sys_vars["Print_level"]["default"]
        Case_index = sys_vars["Case_index"]["default"]
        Generator_Altitude = sys_vars["Generator_Altitude"]["default"]
        Ambient_temperature = sys_vars["Ambient_temperature"]["default"]
        Generator_cooling_type = sys_vars["Generator_cooling_type"]["default"]
        Application_environment = sys_vars["Application_environment"]["default"]
        Cooling_fan_control = sys_vars["Cooling_fan_control"]["default"]
        Magnet_installing_type = sys_vars["Magnet_installing_type"]["default"]
        P_grid=sys_vars["Turbine_power_rated"]["default"]/1000
        P_rated = P_grid * 1.000 ##1.075
        n_rated=sys_vars["Rated_speed"]["default"]
        Eta=sys_vars["Generator_efficiency"]["default"]*100
        D_trans=sys_vars["Shipping_limit"]["default"]
        print('--- 74 guide.py P_grid, P_rated, n_rated, Eta, D_trans, Print_level==',type(P_grid), type(P_rated), type(n_rated), type(Eta), type(D_trans), type(Print_level))
        #time.sleep(100)
        Generator_cost, Generator_mass, Lgenerator=GeneratorSys(P_grid, P_rated, n_rated, Eta, D_trans, Print_level).ComputeMassCost(
            Ambient_temperature,
            Generator_cooling_type,
            Application_environment,
            Cooling_fan_control,

            Magnet_installing_type,
            Generator_Altitude)
        print('------------------guide 81')
        Generator_massCost={
            "Generator":{
                "weight":Generator_mass,
                "cost":Generator_cost
            }
        }

        print('------------------guide 88')
        output_values={
            "Generator_massCost":Generator_massCost,
            "Lgenerator":Lgenerator
        }
        #output variable to subsystem result folder
        print(output_values)
        output_path=os.path.join(my_model_output, 'Generator.xlsx')
        Gen_df = pd.DataFrame(output_values)
        Gen_df.to_csv(output_path, index=False,sep='\t')
        #return output_values
        return output_values
if __name__ == '__main__':
    from DeGenerator import DeGenerator
    my_user = 'test'
    #input_path = os.getcwd() + input +'generator_material_price_list.xlsx'
    output_path = os.getcwd() + '/results/Generator.xlsx'
    #my_sys_var = os.path.join(app.config['WORKING_MODEL_DIR'], my_user, 'sys_vars.json')
    my_sys_var = os.getcwd() + 'sys_vars.json'
    fp = open(my_sys_var, 'r', encoding=u'utf-8', errors='ignore')
    try:
        js_vars = json.load(fp)
    except:
        #return 'sys variables  xlsx file Error '
        print( 'sys variables  xlsx file Error ')
    #call function
    gen_obj = DeGenerator()
    gen_obj.calculate(js_vars)
