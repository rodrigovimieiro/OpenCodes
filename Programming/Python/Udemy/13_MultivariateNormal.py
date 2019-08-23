"""
Author: Rodrigo de Barros Vimieiro
Date: August, 2019
rodrigo.vimieiro@gmail.com
=========================================================================
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal as mvn


#%%

covM = np.array([[1,.8],[.8,3]])

mu = np.array([0,2])

r = mvn.rvs(mean=mu,cov=covM,size=1000)

plt.figure(1)
plt.axis('equal')
plt.scatter(r[:,0],r[:,1])


r = np.random.multivariate_normal(mean=mu,cov=covM,size=1000)

plt.figure(2)
plt.axis('equal')
plt.scatter(r[:,0],r[:,1])



