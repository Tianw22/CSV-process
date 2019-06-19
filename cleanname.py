#Capitalize Words.
#Delete row by conditions
import pandas as pd
import numpy as np
from nameparser import HumanName
import string

xls = pd.ExcelFile('xxxxxxx.xls')
df = xls.parse('SurveysAnswersCrosstab', skiprows=4, index_col=None) #skip first 4 rows

df = df.drop(df.index[len(df)-1]) #drop the last row
df = df.drop(df.index[0]) #drop the first row
df = df.drop_duplicates("ID", keep='first', inplace=False) #drop duplicate records by "ID"
df = df.reset_index(drop=True)
df = df.fillna(' ') #fill all the NaN with ' '

list1 = []
list2 = []

#Save the rows with "Notes" in list1, else in list2
for i in range(0,int(len(df['Notes']))):
    if str(df['Notes'][i]) != str(df['Notes'][0]):
        list1.append(df.iloc[i])
    else:
        list2.append(df.iloc[i])
        
n1 = pd.DataFrame(list1)
n2 = pd.DataFrame(list2)

n1 = n1.reset_index(drop=True)
n2 = n2.reset_index(drop=True)

#Capitalize all the initial letter of each word in selected columns.
col = ['First Name', 'Title', 'Company', 'Address', 'State', 'City', 'Country']
def capwordallnew(dataset):
    for item in col:
        for i in range(0, len(dataset)):
            if str(dataset[item][i]) != 'United States of America':
                dataset[item][i] = string.capwords(dataset[item][i])
    return dataset

#Capitalize last name with Mc, Mac...
def caplastname(dataset):
    for i in range(0,len(dataset['Last Name'])):
        n = str(dataset['Last Name'][i])
        name = HumanName(n)
        name.capitalize(force=True)
        ln = name.first
        dataset['Last Name'][i] = ln
    return dataset
    
n1 = capwordallnew(n1)
n1 = caplastname(n1)
n2 = capwordallnew(n2)
n2 = caplastname(n2)

#Delete the rows depends on whether the selected column contains a specific parameter.
def dropbycol(col,para):
    new = n2[~n2[col].str.contains(para)]
    return new
    
#for example, delete all the rows depends on whether the 'e-Mail' column contains 'edu'
n2 = dropbycol('e-Mail','edu') 
n1.to_excel('n1.xlsx',header=True, index=False)
n2.to_excel('n2.xlsx',header=True, index=False)
