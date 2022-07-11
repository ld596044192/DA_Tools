import os
import re,public,json,subprocess

a = "adb: error: remote object '/data/crash_reports' does not exist"

d = a.split(':')[-1].strip()
print(d)
