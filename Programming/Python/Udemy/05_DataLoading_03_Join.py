"""
Author: Rodrigo de Barros Vimieiro
Date: August, 2019
rodrigo.vimieiro@gmail.com
=========================================================================
"""
import pandas as pd

#%% 

# Loading by Pandas

t1 = pd.read_csv("data/table1.csv")

t2= pd.read_csv("data/table2.csv")


print(t1)

print(t2)


m = pd.merge(t1,t2,on='user_id')    # Merge the two tables

print(m)

m = t1.merge(t2,on='user_id')

print(m)    # Another way to merge the two tables