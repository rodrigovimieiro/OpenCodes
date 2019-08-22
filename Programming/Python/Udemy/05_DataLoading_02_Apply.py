"""
Author: Rodrigo de Barros Vimieiro
Date: August, 2019
rodrigo.vimieiro@gmail.com
=========================================================================
"""
import pandas as pd
from datetime import datetime


#%% 

# Loading by Pandas

x = pd.read_csv("data/international-airline-passengers.csv",engine="python", skipfooter=3)


x.columns = ["month","passengers"]


print(x.passengers)

x['ones'] = 1   # Add a column

print(x.head())


x['dt'] = x.apply(lambda row: datetime.strptime(row['month'], '%Y-%m'),axis=1)

print(x.info)