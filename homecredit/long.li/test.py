#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 21:02:44 2018

@author: long.li


"""

from utility import utility

import numpy as np
import pandas as pd

recordNum = 100
n = 2
varNum = 2
keys = ['ID%04d' %i for i in range(int(recordNum/n))] * n
varlst = ['x%04d' %i for i in range(varNum)]

dsDict1 = {k:np.random.choice(["v" + k[-1] + v for v in ["a","b"]], recordNum) for k in varlst}

df = pd.DataFrame(dict(dsDict1, key = keys))
df[['v1', 'v2']] = pd.DataFrame([[1]*2], index=df.index)

idcol = "key"
group = varlst
f = sum

dfgrp = df.groupby([idcol] + group)

dfgrp.obj.columns
dfgrp[["v1", "v2"]].sum()

utility.varcal_cal_atom(dfgrp[["v1"]], sum, idcol, group)

# 获取grouped dataframe列名——原始的dataframe
df.groupby(group)[varlst].obj.columns
dfres = utility.varcal_cal_b1(dfgrp, f, idcol, group)



from utility import utility

import numpy as np
import pandas as pd

recordNum = 100
n = 2
varNum = 2
keys = ['ID%04d' %i for i in range(int(recordNum/n))] * n
varlst = ['x%04d' %i for i in range(varNum)]

dsDict1 = {k:np.random.choice(["v" + k[-1] + v for v in ["a","b"]], recordNum) for k in varlst}

df = pd.DataFrame(dict(dsDict1, key = keys))
df[['v1', 'v2']] = pd.DataFrame([[1]*2], index=df.index)

idcol = "key"
group = varlst
exrult = [{'cols':'x0000','exmethod':None,'conmethod':None,'exobj':"v1",'conobj':None}
, {'cols':None,'exmethod':None,'conmethod':'D','exobj':None,'conobj':"v1"}]

mmap = {"S":sum, "D":pd.Series.nunique}

dft = utility.varcal_cal_dimidx(df, idcol, None, group, None, exrult, mmap)




