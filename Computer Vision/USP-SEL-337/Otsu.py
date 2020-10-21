#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 10:18:03 2020

@author: Rodrigo
"""

import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

img = plt.imread("fig.tif")

#%%
hist = plt.hist(img.flatten(), bins=np.arange(0,257), range=(0, 255), density=True)
plt.xlabel('Nível de cinza')
plt.ylabel('Probabilidade')
plt.title('Histograma')
plt.text(76 + 1, hist[0][76], r"$p_{76}=$"+"{:.3f}".format(hist[0][76]))
plt.text(178 + 1, hist[0][178], r"$p_{178}=$"+"{:.3f}".format(hist[0][178]))
plt.savefig("Histograma.png")

#%%

hist = plt.hist(img.flatten(), bins=np.arange(0,257), range=(0, 255), density=True)
myAxis = plt.axis()
plt.text(76 + 1, hist[0][76], r"$p_{76}=$"+"{:.3f}".format(hist[0][76]))
plt.text(178 + 1, hist[0][178], r"$p_{178}=$"+"{:.3f}".format(hist[0][178]))
plt.plot(np.array((125,125)),np.array((myAxis[0],myAxis[-1])),'k--')
plt.text(130, .05, "T", fontsize=15)
plt.text(24, .5, "C1", fontsize=15)
plt.text(200, .5, "C2", fontsize=15)
plt.axis(myAxis)
plt.xlabel('Nível de cinza')
plt.ylabel('Probabilidade')
plt.title('Histograma')
plt.savefig("Histograma_2.png")