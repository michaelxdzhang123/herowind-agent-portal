from cmath import polar
from os import path, system, getcwd, listdir,remove,scandir
import math
import json
import json
import json as js
import sys
import time
import re
import logging
import streamlit.components.v1 as components
import time
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend to avoid KeyboardModifier errors
import matplotlib.pyplot as plt
#import blacstab2
import demjson
import os
import socket
import yaml
import pandas as pd
from collections import OrderedDict
import streamlit as st
import pyvista as pv
from stpyvista import stpyvista
#import hiplot as hip
import numpy as np
import requests
import random
from dotenv import load_dotenv
import plotly.graph_objects as go
from utils import Cursor
import mpld3
import streamlit.components.v1 as components
from mpld3 import plugins
from streamlit_navigation_bar import st_navbar
from dotenv import load_dotenv
#from BeaverFramework.beavertools import json2yaml, yaml2json
import plotly.express as px
from ruamel.yaml import YAML
import configparser
import sys
import os

# Add BeaverFramework to Python path for autocomplete
home_dir = os.path.expanduser("~")
beaver_path = os.path.join(home_dir, "apps/beaver-framework")
if beaver_path not in sys.path:
    sys.path.insert(0, beaver_path)

# Import classes with type hints for better autocomplete
from BeaverFramework.Framework.turbine_def import Airfoils 
from BeaverFramework.Framework.turbine_def import Turbine
from BeaverFramework.Framework.turbine_def import Blade 
from BeaverFramework.Framework.turbine_def import Environment
from BeaverFramework.Framework.turbine_def import Nacelle
from BeaverFramework.Framework.turbine_def import Rotor_aero
from BeaverFramework.Framework.turbine_def import AI
from BeaverFramework.Framework.turbine_def import System



#This Application codes from Michael Zhang
load_dotenv()
user_name = os.getenv("USER_NAME")
data_base = os.getenv("BBS_BASE")
run_base = os.getenv("RUN_BASE")
user_log = os.getenv("SYS_LOG")
st.set_page_config(layout="wide")

m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #0099ff;
    color:#ffffff;
}
div.stButton > button:hover {
    background-color: #00ff00;
    color:#ff0000;
    }
