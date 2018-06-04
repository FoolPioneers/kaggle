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

dsDict1 = {k:np.random.choice(["a","b","c","d"], recordNum) for k in varlst}

df = pd.DataFrame(dict(dsDict1, key = keys))
df[['v1', 'v2']] = pd.DataFrame([[1]*2], index=df.index)

idcol = "key"
group = varlst
f = sum

dfgrp = df.groupby([idcol] + group)
dfres = utility.varcal_cal_b1(dfgrp, f, idcol, group)






from utility import utility

import numpy as np
import pandas as pd

recordNum = 100
n = 2
varNum = 2
keys = ['ID%04d' %i for i in range(int(recordNum/n))] * n
varlst = ['x%04d' %i for i in range(varNum)]

dsDict1 = {k:np.random.choice(["a","b","c","d"], recordNum) for k in varlst}

df = pd.DataFrame(dict(dsDict1, key = keys))
df[['v1', 'v2']] = pd.DataFrame([[1]*2], index=df.index)

idcol = "key"
group = varlst

dft = utility.varcal_cal_dimidx(df, idcol, None, group, None, None, fmap = None)




