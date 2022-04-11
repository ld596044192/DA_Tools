# 主程序
# -*- coding:utf-8 -*-
import sys
import threading

import public
import os,getpass
import win32api

adb_path = public.resource_path(os.path.join('main', 'main_adb.exe'))
logo_path = public.resource_path(os.path.join('main', 'main_logo.exe'))
username = getpass.getuser()

# 创建临时文件夹
make_dir = 'C:\\Users\\' + username + '\\Documents\\ADB_Tools(DA)\\'
if not os.path.exists(make_dir):
    os.makedirs(make_dir)
# 主程序启动标志
root_state = make_dir + 'root_state.txt'


class Main_Threads(object):
    def __init__(self):
        with open(root_state,'w') as fp:
            fp.write('0')
        print('程序已初始化！！！')

    def main(self):
        def logo():
            win32api.ShellExecute(0, 'open', logo_path, '', '', 1)

        def adb():
            while True:
                root_state_finally = open(root_state, 'r').read()
                if root_state_finally == '0-1':
                    break
                elif root_state_finally == 'main_stop':
                    sys.exit()
            win32api.ShellExecute(0, 'open', adb_path, '', '', 1)

        t1 = threading.Thread(target=logo)
        t1.setDaemon = True
        t1.start()

        t2 = threading.Thread(target=adb)
        t2.setDaemon = True
        t2.start()


if __name__ == '__main__':
    main = Main_Threads()
    main.main()


