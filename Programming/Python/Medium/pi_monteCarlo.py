#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 11:02:04 2020

@author: Rodrigo
"""

# Ref: https://towardsdatascience.com/an-overview-of-monte-carlo-methods-675384eb1694

import numpy as np
import matplotlib.pyplot as plt

n = 100000

# Generate random coords
x = np.random.rand(n,2)

# Is this point inside a circunference with radius 1?
inside = x[ np.sqrt(x[:,0]**2 + x[:,1]**2) < 1]

# pi/4 = len(inside) / len(x)
piEstimate = 4*len(inside) / len(x)

print('Estimate of pi: {}'.format(piEstimate))

plt.figure(figsize=(8,8))
plt.scatter(x[:,0],x[:,1], s=.5, c='blue')
plt.scatter(inside[:,0],inside[:,1], s=.5, c='red')