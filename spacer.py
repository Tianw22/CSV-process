#Add(insert) space between letters and numbers
#在数字和字母间加空格
import re
txt = '!!!this, 1is, 2a 3test!!!'
def spacer(text):
    return re.sub(r'([0-9])([a-zA-Z])',r"\1 \2",text,re.MULTILINE).strip()
print(spacer(txt))
#Output => !!!this, 1 is, 2 a 3 test!!!
