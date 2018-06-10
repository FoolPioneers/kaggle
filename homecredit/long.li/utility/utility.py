#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 21:03:45 2018

@author: long.li
utility function for variable calculation
"""
import pandas as pd
import numpy as np
import itertools
from functools import reduce

def varcal_cal_atom(dfgrp, f, idcol, group, reset_index = False):
    """
    计算给定分组下，某一聚合方式，选定的所有变量，并将行转列，且重命名
    dfgrp：grouped dataframe
    f: aggregate function
    idcol: transposed dataframe which column as the key
    group: cols for group,and for transpose
    """
    dftmp = dfgrp.aggregate(f).reset_index()
    
    varlst = list(set(dftmp.columns) - set([idcol] + group))
    
    print("loginfo group:", group)
    print("loginfo method:", f)
    print("loginfo objlist:", varlst)
    
    dftmp = pd.pivot_table(dftmp, index=[idcol], columns = group, values=varlst)
    dftmp.columns = ['_'.join([str(s).strip() for s in col if s]) for col in dftmp.columns]
    
    return dftmp

def varcal_cal_obj_exrule(exrule, m, objlst, group):
    """
    通过自定义的筛选规则, 过滤给定计算方式下，以及分组条件下，需要计算的计算对象
    样例[{'cols':'SK_DPD','exmethod':None,'conmethod':'D','exobj':None,'conobj':'CAC'}]
    """
    objs_by_incl = set()
    objs_by_ex = set(objlst)
    
    for rule in exrule:
        col = rule.get("cols")
        if(col is not None  and col not in group + [None]):
            continue
        if(rule["exmethod"] == None or m ==  rule["exmethod"]):
            if(rule["exobj"] == None and rule["exmethod"] != None):
                objs_by_ex = {}
            else:
                objs_by_ex = objs_by_ex - {rule["exobj"]}
                
        if(rule["conmethod"] == None or m ==  rule["conmethod"]):
            if rule["conobj"] != None:
                objs_by_incl = objs_by_incl.union({rule["conobj"]})
        
    res = objs_by_incl if len(objs_by_incl) >0 else objs_by_ex
    return list(res)
    
    
def varcal_cal_methods(dfgrp, idcol, group, exrule, fmap, objlst):
    """
    给定grouped dataframe 计算在一定变量过滤规则和计算方式下所有的变量
    """
    methods = list(fmap.keys())
    
    reslst = []
    for m in methods:
        # deal with exclude method
        obj_filtered = varcal_cal_obj_exrule(exrule, m, objlst, group)
        if len(obj_filtered) == 0:
            continue
        
        # print("subcolumns from grouped dataframe:", obj_filtered)
        dftmp = varcal_cal_atom(dfgrp[obj_filtered], fmap[m], idcol, group)
        dftmp.columns = [m + c for c in dftmp.columns]
        
        reslst.append(dftmp)
        
    return reduce(lambda x, y: pd.merge(x, y, left_index=True, right_index=True), reslst)
    

def varcal_cal_dimidx(df, idcol, timecol, group, objmap = None, exrule = None, fmap = None):
    """
    给定数据集 ，记录ID，分组列表，计算对象和计算方式。计算左右笛卡尔集情况下的变量，在给定变量过滤规则的情况下
    。基于维度指标法的变量计算衍生
    """
    if fmap is None:
        fmap = {"S":sum, "A":np.mean, "C":sum, "L":min, "M":max, "T":np.std
                , "D":pd.Series.nunique}
    
    allgroup = group if timecol is None else [timecol] + group
    
    if objmap is not None:
        df.rename(columns = objmap, inplace = True)
        objlst = list(objmap.keys())
    else:
        objlst = list(set(df.columns) - set(allgroup) - {idcol})
        
    reslst = []
    for L in range(1, len(allgroup) + 1):
        for subgrp in itertools.combinations(allgroup, L):
            subgrp = list(subgrp)
            df_grp = df.groupby(subgrp + [idcol])
            
            reslst.append(varcal_cal_methods(df_grp, idcol, subgrp, exrule, fmap, objlst))
            
    return reduce(lambda x, y: pd.merge(x, y, left_index=True, right_index=True), reslst).reset_index()
                

def varcal_udaf_lr(self, x, ys, group):
    df = self.copy()
    dfxy = df[ys].multiply(df[x], axis="index")
    dfxy[group] = df[group]
    dfxx = np.square(df[[x]])
    dfxx[group] = df[group]
    
    dfxy_avg = dfxy.groupby(group).mean()
    dfxx_avg = dfxx.groupby(group).mean()
    
    dfx_avg = df.groupby(group)[[x]].mean()
    dfy_avg = df.groupby(group)[ys].mean()
    
    dfx_avg_2 = np.square(dfx_avg)
    
    dfres = (dfxy_avg - dfy_avg.multiply(dfx_avg[x], axis="index")).multiply(1/(dfxx_avg - dfx_avg_2)[x], axis="index")
    return dfres
