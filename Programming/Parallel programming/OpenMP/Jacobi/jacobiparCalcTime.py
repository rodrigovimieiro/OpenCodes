"""
Author: Rodrigo de Barros Vimieiro
Date: October, 2019
rodrigo.vimieiro@gmail.com
=========================================================================
"""
import pandas as pd
from os import walk



path = "output/"

txtFiles = []
for (_, _, filenames) in walk(path):
    for file in filenames:
        if file.endswith(".txt"):
            txtFiles.append(file)
    break

txtFiles.sort()



for f in txtFiles:
    tmp = f.split('_')[1]
    nThread = int(tmp.split('.')[0])

    data = pd.read_csv(path + f, sep=" ", header=None)

    timeValues = data.values[:,0]

    if(nThread == 1):

        meanSerialTime = timeValues.mean()

        print("\n *** Time for executions with %d thread ***" % nThread)
        print("Mean: %f" % meanSerialTime)
        print("Std: %f" % timeValues.std())
        print("Iterations: %d" % data.values[0,1])
        
    else:
        
        meanParallelTime = timeValues.mean()
        speedup = meanSerialTime/meanParallelTime
        efficiency = speedup/nThread
        
        print("\n *** Time for executions with %d threads ***" % nThread)
        print("Mean: %f" % meanParallelTime)
        print("Std: %f" % timeValues.std())
        print("Speedup: %f" % speedup)
        print("Efficiency: %f" % efficiency)
        print("Iterations: %d" % data.values[0,1])




#%%
