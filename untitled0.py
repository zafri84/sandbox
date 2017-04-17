# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 06:29:31 2017

@author: Syafri Bahar
"""

#%% combined all the parameters 
parameter_names=['Pmtr_Com_2016_GBM_Com2016_20170412'
                 ,'Pmtr_CS_2016_CS2016_20170412'
                 ,'Pmtr_EQ_2016_EQ2016_20170412'
                 ,'Pmtr_FX_2016_GBM_FX2016_20170412'
                 ,'Pmtr_IR_2016_EVMR_IR2016_6M_20170412']


import pandas as pd 

tcomb=list([])

for pname in parameter_names: 
    t=read_as_plain_table(pname)
    tcomb.append(t)
tcomb=pd.concat(tcomb)
#%%
import numpy as np 

t=tcomb
t['value']=np.real(t['value'])

#t=t.loc[t['is_driver']==0 & t['DriverID'].str.contains('Asia').astype(bool),:]

xw.view(t,xw.sheets('Sheet1'))
#%% 
import ccr
ccr.extract_QuIC_parameters('Input Parameters QuIC ND 20151012.csv')