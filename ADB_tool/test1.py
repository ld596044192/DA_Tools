import os
import re,public,json,subprocess


uuid_result = public.execute_cmd('adb shell grep "UUID" /data/syslog.log > C:\Users\lida\Documents\ADB_Tools(DA)\uuid.log')
