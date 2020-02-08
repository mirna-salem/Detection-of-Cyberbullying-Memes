# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 13:58:11 2019

@author: Mirna
"""

import pandas as pd
import re

df = pd.read_csv('varmichelle_.csv',  encoding='latin-1')
clean_text = lambda x: re.sub('[^A-Za-z0-9 ]+', '', x)
df['tweet'] = df['tweet'].apply(clean_text)

df.to_csv('Clean_Varmichelle.csv', mode='a',header = False)