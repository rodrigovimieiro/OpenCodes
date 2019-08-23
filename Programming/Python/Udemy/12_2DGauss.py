"""
Author: Rodrigo de Barros Vimieiro
Date: August, 2019
rodrigo.vimieiro@gmail.com
=========================================================================
"""
import numpy as np
import matplotlib.pyplot as plt


#%%

mean = [5,5]
std = [1,10]

array = np.random.randn(10000,2)

array[:,0] = std[0] * array[:,0] + mean[0]
array[:,1] = std[1] * array[:,1] + mean[1]

plt.figure(1)
plt.axis('equal')
plt.scatter(array[:,0],array[:,1])





