import os,public
import re,public,json,subprocess
import time

while True:
    result = os.popen('adb shell /data/miniapp_cli memoryUsage','r').read()
    print(result)
    time.sleep(2)

