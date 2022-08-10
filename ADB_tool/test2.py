import public,re,subprocess

a = "cat: can't open '/data/UUID.ini': No such file or directory"

b = ' '.join(a.strip().split()).split(':')[-1].strip()
print(b)
