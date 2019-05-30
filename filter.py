import pandas as pd
import numpy as np

df = pd.read_csv('XXXXXXXX.csv', header = None, encoding = 'utf-8')
df = pd.DataFrame(df)
df = df.replace(r'^\s*$', np.nan, regex=True)
dfcopy = df.copy()
rowlen = dfcopy.shape[0]
collen = dfcopy.shape[1]

def newlist(ds,length):
    dfappend = pd.DataFrame(columns=[0,1,2,3,4])
    x = int(length//5)
    i = 0
    for i in range(0,x):
        a = i * 5
        dftem = df_after[[a,a+1,a+2,a+3,a+4]]
        dftem.columns = [0,1,2,3,4]
        dfappend = dfappend.append(dftem)
        i = i + 1
    return dfappend
    
    ds = pd.DataFrame(columns=[0,1,2,3,4])
for i in range(0,rowlen):
    dfcopy_row = dfcopy.iloc[i,:]
    dfcopy_col = dfcopy_row.T
    df_after = dfcopy_col.dropna(how = 'any', axis = 0, inplace = False)
    lends = len(df_after)
    df_after = pd.DataFrame(df_after)
    df_after.reset_index(inplace=True,drop=True)
    df_after = pd.DataFrame(df_after).T
    nlist = newlist(df_after,lends)
    ds = ds.append(nlist)
    if i%1000==0:
        print("It's the %ith row"%i)
        
ds.columns = ['Name','Language','Place of Registry','Global 500','Registered Capital']
ds.reset_index(inplace=True,drop=True)
ds.to_csv('xxxx.csv')
