import public,re


path  = r'C:\Users\lida\Desktop\123.txt'
a = open(path,'r',encoding='utf-8').read()
print(a)
re1 = re.findall('package: name=\'(.*?)\'\s',a)
print(''.join(re1))

