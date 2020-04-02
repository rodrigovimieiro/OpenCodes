#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 10:29:41 2020

@author: Rodrigo
"""

import numpy as np
import matplotlib.pyplot as plt


randx = np.random.randn(100,100) # Uniformally distributed points from 0-1

# Ref: https://stackoverflow.com/a/5328669/8682939
hist, bins = np.histogram(randx, bins=50)
width = 0.7 * (bins[1] - bins[0])
center = (bins[:-1] + bins[1:]) / 2
plt.bar(center, hist, align='center', width=width)
plt.show()