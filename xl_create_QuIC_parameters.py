# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 03:16:41 2017

@author: Syafri Bahar
"""
##%
def read_as_plain_table(path_file): 
    from scipy.io  import loadmat
    import pandas as pd 
    d=loadmat(path_file,squeeze_me=True)
    
    data={k:v for k,v in d.items() if not (('__cols' in k) or k.endswith('__'))}
         
    return pd.DataFrame(data)

#%% 
def process(): 
#%%
    import numpy as np
    import pandas as pd
    import os 
    import xlwings as xw 
#    wb=xw.Book.caller() 
    sh_mapping=xw.sheets('mapping')
    sh_db=xw.sheets('Dashboard')
    driver_source=sh_db.range('driver_source').value
    
    t=read_as_plain_table(driver_source+'.mat')
    t['value']=np.real(t['value'])
    l=t.loc[:,['DriverID']].drop_duplicates().set_index([ 'DriverID' ])
    r=t.pivot(index='DriverID',columns='parameter',values='value')
    t=l.merge(r,left_index=True,right_index=True)
    tdriver=t.copy() 
    
    # series of checks     
#    all(tmapping['DriverID'].isin(tdriver['DriverID']))
    
    t=sh_mapping.range('a1').options(pd.DataFrame,expand='table').value
    t=t.merge(tdriver,how='left',right_index=True,left_on='DriverID')
    t=t.reset_index()    
    
    def get_curve_type(rf):
        if rf in ('FinAA','GovBBB','IndBBB'): 
            return 'CS'
        elif rf in ('GlobalEquityFactor'):
            return 'EQ'
        else:
            second=rf.split('.')[1]
            third=rf.split('.')[2]
            
            if second=='Yield':
                return 'IR'
            elif second=='Exchange':
                return 'FX'
            elif second in ['EquityIndex','Equity']: 
                return 'EQ'
            elif second=='ParCreditSpread': 
                return 'CS'
            elif second=='Commodity' or third=='Com':
                return 'Com'
        
    t['CurveType']=t['RiskFactorID'].apply(lambda x: get_curve_type(x) )

    
    
    t['g1Ord1']=0
    t['g1Ord2']=0
    t['g1Transform']=t['model_id'].apply(lambda x: 
                    'LogNormShift'  if x=='EV-MR'   else 
                    'LogNorm'       if x=='GBM'     else 
                    'Norm'          if x=='CS1'     else 
                    'LogNorm'       if x=='CS2'     else 'ERROR' 
                    )
    t['g1MeanFunc']=t['model_id'].apply(lambda x: 
                'StandardLogNormMR' if x=='EV-MR'   else 
                'LogNormDrift'      if x=='GBM'     else  
                'NormMR'            if x=='CS1'     else 
                'LogNormMR'         if x=='CS2'     else 'ERROR'
                )
        
    def calculate_m(model,a,b): 
        if model=='EV-MR':
            return np.exp(-b/a)
        elif model=='CS1': 
            return 9999 
        else :
            return 0
        
    t['g1Param_m']=t.apply(lambda x: 
                calculate_m(x['model_id'],x['a'],x['b'])
                ,axis=1)

        
    t['g1Param_m']=t.apply(lambda x: 
                calculate_m(x['model_id'],x['a'],x['b'])
                ,axis=1)
        
    def calculate_d(model,a): 
        if model=='EV-MR':
            return -a
        elif model=='CS1': 
            return 9999 
        else :
            return 0
        
    t['g1Param_d']=t.apply(lambda x: 
                calculate_m(x['model_id'],x['a'],x['b'])
                ,axis=1)

    t['g1PerAnnumRF']=365


    t['g1Param_s2']=0
    t['g1Param_s3']=0
    t['g1Floor']='-infinity'
    t['g1IdxRFs']=np.cumsum(np.ones_like(t.index))
    
    def calculate_beta(CurveType,beta):
        if CurveType in ['CS','EQ']: 
            return beta
        elif CurveType in ['IR','FX','Com']:
            return 1
                
    
    t['g1Betas']=t.apply(lambda x: calculate_beta(x['CurveType'],x['beta']),axis=1)

    qm_rf=t.copy()


#    xw.view(tdriver,xw.sheets('data'))
    xw.view(qm_rf,xw.sheets('Qm_risk_factor'))
    
    
    
    