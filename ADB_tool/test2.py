import os.path
import threading
import time
import public
import getpass,win32api
import datetime

adb_path = public.resource_path(os.path.join('adb-tools'))


def main_record():
    os.chdir(adb_path)
    # 录屏
    p = public.execute_cmd('adb shell screenrecord /sdcard/demo.mp4')
    print(p)


def stop():
    time.sleep(5)
    public.stop_thread(t1)


t1 = threading.Thread(target=main_record)
t1.start()

t2 = threading.Thread(target=stop)
t2.start()