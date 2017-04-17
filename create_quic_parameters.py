# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 23:23:44 2017

@author: BaharS
"""

#%% 
#import os
#os.chdir(r'\\Eu.rabonet.com\fs\RISK\RMM\Financial Markets\3. Counterparty Credit Risk\04. Other\Review 2016\Syafri\project\projects')

#import sys 
#sys.path.append(r'..\libraries\python')
#
#import imp 
#imp.reload(ccr)

#%%
#stoc_file=r'..\parameters\historical_stochastic_file\2015\Input Parameters QuIC DD 20151012.csv'

import imp 
imp.reload(ccr)
import ccr 

stoc_file=r'Input Parameters QuIC DD 20151012.csv'

ccr.extract_QuIC_parameters(stoc_file)
#%% 

def read_as_plain_table(path_file): 
    from scipy.io  import loadmat
    import pandas as pd 
    d=loadmat(path_file,squeeze_me=True)
    
    data={k:v for k,v in d.items() if not (('__cols' in k) or k.endswith('__'))}
         
    return pd.DataFrame(data)


#%% 
driver_source=r'Pmtr_combined_non_shifted_2016'
list_rf=ccr.csv2dict(r'mapping.csv')['risk_factor_mapping']


t=read_as_plain_table(driver_source)

t['model_id']=t['parameter_name'].apply( lambda x : 
    'EV-MR' if x=='Pmtr_IR_2016_EVMR_IR2016_6M_20170412' else
    'GBM'   if x=='Pmtr_FX_2016_GBM_FX2016_20170412' else 
    'GBM'   if x=='Pmtr_CS_2016_CS2016_20170412' else 
    'GBM'   if x=='Pmtr_EQ_2016_EQ2016_20170412' else 
    'CS1'   if x=='Pmtr_Com_2016_GBM_Com2016_20170412' else ''    
    )
#!! just workaround, this should happen in the matlab calibration code 

l=t.loc[:,['DriverID','CurrencyID','CurveType' 'model_id']].drop_duplicates().set_index([ 'DriverID' ])
r=t.pivot(index='DriverID',columns='parameter',values='value')
t=l.merge(r,left_index=True,right_index=True)
tdriver=t.copy() 
#%%
t=list_rf
t=t.merge(tdriver,how='left',right_index=True,left_on='DriverID')
t['g1MeanFunc']=t['model_id'].apply(lambda x: 
                'StandardLogNormMR' if x=='EV-MR'   else 
                'LogNormDrift'      if x=='GBM'     else 
                )

t['g1Transform']=t['model_id'].apply(lambda x: 
                'LogNormShift' if x=='EV-MR'   else 
                'LogNorm'      if x=='GBM'     else 
                )
t['g1Param_m']=t['model_id'].apply(lambda x: 
                'LogNormShift' if x=='EV-MR'   else 
                'LogNorm'      if x=='GBM'     else 
                )


t.head() 
#%% 
df=pd.DataFrame({'x':['a','b','c']})
df['y']=df['x'].apply(lambda x: 'amanda' if x=='a' 
                                  else 'beta' if x=='b' 
                                  else 'cacing')

print(df)
