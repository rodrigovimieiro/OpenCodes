"""
Author: Rodrigo de Barros Vimieiro
Date: August, 2019
rodrigo.vimieiro@gmail.com
=========================================================================
"""
import numpy as np
import matplotlib.pyplot as plt


#%%

# Generating the signal
x = np.linspace(0,100,10000)

y = np.sin(x) + np.sin(2*x) + np.sin(3*x)

plt.figure(1)
plt.title('Time domain')
plt.plot(x,y)

# FFT

Y = np.fft.fft(y)

Ymag = np.abs(Y)

plt.figure(2)
plt.title('Freq domain')
plt.plot(x,Ymag)
    

