"""
Author: Rodrigo de Barros Vimieiro
Date: August, 2019
rodrigo.vimieiro@gmail.com
=========================================================================
"""
import numpy as np


#%%
A = np.array([[1,1],[1.5,4]]) # Matrix

b = np.array([2200,5050])

x = np.linalg.inv(A).dot(b)

print(x)

print(A.dot(x))

x = np.linalg.solve(A,b)

print(x)













