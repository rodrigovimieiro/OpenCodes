"""
Author: Rodrigo de Barros Vimieiro
Date: August, 2019
rodrigo.vimieiro@gmail.com
=========================================================================
"""
from scipy.stats import norm
import numpy as np
import matplotlib.pyplot as plt


#%%

print(norm.pdf(0))

mean = 5
std = 10

print(norm.pdf(0,mean,std))

array = np.random.randn(1000)

plt.figure(1)
plt.scatter(array,norm.pdf(array))

plt.figure(2)
plt.scatter(array,norm.logpdf(array))

plt.figure(3)
plt.scatter(array,norm.cdf(array))

plt.figure(4)
plt.scatter(array,norm.logcdf(array))





