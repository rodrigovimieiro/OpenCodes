"""
Author: Rodrigo de Barros Vimieiro
Date: October, 2019
rodrigo.vimieiro@gmail.com
=========================================================================
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

#%%
path_time = "output/"

txtFiles = []
for (_, _, filenames) in os.walk(path_time):
    for file in filenames:
        if file.endswith(".txt"):
            txtFiles.append(file)
    break

txtFiles.sort()



#%%
nThreadsParallel = len(txtFiles)-1

meanParallelTime = np.zeros(nThreadsParallel)
stdParallelTime = np.zeros(nThreadsParallel)
speedup = np.zeros(nThreadsParallel)
efficiency = np.zeros(nThreadsParallel)
iterParallelTime = np.zeros(nThreadsParallel)

nThreadVector = np.zeros(nThreadsParallel+1)


#%%
for count, f in enumerate(txtFiles,-1):
    
    tmp = f.split('_')[1]
    nThread = int(tmp.split('.')[0])
    
    nThreadVector[count+1] = nThread

    data = pd.read_csv(path_time + f, sep=" ", header=None)

    timeValues = data.values[:,0]

    if(nThread == 1):

        meanSerialTime = timeValues.mean()
        stdSerialTime = timeValues.std()
        iterSerialTime = data.values[0,1]

        print("\n *** Time for executions with %d thread ***" % nThread)
        print("Mean: %f" % meanSerialTime)
        print("Std: %f" % stdSerialTime)
        print("Iterations: %d" % iterSerialTime)
        
    else:
        
        meanParallelTime[count] = timeValues.mean()
        stdParallelTime[count] = timeValues.std()
        speedup[count] = meanSerialTime/meanParallelTime[count]
        efficiency[count] = speedup[count]/nThread
        iterParallelTime[count] = data.values[0,1]
        
        print("\n *** Time for executions with %d threads ***" % nThread)
        print("Mean: %f" % meanParallelTime[count])
        print("Std: %f" % stdParallelTime[count] )
        print("Speedup: %f" % speedup[count])
        print("Efficiency: %f" % efficiency[count])
        print("Iterations: %d" % iterParallelTime[count])



#%%
path_figure = 'figures'
path_csv = 'table'

if not os.path.exists(path_figure):
    os.makedirs(path_figure)
    
if not os.path.exists(path_csv):
    os.makedirs(path_csv)

meanTime = np.concatenate([np.array([meanSerialTime]),meanParallelTime])
stdTime = np.concatenate([np.array([stdSerialTime]),stdParallelTime])

#%%
plt.figure()
plt.stem(nThreadVector,meanTime,use_line_collection=True)
plt.xlabel('Thread number')
plt.ylabel('Mean execution time (s)')
plt.savefig(path_figure + '/Mean_execution_time.png', dpi=150, transparent=False, bbox_inches='tight')

plt.figure()
plt.stem(nThreadVector,stdTime,use_line_collection=True)
plt.xlabel('Thread number')
plt.ylabel('Standard deviation execution time (s)')
plt.savefig(path_figure + '/Std_execution_time.png', dpi=150, transparent=False, bbox_inches='tight')

plt.figure()
plt.stem(nThreadVector[1:],speedup,use_line_collection=True)
plt.xlabel('Thread number')
plt.ylabel('Speedup')
plt.savefig(path_figure + '/Speedup.png', dpi=150, transparent=False, bbox_inches='tight')

plt.figure()
plt.stem(nThreadVector[1:],efficiency,use_line_collection=True)
plt.xlabel('Thread number')
plt.ylabel('Efficiency')
plt.savefig(path_figure + '/Efficiency.png', dpi=150, transparent=False, bbox_inches='tight')

#%%

np.savetxt(path_csv + "/meanTime.csv", np.stack((nThreadVector,meanTime),axis=1), fmt='%2.2e')
np.savetxt(path_csv + "/stdTime.csv", np.stack((nThreadVector,stdTime),axis=1), fmt='%2.2e')
np.savetxt(path_csv + "/speedup.csv", np.stack((nThreadVector[1:],speedup),axis=1), fmt='%2.2e')
np.savetxt(path_csv + "/efficiency.csv", np.stack((nThreadVector[1:],efficiency),axis=1), fmt='%2.2e')


#%%
