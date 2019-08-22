"""
Author: Rodrigo de Barros Vimieiro
Date: August, 2019
rodrigo.vimieiro@gmail.com
=========================================================================
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


#%%
A = pd.read_csv('data/data_1d.csv', header=None).values

print(A)

x = A[:,0]
y = A[:,1]


plt.figure(1)
plt.hist(x)

randx = np.random.random(10000) # Uniformally distributed points from 0-1

plt.figure(2)
plt.hist(randx, bins=5)     # Plot histogram with 5 bins

x_line = np.linspace(0,100,100)
y_line = 2*x_line + 1 
residual = y - y_line;  # Subtract the mean values

plt.figure(3)
plt.hist(residual)


