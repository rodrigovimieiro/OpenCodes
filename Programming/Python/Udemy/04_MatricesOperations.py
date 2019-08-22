"""
Author: Rodrigo de Barros Vimieiro
Date: August, 2019
rodrigo.vimieiro@gmail.com
=========================================================================
"""
import numpy as np


#%%
a = np.array([[1,2],[3,4]]) # Matrix

invA = np.linalg.inv(a) # A inverse

print(invA.dot(a))

detA = np.linalg.det(a) # A determinant

print(detA)

digA = np.diag(a) # A diagonal

print(digA)

traceA = np.trace(a) # Trace of A

print(traceA)

a = np.random.random((100,3))

covA = np.cov(a.T) # Covariance matrix

print(covA.shape)


eigenvalues, eigenvectors = np.linalg.eig(covA) # Eigenvalues and Eigenvectors

print(eigenvalues)
print(eigenvectors)









