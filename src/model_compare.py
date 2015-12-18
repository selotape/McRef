
# coding: utf-8

# In[13]:

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from numpy import exp
from pandas.core.series import Series

pd.set_option('display.mpl_style', 'default')
pd.set_option('display.width', 5000) 
pd.set_option('display.max_columns', 60)


# In[17]:

flat_coalescence_stats =     pd.read_csv        ('C:\\Users\\ronvis\\Dropbox\\Thesis\\ModelCompare\\code\\ModelCompare\\sample_data\\sample-data.flatStats.tsv', sep='\t')


# In[18]:

flat_coalescence_stats = flat_coalescence_stats[['logPrior','coalStatFlat', 'numCoalFlat', 'root_theta', 'genealogyLogLikelihood' ]]
flat_coalescence_stats.columns = ['logPrior','time_stats', 'num_coal', 'root_ϴ', 'P_Z_ϴM' ]

printFactor = 10000.0
flat_coalescence_stats['root_ϴ'] = flat_coalescence_stats[['root_ϴ']].apply(lambda x:x/printFactor)


# In[19]:

def P_Z_ϴM0(theta, num_coal, time_stats):
    result = num_coal*np.log(2.0/theta) -(time_stats/theta)
    return result


# In[20]:

flat_coalescence_stats['root_ϴ'] = flat_coalescence_stats[['root_ϴ']].apply(lambda x:x/1000.0)
root_ϴ = flat_coalescence_stats['root_ϴ'] 
num_coal = flat_coalescence_stats['num_coal'] 
time_stats = flat_coalescence_stats['time_stats']

flat_coalescence_stats['P_Z_ϴM0'] = P_Z_ϴM0(root_ϴ, num_coal, time_stats)


# In[21]:

flat_coalescence_stats['P_Z_ϴM0'].plot()


# In[22]:

flat_coalescence_stats['P_Z_ϴM'].plot()


# In[23]:

flat_coalescence_stats.describe()


# In[24]:

flat_coalescence_stats.head()

E_P_Z_ϴM = flat_coalescence_stats['P_Z_ϴM'].mean()
E_P_Z_ϴM0 = flat_coalescence_stats['P_Z_ϴM0'].mean()

result = E_P_Z_ϴM - E_P_Z_ϴM0
print("E_P_Z_ϴM0 " + str(E_P_Z_ϴM0))
print("E_P_Z_ϴM " + str(E_P_Z_ϴM))