</style>""", unsafe_allow_html=True)
# basic dir in .env

new_chords = {}
sections = {}
each_sec = {}
cmp_base = {}
display = True
hostnm=socket.gethostname()
log_path = path.join(getcwd(),'bbs.log')
logger = logging.getLogger("BBS")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(log_path)  # file to adding log info
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
#def edit_cell(row, column,df, options):
#    selected_value = st.selectbox('', options, index=options.index(df.at[row, column]))
#    df.at[row, column] = selected_value



def download_file(file_path, file_name):
    """提供文件下载按钮，用于下载指定路径的文件。

    参数:
        file_path (str): 要下载的文件在服务器上的完整路径。
        file_name (str): 用户下载时显示的文件名称。
    """
    with open(file_path, 'rb') as file:
        file_bytes = file.read()
    st.download_button(
        label="下载模版文件",
        data=file_bytes,
        file_name=file_name,
        mime="application/text-plain"
    )

def main():
    """Streamlit 应用主入口函数，初始化页面布局并提供叶片气动外形、
    翼型、材料、刚度及稳定性分析等各模块的交互界面。
    """
    # Use environment variables for base paths
    home_dir = os.path.expanduser("~")
    dir_path_sys=path.join(home_dir, user_name, 'RunData/sys')
    dir_path_shape=path.join(home_dir, user_name, 'RunData/aero_shape')
    dir_path_fem=path.join(home_dir, user_name, 'RunData/fem')
    dir_path_stab2=path.join(home_dir, user_name, 'RunData/stab2')
    #recall system.cfg file first
    sys_file_path = "../sys/system.cfg"
    file_name = "system.cfg"
    config = configparser.ConfigParser()
    config.read(sys_file_path)
    objectives = config["objectives"]
    tb_cfg = config["turbine"]
    env_cfg = config["environment"]
    page = st_navbar(["SysIters","Shapes", "Airfoils","FoilsPolars","Material","MakeGeo",\
        "Lamplan","Stiffness","Stability","AIReport"])
    col1, col2, col3,col4,col5 = st.columns(5)
    if page == "SysIters":

         #AEP [GWh]
        st.divider()
        sl1,sl2,sl3,sl4 = st.columns(4)
        with sl1:
            System.min_aep_hours = st.text_input("min_aep_hour", value=objectives["min_aep_hours"], key="min_aep_hour")
            #Aero CPmax [-] e.g. >0.47
            Blade.Cp_max = st.text_input("cp_max", value=objectives["Cp_max"], key="Cp_max")
            #Blade mass [ton] e.g. 50
            Blade.mass_total = st.text_input("blade_mass_total", value=objectives["blade_mass_total"], key="blade_mass_total")
            #Blade cost [RMB] e.g. 8 mil for 3 blades
            #blade_cost: 8
            #Blade load [MNm] e.g. 90
            #max_loads : 
            #Blade thrust [MN] e.g. xx
            System.max_tip_speed = st.text_input("max_tip_speed", value=objectives["max_tip_speed"], key="max_tip_speed")
            #load envelope max , unit
            #load_evlop: [('xxx_Mxy',1500),(xxxx_Mxy",130)]
            #Average wind speed at hub height for Design [m/s] e.g. 10
            Environment.Annual_windspeed = st.text_input("wind_speed_avg", value=env_cfg["wind_speed_avg"], key="wind_speed_avg")
            #Weibull shape facor, k [-] e.g. 2.3
            Environment.A_value = st.text_input("A value", value=env_cfg["a_value"], key="A_value")
            Environment.K_value = st.text_input("K value", value=env_cfg["k_value"], key="K_value")
            #Vref [m/s] e.g. 57
            Environment.EWS_50yrs_10min = st.text_input("Vref", value=env_cfg["Vref"], key="Vref")
            #Reference TI [%] e.g. 10
            Environment.effectiveTI_15 = st.text_input("Turblence ", value=env_cfg["TI"], key="TI")
        with sl2:
            #Rated power, P [MW] e.g. 16
            Turbine.power_rated = st.text_input("Turbine_power_rated", value=tb_cfg["Turbine_power_rated"], key="Turbine_power_rated")
            #Rotor diameter range, RD [m] e.g. 250-253
            Turbine.Rotor_diameter = st.text_input("Rotor_diameter", value=tb_cfg["rotor_diameter"], key="Rotor_diameter")
            System.hub_diameterr = st.text_input("hub_diameter", value=tb_cfg["hub_diameter"], key="hub_diameter")
            #Hub height, HH [m] e.g. 150
            System.hub_height = st.text_input("hub_height", value=tb_cfg["hub_height"], key="hub_height")
            #Cut-in wind speed [m/s] e.g. 4
            Turbine.ws_cutin = st.text_input("s_speed", value=tb_cfg["start_speed"], key="start_speed")
            Turbine.ws_cutout = st.text_input("last_speed", value=tb_cfg["last_speed"], key="last_speed")
            Turbine.ws_power_rated = st.text_input("rated_wind_speed", value=tb_cfg["rated_wind_speed"], key="rated_wind_speed")
            #Loss model [%] e.g. 10% or loss model in hawc2/bladed format
            #Average air density [kg/m3] e.g. 1.2
            Environment.mean_air_density = st.text_input("air_density", value=env_cfg["air_density"], key="air_density")
            #Minimum air density [kg/m3] e.g. 0.9
            Environment.mean_air_density = st.text_input("air_density_min", value=env_cfg["air_density_min"], key="air_density_min")

        with col1:
            download_file(sys_file_path, "system.cfg")
        with col2:
            if st.button("Save to system.cfg"):
                # Save configuration logic - update config with current values
                try:
                    # Update objectives section
                    config["objectives"]["min_aep_hours"] = st.session_state.get("min_aep_hour", objectives["min_aep_hours"])
                    config["objectives"]["Cp_max"] = st.session_state.get("Cp_max", objectives["Cp_max"])
                    config["objectives"]["blade_mass_total"] = st.session_state.get("blade_mass_total", objectives["blade_mass_total"])
                    config["objectives"]["max_tip_speed"] = st.session_state.get("max_tip_speed", objectives["max_tip_speed"])
                    
                    # Update environment section
                    config["environment"]["wind_speed_avg"] = st.session_state.get("wind_speed_avg", env_cfg["wind_speed_avg"])
                    config["environment"]["a_value"] = st.session_state.get("A_value", env_cfg["a_value"])
                    config["environment"]["k_value"] = st.session_state.get("K_value", env_cfg["k_value"])
                    config["environment"]["Vref"] = st.session_state.get("Vref", env_cfg["Vref"])
                    config["environment"]["TI"] = st.session_state.get("TI", env_cfg["TI"])
                    config["environment"]["air_density"] = st.session_state.get("air_density", env_cfg["air_density"])
                    config["environment"]["air_density_min"] = st.session_state.get("air_density_min", env_cfg["air_density_min"])
                    
                    # Update turbine section
                    config["turbine"]["Turbine_power_rated"] = st.session_state.get("Turbine_power_rated", tb_cfg["Turbine_power_rated"])
                    config["turbine"]["rotor_diameter"] = st.session_state.get("Rotor_diameter", tb_cfg["rotor_diameter"])
                    config["turbine"]["hub_diameter"] = st.session_state.get("hub_diameter", tb_cfg["hub_diameter"])
                    config["turbine"]["hub_height"] = st.session_state.get("hub_height", tb_cfg["hub_height"])
                    config["turbine"]["start_speed"] = st.session_state.get("start_speed", tb_cfg["start_speed"])
                    config["turbine"]["last_speed"] = st.session_state.get("last_speed", tb_cfg["last_speed"])
                    config["turbine"]["rated_wind_speed"] = st.session_state.get("rated_wind_speed", tb_cfg["rated_wind_speed"])
                    
                    # Write the updated config back to file
                    with open(sys_file_path, 'w') as configfile:
                        config.write(configfile)
                    
                    st.success("Configuration saved successfully!")
                except Exception as e:
                    st.error(f"Error saving configuration: {str(e)}")
 
    if page == "Shapes":
        #Shape_Existing, Shape_upload_JSON, Shape_upload_YAML, save_all, logOFF = st.tabs(["Shape_Existing","Shape_upload_JSON" ,"Shape_upload_YAML","save_all","logOFF"]) 
        with col1:
            option = st.selectbox("系统选择",("Shape_Existing","Shape_upload_JSON" ,"download all foils","next to Airfoils selection"))
        if option == "Shape_upload_JSON":
            data_json = {}    
            
           
            """Function to upload JSON files to blade shape directory"""
            target_dir = os.path.join(data_base, "aero_shape/inputs/blade_shape")
            
            # Ensure directory exists
            os.makedirs(target_dir, exist_ok=True)
            
            uploaded_file = st.file_uploader(
                "Upload JSON blade shape file", 
                type=["json"], 
                help="Upload a JSON file containing blade shape data"
            )
            
            if uploaded_file is not None:
                try:
                    # Save uploaded file to target directory
                    file_path = os.path.join(target_dir, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    st.success(f"File {uploaded_file.name} uploaded successfully to {target_dir}")
                    
                    # Process the JSON data
                    uploaded_file.seek(0)  # Reset file pointer
                    data_json = pd.read_json(uploaded_file)
                    
                    # Validate JSON structure
                    if 'Blade' in data_json and 'Sections' in data_json['Blade']:
                        st.success("JSON file structure validated successfully!")
                        return data_json
                    else:
                        st.error("Invalid JSON structure. Expected 'Blade' -> 'Sections' format.")
                        return None
                        
                except Exception as e:
                    st.error(f"Error uploading file: {str(e)}")
                    return None
            else:
                st.info("Please select a JSON file to upload")
            


        
        elif option == "Shape_Existing": 
            with col2:
                #st.write("选择一个初始形状叶片")
                data_json = {}
                list_inputs_dir = os.path.join(data_base,"aero_shape/inputs/blade_shape")
                list_files = os.listdir(list_inputs_dir)
                file_ch = st.selectbox("选择一个叶片形状", (list_files))
                ext_file = os.path.join(list_inputs_dir,file_ch)
                data_json= pd.read_json(ext_file) 
                
                sections = data_json['Blade']['Sections'] 
                #st.write(sections)           
                shows = True         
                #st.write("show_xx ",show_secs,show_rel_Thick,show_twist)
        elif option == "download all foils":
            my_export_name = st.text_input("input a zip file name eg. my_zip")
            if my_export_name and st.button("Create and Download Zip"):
                import zipfile
                import tempfile
                
                # Directory to zip
                dir_to_zip = os.path.join(data_base, "aero_shape/inputs/blade_shape")
                
                # Create temporary zip file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_file:
                    with zipfile.ZipFile(tmp_file.name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        # Walk through the directory and add all files
                        for root, dirs, files in os.walk(dir_to_zip):
                            for file in files:
                                file_path = os.path.join(root, file)
                                # Add file to zip with relative path
                                arcname = os.path.relpath(file_path, dir_to_zip)
                                zipf.write(file_path, arcname)
                    
                    # Read the zip file content
                    with open(tmp_file.name, 'rb') as f:
                        zip_data = f.read()
                    
                    # Provide download button
                    st.download_button(
                        label=f"Download {my_export_name}.zip",
                        data=zip_data,
                        file_name=f"{my_export_name}.zip",
                        mime="application/zip"
                    )
                    
                    # Clean up temporary file
                    os.unlink(tmp_file.name)
                    
                st.success(f"Zip file '{my_export_name}.zip' created successfully!")
            
            shows = False
        elif option == "next to Airfoils selection":
            quit()

        if (option =="Shape_Existing" or option =="Shape_upload_YAML"):
            #sections = data_json['Blade']['Sections']
            #st.write(sections)
            ChordThick,abs_Chord,abs_Thick,Twist,rel_Thick = st.tabs(["ChordThick","abs_Chord","abs_Thick","Twist","rel_Thick"])
            list_Chord = []
            list_Thick_abs = []
            list_Twist = []
            list_Thickness = []
            radius = []
            all_list = []
            #st.write(sections)
            for section in sections:
                list_Chord.append(section["ab_Chord"])
                list_Thick_abs.append(section["ab_Thickness"])
                list_Twist.append(section["Twist"])
                list_Thickness.append(section["rel_Thickness"]) 
                #st.write(section["rel_Thickness"])
                radius.append(section["Dist_from_root"])
            #st.write(list_Thickness)
            all_list.append(list_Chord)
            all_list.append(list_Thick_abs)     
            df = pd.DataFrame(all_list,dtype=float,columns=radius)
            df.index= ["Chord","Thick_abs"]  
            sect_save = True
            if sect_save:
                    all_list.append(list_Twist)
                    all_list.append(list_Thick_abs)
                    all_list.append(list_Thickness)
                    df.index= ["Chord","Thick_abs"]  
                    df.to_csv("./read_json_df.csv")
            #st.write('Aeroshape Regarding , shape analysis ',df.T)
            x_size = int(np.max(np.array(radius))) + 5 
            y_size = int(np.max(np.array(list_Chord))) + 1
            show_top = True
            x = np.array(radius)
            y = np.array(df.T)
            my_labels = ["Chord","abs_thickness"]
            with ChordThick:
                fig1 = plt.figure(figsize=(15,5))
                #plt.subplot(411)
                plt.plot(x,y, color='tab:blue',marker='.')
                plt.grid(True,axis='x',which='both',linestyle='--',color='gray',alpha=0.5)
                plt.grid(True,axis='y',which='both',linestyle='--',color='lightblue',alpha=0.5)
                plt.xticks(np.arange(0,x_size,5))
                plt.yticks(np.arange(0,y_size,0.5))
                plt.xlabel("blade raduis m")
                plt.ylabel("absolute Chord ")
                plt.legend(loc="best", labels=my_labels)
                plt.tight_layout()
                for axes in fig1.axes:
                    for line in axes.get_lines():
                        # get the x and y coords
                        xy_data = line.get_xydata()
                        labels = []
                        for x, y in xy_data:
                            # Create a label for each point with the x and y coords
                            html_label = f'<table border="1" class="dataframe"> <thead> <tr style="text-align: right;"> </thead> <tbody> <tr> <th>x</th> <td>{x}</td> </tr> <tr> <th>y</th> <td>{y}</td> </tr> </tbody> </table>'
                            labels.append(html_label)
                        # Create the tooltip with the labels (x and y coords) and attach it to each line with the css specified
                        tooltip = plugins.PointHTMLTooltip(line, labels, css=css)
                        # Since this is a separate plugin, you have to connect it
                        plugins.connect(fig1, tooltip)
                fig_html = mpld3.fig_to_html(fig1)
                components.html(fig_html,width=2600, height=490)                   
            with Twist:
                y2 = np.array(list_Twist)
                x =  np.array(radius)
                y_size = int(np.max(np.array(list_Twist))) + 1
                x_size = int(np.max(np.array(radius)))+5
                fig2 = plt.figure(figsize=(15,5))
                plt.plot(x,y2, color='tab:blue',marker='.')
                plt.grid(True,axis='x',which='both',linestyle='--',color='gray',alpha=0.5)
                plt.grid(True,axis='y',which='both',linestyle='--',color='gray',alpha=0.5)
                plt.xticks(np.arange(0,x_size,5))
                plt.yticks(np.arange(0,y_size,1))
                plt.xlabel("blade raduis m")
                plt.ylabel("Relative Thickness % ")
                plt.legend(loc="best", labels="Twist Angle")
                plt.tight_layout()
                for axes in fig2.axes:
                    for line in axes.get_lines():
                        # get the x and y coords
                        xy_data = line.get_xydata()
                        labels = []
                        for x, y in xy_data:
                            # Create a label for each point with the x and y coords
                            html_label = f'<table border="1" class="dataframe"> <thead> <tr style="text-align: right;"> </thead> <tbody> <tr> <th>x</th> <td>{x}</td> </tr> <tr> <th>y</th> <td>{y}</td> </tr> </tbody> </table>'
                            labels.append(html_label)
                        # Create the tooltip with the labels (x and y coords) and attach it to each line with the css specified
                        tooltip = plugins.PointHTMLTooltip(line, labels, css=css)
                        # Since this is a separate plugin, you have to connect it
                        plugins.connect(fig2, tooltip)
                fig_html = mpld3.fig_to_html(fig2)
                components.html(fig_html,width=2600, height=499)
            with abs_Thick:          
                y_size = int(np.max(np.array(list_Thick_abs)))
                #st.write(y_size)
                fig3 = plt.figure(figsize=(15,5))
                x = np.array(radius)
                y1 = np.array(list_Thick_abs)
                plt.plot(x,y1, color='tab:blue',marker='.')
                plt.grid(True,axis='x',which='both',linestyle='--',color='gray',alpha=0.5)
                plt.grid(True,axis='y',which='both',linestyle='--',color='gray',alpha=0.5)
                plt.xticks(np.arange(0,x_size,5))
                plt.yticks(np.arange(0,y_size,0.5))
                plt.xlabel("blade raduis m")
                plt.ylabel("absolute Thickness % ")
                plt.legend(loc="best", labels="absolute Thickness")
                plt.tight_layout()
                for axes in fig3.axes:
                    for line in axes.get_lines():
                        # get the x and y coords
                        xy_data = line.get_xydata()
                        labels = []
                        for x, y in xy_data:
                            # Create a label for each point with the x and y coords
                            html_label = f'<table border="1" class="dataframe"> <thead> <tr style="text-align: right;"> </thead> <tbody> <tr> <th>x</th> <td>{x}</td> </tr> <tr> <th>y</th> <td>{y}</td> </tr> </tbody> </table>'
                            labels.append(html_label)
                        # Create the tooltip with the labels (x and y coords) and attach it to each line with the css specified
                        tooltip = plugins.PointHTMLTooltip(line, labels, css=css)
                        # Since this is a separate plugin, you have to connect it
                        plugins.connect(fig3, tooltip)
                fig_html = mpld3.fig_to_html(fig3)
                components.html(fig_html,width=2600, height=499)
            
            with rel_Thick: 
                #st.write(list_Thickness)         
                y_size = int(100*np.max(np.array(list_Thickness)))
                fig4 = plt.figure(figsize=(15,5))
                x = np.array(radius)
                y1 = np.array(list_Thickness)*100
                plt.plot(x,y1, color='tab:blue',marker='.')
                plt.grid(True,axis='x',which='both',linestyle='--',color='gray',alpha=0.5)
                plt.grid(True,axis='y',which='both',linestyle='--',color='gray',alpha=0.5)
                y_size = 100
                plt.xticks(np.arange(0,x_size,5))
                plt.yticks(np.arange(0,y_size,5))
                plt.xlabel("blade raduis m")
                plt.ylabel("Relative Thickness % ")
                plt.legend(loc="best", labels="Reletive Thickness")
                plt.tight_layout()
                for axes in fig4.axes:
                    for line in axes.get_lines():
                        # get the x and y coords
                        xy_data = line.get_xydata()
                        labels = []
                        for x, y in xy_data:
                            # Create a label for each point with the x and y coords
                            html_label = f'<table border="1" class="dataframe"> <thead> <tr style="text-align: right;"> </thead> <tbody> <tr> <th>x</th> <td>{x}</td> </tr> <tr> <th>y</th> <td>{y}</td> </tr> </tbody> </table>'
                            labels.append(html_label)
                        # Create the tooltip with the labels (x and y coords) and attach it to each line with the css specified
                        tooltip = plugins.PointHTMLTooltip(line, labels, css=css)
                        plugins.connect(fig4, tooltip)
                fig_html = mpld3.fig_to_html(fig4)
                components.html(fig_html,width=2600, height=499)
                        # Since this is a separate plugin, you have to connect it
            with abs_Chord:
                y2 = np.array(list_Chord)
                x =  np.array(radius)
                y_size = int(np.max(np.array(list_Chord))) + 1
                x_size = int(np.max(np.array(radius)))+5
                fig5 = plt.figure(figsize=(15,5))
                plt.plot(x,y2, color='tab:blue',marker='.')
                plt.grid(True,axis='x',which='both',linestyle='--',color='gray',alpha=0.5)
                plt.grid(True,axis='y',which='both',linestyle='--',color='gray',alpha=0.5)
                plt.xticks(np.arange(0,x_size,5))
                plt.yticks(np.arange(0,y_size,0.5))
                plt.xlabel("blade raduis m")
                plt.ylabel("absolute Thickness % ")
                plt.legend(loc="best", labels="absolute Thickness")
                plt.tight_layout()
                for axes in fig5.axes:
                    for line in axes.get_lines():
                        # get the x and y coords
                        xy_data = line.get_xydata()
                        labels = []
                        for x, y in xy_data:
                            # Create a label for each point with the x and y coords
                            html_label = f'<table border="1" class="dataframe"> <thead> <tr style="text-align: right;"> </thead> <tbody> <tr> <th>x</th> <td>{x}</td> </tr> <tr> <th>y</th> <td>{y}</td> </tr> </tbody> </table>'
                            labels.append(html_label)
                        tooltip = plugins.PointHTMLTooltip(line, labels, css=css)
                        plugins.connect(fig5, tooltip)
                fig_html = mpld3.fig_to_html(fig5)
                components.html(fig_html,width=2600, height=499)
    elif page == "Airfoils":
        #assign to thickness on  screen 
        foils_dir = os.path.join(data_base, "airfoils")
        air_file_list = []
        for file in os.listdir(foils_dir):
            air_file_list.append(file)
        foil_analysis, upload_foil = st.columns(2)
        with upload_foil:  
            uploaded_file = st.file_uploader("上传翼型文件.dat",type=["dat"]) 
            if uploaded_file is not None: 
                my_output_dir = os.path.join(data_base, "airfoils")
                # Move uploaded file to base directory
                target_path = os.path.join(my_output_dir,uploaded_file.name)
                with open(target_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                st.success(f"File saved to: {target_path}")
                
                datain = pd.read_csv(uploaded_file)
                #st.write(datain)
                
                my_output_dir = os.path.join(data_base, "airfoils")
                filename = uploaded_file.name
                df = pd.read_csv(os.path.join(my_output_dir,filename),sep='\s+', skiprows=1, names=['x','y'])
                x = pd.array(df['x'])
                y = pd.array(df['y'])
                fig = plt.figure(1,figsize=(6,2),dpi=20)
                plt.plot(x,y)
                plt.legend(loc="best",labels=['x','y'])
                plt.tight_layout()
                st.pyplot(fig)
            else:
                #show a profile 
                my_output_dir = os.path.join(data_base, "airfoils")
                # Get the first file name from the directory
                files_in_dir = os.listdir(my_output_dir)
                if files_in_dir:
                    filename = files_in_dir[0]  # Get the first file
                else:
                    st.error(f"error no foil file exit, please mkdir : airfoils based on", my_output_dir)   # fallback if directory is empty
                
                try:
                    df = pd.read_csv(os.path.join(my_output_dir,filename),sep='\s+', skiprows=1, names=['x','y'])
                    #st.write(df['x'])
                    x = pd.array(df['x'])
                    y = pd.array(df['y'])
                    fig = plt.figure(1,figsize=(6,2),dpi=20)
                    plt.plot(x,y)
                    plt.legend(loc="best",labels=['x','y'])
                    plt.tight_layout()
                    st.pyplot(fig)
                except Exception as e:
                    st.error(f"Error reading file {filename}: {str(e)}")
                    st.write(f"Directory: {my_output_dir}")
                    st.write(f"Available files: {files_in_dir}")
        with foil_analysis:
            air_file_list = []
            for file in os.listdir(foils_dir):
                air_file_list.append(file)
            air_select = st.selectbox("选择一个翼型分析",(air_file_list))
            my_output_dir = os.path.join(data_base, "airfoils")
            if air_select is not None:
                this_dat = os.path.join('./airfoils',air_select)
                this_Re = st.number_input("Re",value=1e6,help="Re input, eg. 1e6")
                this_polar = air_select
                this_aoa = st.number_input("AOA",value=0,help=" angle of attack, eg: 0 or 1 or 0 2 4 6 ")        
                #os.system("./xfoil_shell.sh %s %s %s %s" % (this_dat, this_Re, this_polar, this_aoa))
                #time.sleep(2)
                #plot here
                #st.image("1.png")
                #df1 = pd.read_csv(os.path.join("outputs/this_polar", this_polar), skiprows=6)
                #st.write(df1)
            else:
                this_dat =  "./airfoils/naca0017.dat"
                this_Re = 1e6
                this_polar = os.path.basename(this_dat).split('.')[0] + ".txt" 
                this_aoa = 2
            if st.button("分析"):
                os.system("./xfoil_shell.sh %s %s %s %s" % (this_dat, this_Re, this_polar, this_aoa))
                time.sleep(2)
                st.image("1.png")
    elif page == "FoilsPolars":
        foils_dir = os.path.join(data_base, "airfoils")
        air_file_list = []
        for file in os.listdir(foils_dir):
            air_file_list.append(file)
        polars_file_list = []
        polars_dir = os.path.join(data_base, "polars")
        for file in os.listdir(polars_dir):
            polars_file_list.append(file)
        foils_assign, polars_assign = st.columns(2)
        with foils_assign:
            st.write("编辑一组翼型去使用")     
            #load fem/s123_lam.yml and update the airfoils and thickness list and also add to system.cfg file
            # Check if airfoils exist and handle both cases
            if  "airfoils" in config["airfoils"] and config["airfoils"]["airfoils"]:
                # If airfoils exist, extract them for the DataFrame
                existing_airfoils = config["airfoils"]["airfoils"]
                if isinstance(existing_airfoils, dict):
                    # If it's a dictionary (thickness: filename format)
                    airfoil_names = []
                    thickness_values = []
                    for thickness, filename in existing_airfoils.items():
                        airfoil_names.append(filename)
                        thickness_values.append(str(thickness))  # Convert to string
                else:
                    # If it's a list (old format)
                    if isinstance(existing_airfoils, list) and len(existing_airfoils) > 1:
                        airfoil_names = existing_airfoils[1] if isinstance(existing_airfoils[1], list) else [existing_airfoils[1]]
                        thickness_values = existing_airfoils[0] if isinstance(existing_airfoils[0], list) else [str(existing_airfoils[0])]
                    else:
                        # Handle case where existing_airfoils is a single value or empty
                        airfoil_names = [existing_airfoils] if existing_airfoils else [""]
                        thickness_values = ["0.0"]
                
                # Ensure both are lists before creating DataFrame
                if not isinstance(airfoil_names, list):
                    airfoil_names = [airfoil_names]
                if not isinstance(thickness_values, list):
                    thickness_values = [str(thickness_values)]
                
                new_df = pd.DataFrame({
                    "thickness": thickness_values,  # String values
                    "airfoil_name": airfoil_names
                })
            else:
                # If no airfoils exist, create empty DataFrame
                new_df = pd.DataFrame({"airfoil_name": [""], "thickness": ["0.0"]})  # String values
            
            st.write("请选择每一行的翼型文件来填充 airfoil_name 列并点击下方保存：")
            #st.dataframe(new_df)  # Display the initial data


            edited_df = st.data_editor(
                new_df,
                column_config={
                    "airfoil_name": st.column_config.SelectboxColumn(
                        label="airfoil_name",
                        options=air_file_list,
                        help="选择一个翼型文件来填充本行"
                    ),
                    "thickness": st.column_config.TextColumn(
                        label="thickness",
                        help="输入厚度值 (例如: 0.21, 0.27)",
                        default="0.0"
                    )
                },
                num_rows="dynamic",
                use_container_width=True,
                hide_index=True,
                key="airfoil_editor_1"
            )

            if st.button("保存到 system.cfg"):
                try:
                    # Load system.cfg file
                    system_cfg_path = "../sys/system.cfg"
                    
                    # Debug: Check if file exists and is writable
                    if os.path.exists(system_cfg_path):
                        st.write(f"File exists: {system_cfg_path}")
                    else:
                        st.write(f"File does not exist: {system_cfg_path}")
                        # Try absolute path
                        system_cfg_path = os.path.abspath(system_cfg_path)
                        st.write(f"Trying absolute path: {system_cfg_path}")
                    
                    system_config = configparser.ConfigParser()
                    system_config.read(system_cfg_path)
                    
                    # Create airfoils dictionary
                    airfoils_dict = {}
                    for i, (name, thickness) in enumerate(zip(edited_df["airfoil_name"].tolist(), edited_df["thickness"].tolist())):
                        if name.strip() and thickness != "":
                            # Add to dictionary with thickness as key and filename as value
                            airfoils_dict[float(thickness)] = f"../data/Airfoils/{name.strip()}"
                    
                    # Create the airfoils string in the desired format
                    airfoils_str = "airfoils={" + ", ".join([f"{k}: '{v}'" for k, v in airfoils_dict.items()]) + "}"
                    
                    # Debug: Show what will be written
                    Debug = True
                    if Debug:
                        st.write("Airfoils dictionary to be written:")
                        st.write(airfoils_str)
                    
                    # Read the existing system.cfg file
                    with open(system_cfg_path, 'r') as configfile:
                        content = configfile.read()
                    
                    # Replace or add the airfoils section
                    import re
                    # Remove existing [airfoils] section if it exists
                    content = re.sub(r'\[airfoils\][^\[]*', '', content, flags=re.DOTALL)
                    # Add the new [airfoils] section with dictionary format
                    content += f"\n[airfoils]\n{airfoils_str}\n"
                    
                    # Write the updated content back to the file
                    with open(system_cfg_path, 'w') as configfile:
                        configfile.write(content)
                    
                    # Verify the file was written
                    if os.path.exists(system_cfg_path):
                        st.success(f"已保存 airfoils 和 thickness 到 {system_cfg_path}")
                        st.write("Saved format:")
                        st.code(f"[airfoils]\n{airfoils_str}")
                    else:
                        st.error("文件保存失败 - 文件不存在")
                        
                except Exception as e:
                    st.error(f"保存到 system.cfg 失败: {e}")
                    import traceback
                    st.write(traceback.format_exc())
        with polars_assign:
            st.write("编辑一组polars去使用")     
            # Check if polars exist and handle both cases
            if  "polars" in config["airfoils"] and config["airfoils"]["polars"]:
                # If airfoils exist, extract them for the DataFrame
                existing_airfoils = config["airfoils"]["polars"]
                if isinstance(existing_airfoils, dict):
                    # If it's a dictionary ( format)
                    polar_names = []
                    thickness_values = []
                    for thickness, filename in existing_airfoils.items():
                        polar_names.append(filename)
                        thickness_values.append(str(thickness))  # Convert to string
                else:
                    # If it's a list (old format)
                    if isinstance(existing_airfoils, list) and len(existing_airfoils) > 1:
                        polar_names = existing_airfoils[1] if isinstance(existing_airfoils[1], list) else [existing_airfoils[1]]
                        thickness_values = existing_airfoils[0] if isinstance(existing_airfoils[0], list) else [str(existing_airfoils[0])]
                    else:
                        # Handle case where existing_airfoils is a single value or empty
                        polar_names = [existing_airfoils] if existing_airfoils else [""]
                        thickness_values = ["0.0"]
                
                # Ensure both are lists before creating DataFrame
                if not isinstance(polar_names, list):
                    polar_names = [polar_names]
                if not isinstance(thickness_values, list):
                    thickness_values = [str(thickness_values)]
                
                new_df = pd.DataFrame({
                    "thickness": thickness_values,  # String values
                    "polar_name": polar_names
                })
            else:
                # If no airfoils exist, create empty DataFrame
                new_df = pd.DataFrame({"polar_name": [""], "thickness": ["0.0"]})  # String values
            
            st.write("请选择每一行的polar文件来填充polar_name 列并点击下方保存：")
            #st.dataframe(new_df)  # Display the initial data

            # Get polar file options
            polar_dir = os.path.join(run_base, "data", "Polars")
            polar_options = []
            if os.path.exists(polar_dir):
                polar_files = [f for f in os.listdir(polar_dir) if f.endswith('.dat')]
                polar_options = polar_files
            
            edited_df = st.data_editor(
                new_df,
                column_config={
                    "polar_name": st.column_config.SelectboxColumn(
                        label="polar_name",
                        options=polars_file_list,
                        help="选择一个polar文件来填充本行",
                    ),
                    "thickness": st.column_config.TextColumn(
                        label="thickness",
                        help="输入厚度值 (例如: 0.21, 0.27)",
                        default="0.0"
                    )
                },
                num_rows="dynamic",
                use_container_width=True,
                hide_index=True,
                key="polar_editor_2"
            )

            if st.button("保存polars到 system.cfg"):
                try:
                    # Load system.cfg file
                    system_cfg_path = "../sys/system.cfg"
                    
                    # Debug: Check if file exists and is writable
                    if os.path.exists(system_cfg_path):
                        st.write(f"File exists: {system_cfg_path}")
                    else:
                        st.write(f"File does not exist: {system_cfg_path}")
                        # Try absolute path
                        system_cfg_path = os.path.abspath(system_cfg_path)
                        st.write(f"Trying absolute path: {system_cfg_path}")
                    
                    system_config = configparser.ConfigParser()
                    system_config.read(system_cfg_path)
                    
                    # Create polars dictionary
                    polars_dict = {}
                    for i, (name, thickness) in enumerate(zip(edited_df["polar_name"].tolist(), edited_df["thickness"].tolist())):
                        if name.strip() and thickness != "":
                            # Add to dictionary with thickness as key and filename as value
                            polars_dict[float(thickness)] = f"../data/Polars/{name.strip()}"
                    
                    # Create the polars string in the desired format
                    polars_str = "polars={" + ", ".join([f"{k}: '{v}'" for k, v in polars_dict.items()]) + "}"
                    
                    # Debug: Show what will be written
                    Debug = True
                    if Debug:
                        st.write("Polars dictionary to be written:")
                        st.write(polars_str)
                    
                    # Read the existing system.cfg file
                    with open(system_cfg_path, 'r') as configfile:
                        content = configfile.read()
                    
                    # Replace or add the polars section
                    import re
                    # Remove existing [polars] section if it exists
                    content = re.sub(r'\[polars\][^\[]*', '', content, flags=re.DOTALL)
                    # Add the new [polars] section with dictionary format
                    content += f"\n[polars]\n{polars_str}\n"
                    
                    # Write the updated content back to the file
                    with open(system_cfg_path, 'w') as configfile:
                        configfile.write(content)
                    
                    # Verify the file was written
                    if os.path.exists(system_cfg_path):
                        st.success(f"已保存 polars 和 thickness 到 {system_cfg_path}")
                        st.write("Saved format:")
                        st.code(f"[polars]\n{polars_str}")
                    else:
                        st.error("文件保存失败 - 文件不存在")
                        
                except Exception as e:
                    st.error(f"保存到 system.cfg 失败: {e}")
                    import traceback
                    st.write(traceback.format_exc())
    elif page == "MakeGeo":
        #paravewweb to show .vtk file
        col1, col2,col3,col4, col5, col6 = st.columns(6)
        
        yamlfile = os.path.join(run_base, "fem","s123_lam.yml")
        config = yaml.load(open(yamlfile, "r"), Loader=yaml.CLoader)
        shape_base = config["planform"]
        Chord_base = shape_base["chord"]
        Thick_base = shape_base["thickness"] 
        Twist_base = shape_base["twist"]  
        list_Chord = []
        list_Thick_abs = []
        list_Twist = [] 
        list_Thickness = []
        radius = []
        all_list = []
        for (chord, thick, twist) in zip(Chord_base, Thick_base, Twist_base):
            radius.append(chord[0])
            list_Chord.append(chord[1])
            list_Thickness.append(thick[1])
            list_Twist.append(twist[1])
            list_Thick_abs.append((thick[1])*float(chord[1]))
        #with col1:
        radii = st.text_input("change  from start,stop,sections along blade radical","np.linspace(0,7,20).tolist() + np.linspace(7.4,121, 120).tolist()")
            #n_sections = st.number_input("sections of blade",value=len(radius),help="how many divided in blade length, eg:80")
        with col2:    
            polate_method = st.selectbox("select spline method",("Linear", "Kochanek", "Cardina" , "SmoothCurve"))
        with col3:
            spspan = st.number_input("input spspan number",value=config["planform"]["npspan"],help="span wise mesh number of sections")
        with col4:
            spchord = st.number_input("input spcord number",value=config["planform"]["npchord"],help="chord wise mesh number of sections")
        #pl1,pl2 = st.columns(2)
        #config["planform"]["n_sections"] = n_sections
        config["mesh"]["radii"] = radii
        config["planform"]["npspan"] = spspan
        config["planform"]["npchord"] = spchord 
        #st.write(config)
        #time.sleep(30)
        configfile = os.path.join(run_base, "fem", "s123_lam.yml")
        #    dumpfile.write(yaml.dump(config))     
        y = YAML()
        y.dump(config,open(configfile, "w"))

        with col1:
            if st.button("create 3D mesh shell"):
                this_cmd = "geomimport"
                os.system("./run_make.sh %s" % (this_cmd))
                this_cmd ="mesh"
                os.system("./run_make.sh %s" % (this_cmd))   
                time.sleep(5)
        #3D with stpyvista
        # Load your .vtk file
        mesh = pv.read(os.path.join(run_base, "fem","temp_b3ps/test_blade.vtp"))
        ## Initialize a plotter object
        plotter = pv.Plotter(window_size=[1500,1000])
        x, y, z = mesh.cell_centers().points.T
        #x,y,z = mesh.cell_left().points.T
        mesh["My scalar"] = z
        ## Add mesh to the plotter
        plotter.add_mesh(
            mesh,
            scalars="My scalar",
            cmap="prism",
            show_edges=True,
            edge_color="#001100",
            ambient=0.01,)
        ## Final touches
        plotter.view_isometric()
        plotter.background_color = 'white'
        ## Send to streamlit
        stpyvista(plotter)
        st.image(os.path.join(run_base, "fem","temp_b3ps/test_blade.png"))
        
        #with pl2:


    elif page == "Lamplan":
        st.markdown(""":blue[可以上传你的铺层文件和实时修改，修改后点击右上角下载]""")
        cl1,cl2,cl3 = st.columns(3)
        with cl1:
            up_csv_file = st.file_uploader("upload a laminate plan .csv file ",type=["csv"],help="customer .csv file to upoload here") 
        
        if up_csv_file is None:
            df = pd.read_csv(os.path.join(run_base, "fem","lamplan_123.csv"))
            st.data_editor(df, key="lamplan_default")
        if up_csv_file is not None:
            df = pd.read_csv(up_csv_file)
            st.data_editor(df, key="lamplan_uploaded")
        st.write("please click upper top to download when you are edit this table")  
        if st.button("make lamplan"):
            this_cmd = "lamplan"
            os.system("./run_make.sh %s" % (this_cmd))
    elif page == "Material":

        st.markdown(''':blue[---材料特性一般很少变化，这里可以修改后] ''')
        if st.button("make matdb"):
            this_cmd = "matdb"
            os.system("./run_make.sh %s" % (this_cmd))  
        with open(os.path.join(run_base, "fem", "materials_v9.yml"), 'r') as file:
            data = yaml.safe_load(file)
            st.write(data)

    elif page == "AIReport":
        al1,al2,al3,al4 = st.columns(4)
        #readn yaml file and shows the deformation of a blade    
        with al1:    
            if  st.button("createReport"):
                this_cmd = "build"
                os.system("./run_create_report.sh  %s" % (this_cmd))
                st.write("---createing report now by grok3---")
                time.sleep(5)
                st.write("done for AI Report! ")
        with al2:
            if st.button("downloadReport--Structure Stability"):
                d_path = "../stab2/AIReport_stab.markdown"
                download_file(d_path,"AIReport_stab.markdown")

        with al3:
            if st.button("downloadReport--Structure Dumping"):
                d_path = "../stab2/AIReport_dumping.markdown"
                download_file(d_path,"AIReport.markdown")


    elif page == "Airfoils":
        st.divider()
        m1,m2,m3 = st.columns(3)
        with m2:
            st.write(data["planform"])
        with m1:
            st.write(data["aero"]["airfoils"])
            st.write(data["aero"]["fem"])  
        with m3:
            st.write(data["laminates"]["slabs"])
            st.write(data["mesh"]["webs"])
    elif page == "Stiffness":
        st.markdown(''':blue[---确定前面的菜单都有选择，然后点击蓝色按钮] ''')
        t1,t2,t3,t4 = st.columns(4)
        with t2:
            if st.button("Convert Hawcstab2"):
                st.markdown(''':blue[---Starting to  Convert OK to Hawcstab2 file format] ''')
                #os.system("./run_all.sh %s" %("step04"))
                for i in range(4):
                    time.sleep(1)                        
                    st.write(f"⏳ 已过去 {i+1} 秒")
                st.write(''':green[------Convert done] ''')
                
                            
        with t1:
            if st.button("Make Stiffness"):
                os.system("./run_stiffness.sh")
                st.markdown('''**:blue[Starting do ANBA Solver, might need more than 20 mins, depending on how many sections]**''')
                with st.empty():
                    for i in range(1200):
                        f = open(os.path.join(run_base,"fem","check_status.log")) 
                        new = f.read()
                        #st.write(line)
                        if new == "anba4_done":
                            f.close()
                            break
                        #f.close()
                        time.sleep(1)
                        n_i = i + 2
                        st.write(f"⏳ 已过去 {n_i} 秒")
                    st.markdown('''**:green[------ANBA4 done]**''')
            
            with t3:
                st.write('''**:blue[Stiffness 6x6 by sections]**''')
                foils_dir = os.path.join(run_base,'fem','stiffness')
                air_file_list = []
                for file in os.listdir(foils_dir):
                    air_file_list.append(file)
                data_json = {}
                list_inputs_dir = os.path.join(run_base,"fem/stiffness")
                #list_files = os.listdir(list_inputs_dir)
                file_ch = st.selectbox("pick a matrix of 6x6", (air_file_list))
                already__run =  True
                if file_ch is not None and already__run:
                    ext_file = os.path.join(list_inputs_dir,file_ch)
                    #st.write(ext_file)
                    with open(ext_file,'r', encoding=u'utf-8', errors='ignore') as fr:
                        data_json = json.load(fr)
                    #data_json = pd.read_json(ext_file)
                    st.write(data_json['stiffness']) 
                else:
                                
                    ext_file = os.path.join(run_base,'fem','stiffness','msec_60000.xdmf.json')
                    with open(ext_file,'r', encoding=u'utf-8', errors='ignore') as fr:
                        data_json = json.load(fr)
                    st.write(data_json['stiffness'])
    if page == "Stability":
        #run shell and dispay result assume .htc file
        htc_file = st.file_uploader("upload a .htc file",type=["htc"])
        if htc_file is not None:
            my_htc_file = htc_file
        else:
            my_htc_file = "15MW_252_Blade_D_directdrive_hs2_locked_case_op1.htc"
        if st.button("run stability analysis"):
          os.system("../stb2/run_stab2.sh %s " % (my_htc_file))
        
        st.markdown(''':blue[---稳定性分析分叶片和风机，图一是有问题的，图二和图三是本次实例计算结果] ''')
        list_inputs_dir = os.path.join(run_base,"stab2")
        st.image(os.path.join(list_inputs_dir,"campbell_analysis.png"), width=500, use_column_width=True)
        st.divider()
        st.image(os.path.join(list_inputs_dir,"campbell_structural.png"), width=500, use_column_width=True)
        st.divider()
        st.image(os.path.join(run_base,"stab2","damping_structural.png"), width=500, use_column_width=True)
        
if __name__=="__main__":
    css = """
        table 
        {
        border-collapse: collapse;
        }
        th
        {
        color: #ffffff;
        background-color: #000000;
        }
        td
        {
        background-color: #cccccc;
        }
        table, th, td
        {
        font-family:Arial, Helvetica, sans-serif;
        border: 1px solid black;
        text-align: right;
        }
    """
    main()

