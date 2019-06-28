#Find company whether in HupSpot.
#Import packages and data
import difflib
import pandas as pd
import numpy as np
from nameparser import HumanName
import string
from titlecase import titlecase
import re
from difflib import SequenceMatcher
import datetime

today = datetime.date.today()

def inputexcel(excel1,baseexcel,header1,header2):
    e1 = pd.read_excel(excel1 ,header = header1, encoding = 'utf-8')
    e2 = pd.read_excel(baseexcel ,header = header2, encoding = 'utf-8')
    return e1,e2
    
e1,e2 = inputexcel('companylist.xlsx','hubspot.xlsx',0,0)

l1 = e1['Name']
l1lo = e1['NameLo']
l2 = e2['Name']
l2 = list(l2)
l2ori = e2['Name']
l2id = list(e2['Company ID'])

for i in range(0,len(l2)):
    l2[i] = l2[i].replace(" ","")
    l2[i] = l2[i].lower()
    
l1lo = map(str, l1lo)
l1lo = list(l1lo)
l2lo = map(str, l2)
l2lo = list(l2lo)

common = []
for item in l2lo:
    comm = difflib.get_close_matches(item,l1lo,1,cutoff=1) 
    common.append(comm)
    
newhs = {"ID":l2id, "Name": l2ori, "Match":common}
newhs = pd.DataFrame(newhs)
newlist = []
for i in range(0,len(newhs['Match'])):
    item = newhs['Match'][i]
    d = len(item)
    if d > 0:
        newlist.append(i)
inhslist = []
for i in newlist:
    inhslist.append(newhs.iloc[i])
inhsdf = pd.DataFrame(inhslist)
inhsdf.to_excel('inhs%s.xlsx'%today, header=True, index=False)

lolist = inhsdf['Match']
lo = []
#The element in column are like "['element']", this part is to get rid of "['']"
for item in lolist:
    p1 = re.compile(r'[[](.*)[]]', re.S) 
    p2 = re.compile(r"['](.*)[']", re.S) 
    pp = re.findall(p1, str(item))
    pp = re.findall(p2, str(item))
    lo.append(pp)
lo = pd.DataFrame(lo)

l1lodf = pd.DataFrame(l1lo)
a = lo[0]
b = l1lodf[0]
diff = list(set(b)-set(a))
difin = []
for item in diff:
    ind = list(l1lodf[0]).index(item)
    difin.append(ind)
    
difflist = []
for i in difin:
    ele = l1.iloc[i]
    difflist.append(ele)
pd.DataFrame(difflist).to_excel('notinhs%s.xlsx'%today, header=True, index=False)
