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

x_line = np.linspace(0,100,100)
y_line = 2*x_line + 1

plt.scatter(x,y,color='red')
plt.plot(x_line,y_line,color='green')
 

