import pandas as pd
import numpy as np
import re
import math

#All the states in the US and Canada
#Mapping states name with their abbreviates.
state_uscnd = {
    'District of Columbia': 'DC',
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
    'Alberta':'AB',
    'British Columbia':'BC',
    'Manitoba':'MB',
    'New Brunswick':'NB',
    'Newfoundland and Labrador':'NL',
    'Northwest Territories':'NT',
    'Nova Scotia':'NS',
    'Nunavut':'NU',
    'Ontario':'ON',
    'Prince Edward Island':'PE',
    'Quebec':'QC',
    'Saskatchewan':'SK',
    'Yukon':'YT',
}
#Given a dictionary { k1: v1, k2: v2 ... } to get { k1: f(v1), k2: f(v2) ... } => my_dictionary = {k: f(v) for k, v in my_dictionary.items()}
state_uscnd = {state: abbrev for state, abbrev in state_uscnd.items()}

#中文表格载入过程注意encoding
df = pd.read_excel('Headquarter_Checked.xlsx', header = 0, encoding = 'utf-8')
df = pd.DataFrame(df)

#数据备份
dfcopy = df.copy()
#dfcopy.columns

#Get dimension of dataframe
rowlen = dfcopy.shape[0]
collen = dfcopy.shape[1]

#Split element by conditions
#Save elements after ", " and delete the rest. 如果单元格内有逗号，仅保存逗号后内容，*注意空格。
#Save elements in "()" and delete the rest. 如果单元格内有括号，仅保存括号内内容
p1 = re.compile(r'[(](.*?)[)]', re.S)
for i in range(0,rowlen):
    item = dfcopy.iloc[i,2]
    if item.find(',') !=-1:
        a = item.split(', ')
        b = a[1]
        d = re.findall(p1, b)
        if len(d)==1:
            dfcopy.iloc[i,2]=d
        else:
            dfcopy.iloc[i,2]=b
            
#Split dataframe by conditions. 根据条件拆分数据集            
list1 = []
list2 = []
list3 = []
list4 = []
for i in range(0,1301):
    d = dfcopy['0 - Global Headquarter'][i]
    if len(d) == 2:
        list1.append(dfcopy.iloc[i])
    elif d == 'Oops':
        list2.append(dfcopy.iloc[i])
    elif d == 'No headquarter':
        list3.append(dfcopy.iloc[i])
    else:
        list4.append(dfcopy.iloc[i])
listone = pd.DataFrame(list1) #已经是缩写的
listoops = pd.DataFrame(list2) #返回值为“Oops”
listnone = pd.DataFrame(list3) #返回值为空
listtodo = pd.DataFrame(list4) #需要dictionary mapping处理的部分

#处理两部分无用数据用于输出
listoops = listoops.reset_index()
listoops = listoops.drop(columns='index')
listnone = listnone.reset_index()
listnone = listnone.drop(columns='index')

#把全称和缩写对应
#Mapping state full name with its abbreviate name
listtodo['abbrev'] = listtodo['0 - Global Headquarter'].map(state_uscnd)

#输出没有对应值的数据，为非美国或加拿大地区
Nanlist = listtodo[listtodo['abbrev'].isnull()]
Nanlist = Nanlist.drop(columns='abbrev')
Nanlist = Nanlist.reset_index()
Nanlist = Nanlist.drop(columns='index')

#处理可用于import的数据并输出
listdone = listtodo.dropna()
listdone = listdone.drop(columns='0 - Global Headquarter')
listdone.columns = ['Company ID', 'LinkedIn Company Page', '0 - Global Headquarter']
listtoimport = listone.append(listdone)
listtoimport = listtoimport.reset_index()
listtoimport = listtoimport.drop(columns='index')

#输出数据
pd.DataFrame(listtoimport).to_excel('importlist.xlsx', header=False, index=False)
pd.DataFrame(Nanlist).to_excel('notuscnd.xlsx', header=False, index=False)
pd.DataFrame(listoops).to_excel('oops.xlsx', header=False, index=False)
pd.DataFrame(listnone).to_excel('notexist.xlsx', header=False, index=False)





