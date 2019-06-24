#Check duplicates between two big dataset. 
#两个万级别条数数据集间的查重
#List查重更加高效

#Import packages
import difflib
import pandas as pd
import numpy as np
from nameparser import HumanName
import string
from titlecase import titlecase
import re
from difflib import SequenceMatcher

#Import data
df1 = pd.read_excel('excel1.xlsx',header = None, encoding = 'utf-8') #Import dataset without columns' names.
list1 = df1[0] #Save the first column as list1
df2 = pd.read_excel('excel2.xlsx',header = 0, encoding = 'utf-8') #Import dataset with the first row as columns' names.
list2 = df2['Name'] #Save the column named 'Name' as list2

#Add/Insert space between numbers and letters
#在数字和字母之间加空格
def spacer(text):
    return re.sub(r'([0-9])([a-zA-Z])',r"\1 \2",text,re.MULTILINE).strip()

#Clean data. Uppercase all the Words. Deduplicate the new list.
for i in range(0,len(list1)):
    list1[i] = list1[i].replace(". ",'.')
    list1[i] = spacer(list1[i])
    list1[i] = titlecase(list1[i])
list1 = list1.drop_duplicates(keep='first', inplace=False)
list1 = list1.reset_index(drop=True)
#pd.DataFrame(list1).to_excel('deduplicatelist.xlsx', header=False, index=False)

# Find item of list1 in list2 with similarity of > 95%
# 在 list2 中找到与 list1 中元素相似度达到95%及以上的元素
common = []
for item in list1:
    comm = difflib.get_close_matches(item,list2,1,cutoff=0.95) 
    #difflib 对于两个超大list找相似元素十分高效。
    #用fuzzywuzzy 处理上万级别的数据集比对需要以小时计数处理时间。
    #同样的数据集，用difflib大概需要不到五分钟。
    common.append(comm)
comcom = pd.DataFrame(common)
comcom = comcom.mask(comcom.eq('None')).dropna().reset_index(drop=True) #Drop all the rows with value 'None'.
for i in range(0,len(comcom)):
    comcom[0][i] = spacer(comcom[0][i])    
#pd.DataFrame(comcom).to_excel('include.xlsx', header=False, index=False)
   
# 找到list1和list2不能匹配的list1的部分
a = set(list1)
b = set(comcom[0])
diff = list(a-b)
diff = pd.DataFrame(diff)
#pd.DataFrame(diff).to_excel('notinclude.xlsx', header=False, index=False)
