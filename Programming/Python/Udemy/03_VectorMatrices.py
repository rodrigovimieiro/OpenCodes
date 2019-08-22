"""
Author: Rodrigo de Barros Vimieiro
Date: August, 2019
rodrigo.vimieiro@gmail.com
=========================================================================
"""
import numpy as np


#%%
a = np.array([[1,2],[3,4]]) # NP array

L = [[1,2],[3,4]]

print(a[0][0])

print(a[0,0])


print(a.T) # Transpose

#%%

b = np.zeros(10)

print(b)

b = np.zeros((10,10))

print(b)


b = np.ones(10)

print(b)

b = np.ones((10,10))

print(b)

b = np.random.random((10,10)) # Uniformly distributed from 0-1

print(b)

b = np.random.randn(10,10) # Gaussian distributed

print(b)

print(b.mean())

print(b.var())

#%%

