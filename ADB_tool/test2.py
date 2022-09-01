import re,public,os

a = os.popen('adb shell dumpsys window','r').read()
print(a)
b = re.findall('mCurrentFocus.*?(com.*?)/.*?}',a,re.S)
print(b)

