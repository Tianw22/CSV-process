#Drop rows with Chinese, Japanese or Korean.
import pandas as pd
import re

df = pd.read_csv('xxxxxxxxxx.csv',header=None,dtype='unicode')
dfli = df[1]

find = []
count = 0
for item in dfli:
    itemstr = str(item)
    if re.match(r'(.*[\u4E00-\u9FFF]+)|([\u4E00-\u9FFF]+.*)', itemstr)!=None:
        count += 1;
    elif re.match(r'(.*[\u3040-\u309f]+)|([\u3040-\u309f]+.*)', itemstr)!=None:
        count += 1;
    elif re.match(r'(.*[\u30a0-\u30ff]+)|([\u30a0-\u30ff]+.*)', itemstr)!=None:
        count += 1;
    elif re.match(r'(.*[\uac00-\ud7ff]+)|([\uac00-\ud7ff]+.*)', itemstr)!=None:
        count += 1;
    else:
        find.append(itemstr)
        
pd.DataFrame(find).to_excel('xxx.xlsx')

# Simplified Chinese &  Traditional Chinese 中文简体和繁体：[\u4E00-\u9FFF]
# Simplified Chinese 中文简体：[\u4E00-\u9FA5]
# Hiragana 日文平假名：[\u3040-\u309f]
# Katakana 日文片假名：[\u30a0-\u30ff]
# Korean 韩文：[\uac00-\ud7ff]
