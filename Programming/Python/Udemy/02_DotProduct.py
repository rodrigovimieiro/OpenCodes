"""
Author: Rodrigo de Barros Vimieiro
Date: August, 2019
rodrigo.vimieiro@gmail.com
=========================================================================
"""
import numpy as np

a = np.array([1,2,3]) # NP array
b = np.array([1,2,3]) # NP array

dot = 0

for na, nb in zip(a,b):
    dot += na*nb
    
print(dot)

print(a*b) # Elementwise multiplication

print(np.sum(a*b))

print(np.dot(a,b))

print(a.dot(b))

print(b.dot(a))


# L2 norm of A
aMag = np.linalg.norm(a)

