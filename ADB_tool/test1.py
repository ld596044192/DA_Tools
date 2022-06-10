import os,re,subprocess

import public

# wifi_mac_result = public.execute_cmd('adb shell ip addr show wlan0')
wifi_mac_result = os.popen('adb shell ip addr show wlan0','r').read().replace('\n\n', '\n')
wifi_mac = ''.join(re.findall('link/ether(.*?)brd',wifi_mac_result)).strip()
print(wifi_mac_result)
print(wifi_mac)

