"""
Author: Rodrigo de Barros Vimieiro
Date: August, 2019
rodrigo.vimieiro@gmail.com
=========================================================================
"""
import numpy as np

L = [1,2,3] # This is a list

A = np.array([1,2,3]) # NP array

for e in L:
    print(e)

for e in A:
    print(e)
  
# list operations
L.append(4)

print(2*L)

# Math operations

print(2*A)

print(np.sqrt(A))

print(np.log(A))

print(np.exp(A))