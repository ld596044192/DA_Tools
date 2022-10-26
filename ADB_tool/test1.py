import os

from adb_test import public
import subprocess

a = public.execute_cmd('adb shell grep "sn" /data/syslog.log')
print(a)

cmd = 'adb shell grep "sn" /data/syslog.log'