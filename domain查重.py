import difflib
import pandas as pd
import numpy as np
import string
import re
from difflib import SequenceMatcher
import datetime

today = datetime.date.today()

def inputexcel(excel1,baseexcel,header1,header2):
    # Import the excel files
    e1 = pd.read_excel(excel1 ,header = header1, encoding = 'utf-8')
    e2 = pd.read_excel(baseexcel ,header = header2, encoding = 'utf-8')

    #List for checking purpose
    e1 = e1.dropna(subset=['Website'])
    l1 = e1['Website']
    l2 = e2['Company Domain Name']
    
    # Make sure to change the elements in the list into string.
    #Or will throw a error that "object of type 'float' has no len()"
    l1 = map(str, l1)
    l1 = list(l1)
    l2 = map(str, l2)
    l2 = list(l2)
    
    # Find common part between list1 and list2
    comweb = []
    for item in l1:
        comm = difflib.get_close_matches(item,l2,1,cutoff=1) 
        comweb.append(comm)
    web = pd.DataFrame(comweb)
    web = web.mask(web.eq('None')).dropna().reset_index(drop=True) #Drop all the rows with value 'None'.
    
    # Save the ones in both list1 and list2, and save into excel with list1 columns details.
    # 保存 list1 和 list2 中共有的 website， 并保存此 website 在 list1 中所在行的所有信息于新表格。
    ind1 = []
    sdf = []
    for item in web[0]:
        ind1.append(l1.index(item))
    for index in ind1:
        sdf.append(e1.iloc[index])
    sdf = pd.DataFrame(sdf)
    sdf.to_excel('inhs%s.xlsx'%today, header=True, index=False)
    
    # Save the ones in list1 but not not list2, and save into excel with list1 columns details.
    # 保存在 list1 中但不在 list2 中的 website， 并保存此 website 在 list1 中所在行的所有信息于新表格。
    a = set(l1)
    b = set(web)
    diff = list(a-b)
    diff = pd.DataFrame(diff)
    ind = []
    difdf = []
    for item in diff[0]:
        ind.append(l1.index(item))
    for index in ind:
        difdf.append(e1.iloc[index])
    difdf = pd.DataFrame(difdf)
    difdf.to_excel('notinhs%s.xlsx'%today, header=True, index=False)
    
inputexcel('excel1.xlsx','hubspot-crm-exports.xlsx',0,0)
