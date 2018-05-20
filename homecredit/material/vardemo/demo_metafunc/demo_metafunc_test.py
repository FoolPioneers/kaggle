# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 12:00:04 2017

@author: long.li
"""
import pandas as pd
import numpy as np
from configpy import demo_varname

funcTemplate = """
import numpy as np

def demoFilterFunc(%(condition)s, %(numObj)s):
%(indent)sreturn %(allExp)s
"""

conditionArrayName = 'conditionAll'
objName = 'objNum'
indent = '    '
varList = demo_varname.demo_varname
outputName = 'demo_filter_func.py'
#returnArray = 'filterArray'

# need add dict desc for objType, use different Object array name for different type of calculate object
valueTrue = {'o':'obj1', 'p':'obj2'}
valueFalse = {'o':'np.nan', 'p':'np.nan'}
# filter code generator
def getVarExp(varName, conditionArrayName, objName, valueTrue, valueFalse):
    conditionList = []
    if varName[4] != 'w':
        conditionList.append('condition1' + varName[4])
    if varName[5] != 'w':
        conditionList.append('condition2' + varName[5])
    if varName[6] != 'w':
        conditionList.append('condition3' + varName[6])
    if varName[7] != 'w':
        conditionList.append('condition4' + varName[7])
        
    if len(conditionList) == 0:
        return '"%s":%s["%s"]' %(varName, objName, valueTrue[varName[3]])
    
    modifiedCondition = ['%s["%s"]' %(conditionArrayName, condition) for condition in conditionList]
    finalCondition = '&'.join(modifiedCondition)
    return '"%s":np.where(%s, %s["%s"], %s)' %(varName, finalCondition, objName, valueTrue[varName[3]], valueFalse[varName[3]])

# function test
# getVarExp('n_aocmmm', 'conditionAll', 'objNum', valueTrue, valueFalse)
# getVarExp('n_aowwww', 'conditionAll', 'objNum', valueTrue, valueFalse)
#varList = ['n_aocmmm', 'n_aowwww']
varExpLst = [getVarExp(varName, conditionArrayName, objName, valueTrue, valueFalse) for varName in varList]
coreExp = ('\n' + indent + ',').join(varExpLst)
# return dict
allExp = '{%s}' %(coreExp)
generatedFuncCode = funcTemplate %dict(condition = conditionArrayName, numObj = objName, indent = indent, allExp = allExp)

with open('../configpy/'+outputName, 'w+') as f:
    f.write(generatedFuncCode)
# test part
# format test
#'''
#%(a)d + %(b)d = %(c)d
#'''%(dict(a=3,b=4,c=5))
#
## numpy aggregate test
#x = np.array([0,2,np.nan,5])
#
#if True:
#    a = [3
#,4
#,6]

