#Filter out only Asian countries.
import pandas as pd
import re
import difflib
from difflib import SequenceMatcher

df = pd.read_csv('dataset1.csv',encoding='latin-1')
df = pd.DataFrame(df)

asia = pd.read_excel('Asia.xlsx') #In JustData

asiab = asia['Abbr']
asiac = asia['Country']

dfc = df['Nation']

aonly = []
for item in dfc:
    match = difflib.get_close_matches(item,asiab,1,cutoff=1) 
    aonly.append(match)
asiaonly = pd.DataFrame(aonly)

newdf = pd.concat([asiaonly, df], axis=1)

newdfdrop = newdf.mask(newdf[0].eq('None')).dropna().reset_index(drop=True) #Drop all the rows with value 'None'.

asiadroplist = newdfdrop.drop([0],axis=1)

asiadroplist.to_csv('AsianList.csv')
