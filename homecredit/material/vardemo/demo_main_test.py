# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 12:00:04 2017

@author: long.li
"""
import pandas as pd
import numpy as np
import sys
from configpy import demo_filter_func
from configpy import demo_varname
import time
# read data part
dfBaseData = pd.read_csv('test/basic_test_data.txt', sep = '\t')


def demoCal(df):
    # generate conditions
    dim = ['cat1','cat2','cat3','cat4']
    catAll = np.array(df[dim])
    colLoc = dict(zip(dim, range(len(dim))))
    allCondition = {
        'condition1a':catAll[:,colLoc['cat1']] == 'a'
        ,'condition1b':catAll[:,colLoc['cat1']] == 'b'
        ,'condition1c':catAll[:,colLoc['cat1']] == 'c'
        ,'condition1d':catAll[:,colLoc['cat1']] == 'd'
        ,'condition2p':catAll[:,colLoc['cat2']] == 'p'
        ,'condition2q':catAll[:,colLoc['cat2']] == 'q'
        ,'condition2m':catAll[:,colLoc['cat2']] == 'm'
        ,'condition2n':catAll[:,colLoc['cat2']] == 'n'
        ,'condition3p':catAll[:,colLoc['cat3']] == 'p'
        ,'condition3q':catAll[:,colLoc['cat3']] == 'q'
        ,'condition3m':catAll[:,colLoc['cat3']] == 'm'
        ,'condition3n':catAll[:,colLoc['cat3']] == 'n'
        ,'condition4p':catAll[:,colLoc['cat4']] == 'p'
        ,'condition4q':catAll[:,colLoc['cat4']] == 'q'
        ,'condition4m':catAll[:,colLoc['cat4']] == 'm'
        ,'condition4n':catAll[:,colLoc['cat4']] == 'n'
    }
    
    # record filter
    numObj = {
        'obj1':np.array(dfBaseData['obj1'])
        ,'obj2':np.array(dfBaseData['obj2'])
    }
    arrayNumFiltered = demo_filter_func.demoFilterFunc(allCondition, numObj)
    # append id
    arrayNumFiltered['id'] = dfBaseData.id
    # aggregate
    dfGrouped = pd.DataFrame(arrayNumFiltered).groupby(['id'])
    # sum
    vars2Agg = [varname for varname in demo_varname.demo_varname if varname[2] == 's']
    dfAgged = dfGrouped[vars2Agg].sum()
    vars2Agg = [varname for varname in demo_varname.demo_varname if varname[2] == 'a']
    dfAgged = dfGrouped[vars2Agg].mean()
    vars2Agg = [varname for varname in demo_varname.demo_varname if varname[2] == 'm']
    dfAgged = dfGrouped[vars2Agg].max()
    vars2Agg = [varname for varname in demo_varname.demo_varname if varname[2] == 'v']
    dfAgged = dfGrouped[vars2Agg].std()

t0 = time.time()
demoCal(dfBaseData)
t1 = time.time()
print(t1-t0)