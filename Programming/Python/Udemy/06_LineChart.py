"""
Author: Rodrigo de Barros Vimieiro
Date: August, 2019
rodrigo.vimieiro@gmail.com
=========================================================================
"""
import numpy as np
import matplotlib.pyplot as plt


#%%
x = np.linspace(0,10,100)

y = np.sin(x)

plt.xlabel("Time")
plt.ylabel("Sin(x)")
plt.title("My cool chart")
plt.plot(x,y)
 

