import re,public,os

a = os.popen('adb shell grep "wlan0" /proc/net/dev','r').read()
print(a)
# b = re.findall('wlan0:\s(.*?)\s',a,re.S)
# print(b)

b_list = [i for i in a.strip().split(' ') if i != '']
print(b_list)
print('下行流量：'+b_list[1])
print('上行流量：'+b_list[9])