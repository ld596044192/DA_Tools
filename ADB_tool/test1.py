import re,public,json



e = ['{"__APPID__": "8180000000000020", "deviceId": "DF6E072094422AAEE56D06C247D3A5BB"} ']
print()
d = eval(''.join(e))

for key,value in d.items():
    if key == 'deviceId':
        print(value)
        break