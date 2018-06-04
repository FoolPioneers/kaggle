#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 21:03:45 2018

@author: long.li
utility function for variable calculate
"""
import pandas as pd
import numpy as np
import itertools
from functools import reduce

def varcal_cal_atom(dfgrp, f, idcol, group, reset_index = False):
    dftmp = dfgrp.aggregate(f).reset_index()
    
    varlst = list(set(dftmp.columns) - set([idcol] + group))
    
    print(idcol, group, varlst)
    dftmp = pd.pivot_table(dftmp, index=[idcol], columns = group, values=varlst)
    dftmp.columns = ['_'.join([str(s).strip() for s in col if s]) for col in dftmp.columns]
    
    return dftmp
    
def varcal_cal_methods(dfgrp, idcol, group, exrule, fmap):
    methods = list(fmap.keys())
    
    reslst = []
    for m in methods:
        # deal with exclude method
        
        dftmp = varcal_cal_atom(dfgrp, fmap[m], idcol, group)
        dftmp.columns = [m + c for c in dftmp.columns]
        
        reslst.append(dftmp)
        
    return reduce(lambda x, y: pd.merge(x, y, left_index=True, right_index=True), reslst)
    

def varcal_cal_dimidx(df, idcol, timecol, group, objmap = None, exrule = None, fmap = None):
    if fmap is None:
        fmap = {"S":sum, "A":np.mean, "C":sum, "L":min, "M":max, "T":np.std
                , "D":pd.Series.nunique}
    
    allgroup = group if timecol is None else [timecol] + group
    
    if objmap is not None:
        df.rename(columns = objmap, inplace = True)
        objlst = list(objmap.keys())
    else:
        objlst = list(set(df.columns) - set(allgroup))
        
    reslst = []
    for L in range(1, len(allgroup) + 1):
        for subgrp in itertools.combinations(allgroup, L):
            subgrp = list(subgrp)
            df_grp = df.groupby(subgrp + [idcol])[objlst]
            
            reslst.append(varcal_cal_methods(df_grp, idcol, subgrp, exrule, fmap))
            
    return reduce(lambda x, y: pd.merge(x, y, left_index=True, right_index=True), reslst).reset_index()
                


