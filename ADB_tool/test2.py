import re

name = '90度'

p = re.findall('(.*?)度',name)[0]
print(p)
