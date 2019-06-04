import pandas as pd
import numpy as np
import re
import math

#中文表格载入过程注意encoding
df = pd.read_csv('xxxxx.csv', header = None, encoding = 'utf-8')
df = pd.DataFrame(df)
df = df.replace(r'^\s*$', np.nan, regex=True)

#数据备份
dfcopy = df.copy()

#数据维度
rowlen = dfcopy.shape[0]
collen = dfcopy.shape[1]

ds = pd.DataFrame(columns=[0,1,2,3,4])
l = 0

for i in range(0,rowlen):
#说明性print
    if i%5000==0:
        print("It's the %ith row"%i)
    #提取一整行数据进行处理，去除NaN    
    #删除带有特殊字符的单元格
    #例：删除所有带有“投资”二字的单元格，删除所有带有“Foreign”单词的单元格。
    #单元格内可能是“投资公司”，“投资人”。只要有“投资”就会被整个删掉。
    dfcopy_row = dfcopy.iloc[i,]
    dfcopy_row_af = dfcopy_row.dropna(how = 'any', axis = 0, inplace = False)
    row_af = pd.DataFrame(dfcopy_row_af)
    row_af.columns=["a"]
    row_af = row_af[~row_af.a.str.contains("投资")]
    row_af = row_af[~row_af.a.str.contains("Foreign")]
    lends = len(row_af)
    
    #转置清理后的数据为一行的Dataframe
    df_after = pd.DataFrame(row_af)
    df_after.reset_index(inplace=True,drop=True)
    df_after = pd.DataFrame(df_after).T
    df_after.reset_index(inplace=True,drop=True)
    
    #用math.ceil向上取整。math.ceil(6/5)=2
    f = 0
    newlist = []
    x = math.ceil(lends/5)
    y = 5*x
    
    #找到包含特定值或者字符的元素，以此元素为新的一行的第一列
    #即，每读到含有“姓名”的单元格时写入新的一行
    #假设新的数据为五列
    #则用特定值或者字符补齐行，例：“drop”
    #例如["姓名 张三","性别 男","年龄 18","身高 180","籍贯 BJ","姓名 李四","性别 男","年龄 17","身高 175"]，第二行写入时，“籍贯”缺失，则加入指定字符在此单元格。
    for f in range(0,lends):
        a = str(df_after[f])
        if a.find("姓名") != -1:
            for b in range(f,f+5):
                try:
                    newlist.append(df_after[[b]])
                except KeyError:
                    newlist.append("drop")
    newdf = pd.DataFrame(newlist)
    
    #依旧用上面的例子，把十个元素分割为两行，每行五个值。
    dfappend = pd.DataFrame(columns=[0,1,2,3,4])
    lds = len(newdf)
    c = int(lds//5)
    j = 0
    for j in range(0,c):
        d = j * 5
        e = d + 5
        dftem = newdf[d:e]
        dftemn = pd.DataFrame(dftem)
        dftra = dftemn.T
        dftra.columns = [0,1,2,3,4]
        dfappend = dfappend.append(dftra)    
    ds = ds.append(dfappend)
print("Finished")
ds.reset_index(inplace=True,drop=True)

#删除含有特定元素的行
#把前一步输出中所有含有“drop”的行都删除。
dsstr = ds.astype(str)
new = dsstr[~dsstr[4].str.contains('drop')]
                               #, na=False)]
new.reset_index(inplace=True,drop=True)

#删除每个元素特定字符左边的内容。
#比如“中文 苹果”，只想留“苹果”而删除整列的“中文”，见new[0]
new[0] = new[0].str.split('中文').str[1]
new[1] = new[1].str.split('英文').str[1]
new[2] = new[2].str.split('HA').str[1]
new[3] = new[3].str.split('\n0').str[1]
new[4] = new[4].str.split('?))').str[1]
#new.head()

#更改列名称
new.columns = ["A","B","C","D","E"]
#new.head()

#"utf-8" maybe return unreadable code. 中文写入.csv时候encoding用“utf-8-sig”。
new.to_csv('newfile.csv',encoding='utf-8-sig')
