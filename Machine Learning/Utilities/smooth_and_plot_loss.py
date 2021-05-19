#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  7 09:11:08 2021

@author: Rodrigo
"""

import pandas as pd
import matplotlib.pyplot as plt

from typing import List

#%%
# Ref: https://stackoverflow.com/a/49357445/8682939
def smooth(scalars: List[float], weight: float) -> List[float]:  # Weight between 0 and 1
    last = scalars[0]  # First value in the plot (first timestep)
    smoothed = list()
    for point in scalars:
        smoothed_val = last * weight + (1 - weight) * point  # Calculate smoothed value
        smoothed.append(smoothed_val)                        # Save it
        last = smoothed_val                                  # Anchor the last smoothed value

    return smoothed

#%%

red_factors = [50, 25, 15]
red_colors = ['r','g','b']
ema_weight = 0.99

#%%
for idX, red_factor in enumerate(red_factors):
    
    df = pd.read_csv('{}.csv'.format(red_factor))  
    df = df[df['Value'] < 86e-3]
    x = df['Step']
    y = df['Value']
    y_smooth = smooth(list(y), ema_weight)
    plt.plot(list(x), y_smooth, label=red_factor, color=red_colors[idX])
    plt.plot(list(x), y, color=red_colors[idX], alpha=0.4)
    
    
plt.legend()
plt.title("Loss")
