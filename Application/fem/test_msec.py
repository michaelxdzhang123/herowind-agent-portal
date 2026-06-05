## got data set from .csv and make them stream show
## this is for structure analysis
import streamlit as st
from os import getcwd,path
import numpy as np
import pickle
fn = "./temp_b3ps/plybook.pck"
fn = "./temp_b3ps/test_blade.pck"
with open(fn, 'rb') as f:
    x = pickle.load(f)
    print(x)
