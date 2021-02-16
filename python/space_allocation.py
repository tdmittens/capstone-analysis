# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 00:19:30 2021

@author: Tarandeep
"""

#from docplex.cp.model import *
#
#mdl = CpoModel()

import cplex
from doopl.factory import create_opl_model
import pandas as pd


# data import
specs = pd.read_excel(
    r'D:\OneDrive - Ryerson University\[School]\4X (Capstone)\210209 New Required Files for Software\Capstone_SKUs_V2_attempt_5_1_hour.xlsx')

flow = specs['fi'].tolist()
volume = specs['Volume/ pallet (cu ft)'].tolist()

n = 1541


with create_opl_model(model="Space Allocation.mod") as opl:
    opl.set_input("flow", flow)
    opl.set_input("volume1", flow)
    opl.run()
    report = opl.report



