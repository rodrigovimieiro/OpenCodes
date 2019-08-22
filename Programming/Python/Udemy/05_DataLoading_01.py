"""
Author: Rodrigo de Barros Vimieiro
Date: August, 2019
rodrigo.vimieiro@gmail.com
=========================================================================
"""
import numpy as np
import pandas as pd


#%% 

# CSV = comma separated values

# Loading by brute force
x = []

for line in open("data/data_2d.csv"):
    row = line.split(',')
    sample  = list(map(float,row))
    x.append(sample)

x = np.array(x)

print(x)

# Loading by Pandas

x = pd.read_csv("data/data_2d.csv",header=None)

print(x.head(20))

print(x.iloc[0,0])  # get the first element
print(x.loc[0])     # get the first row of elements
print(x[0])         # get the first column of elements

print(x[x[0] < 5])  # Find element which are less than 0

xM = x.values       # Convert ir to numpy array




