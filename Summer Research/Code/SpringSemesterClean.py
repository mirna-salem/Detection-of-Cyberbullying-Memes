# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 13:20:24 2019

@author: Mirna
"""

import pandas as pd
import re

df = pd.read_csv('FallSemesterData.csv',  encoding='latin-1')
clean_text = lambda x: re.sub('[^A-Za-z0-9 ]+', '', x)
df['Text'] = df['Text'].apply(clean_text)

df.to_csv('Clean_Fall_Semester.csv', mode='a',header = False)