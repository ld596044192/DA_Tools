# 该py程序需要单独打包成一个exe后台程序供主程序调用，放进background_program文件夹即可
import os.path
import public
import getpass
import tkinter
import ctypes,sys,signal
import threading
import psutil

username = getpass.getuser()
adb_path = public.resource_path(os.path.join('adb-tools'))
# 记录录屏状态和pid
make_dir = 'C:\\Users\\' + username + '\\Documents\\ADB_Tools(DA)\\'
record_state = make_dir + 'record_state.txt'
record_pid = make_dir + 'record_pid.txt'
record_count = make_dir + 'record_count.txt'
# 录屏名称
record_name = make_dir + 'record_name.txt'
username = getpass.getuser()
# 自定义录屏保存文件名
record_dirname = 'ADB工具-录屏（DA）'
record_save = 'C:\\Users\\' + username + '\\Desktop\\' + record_dirname + '\\'
# cmd自动最小化
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)
# 获取录屏程序进程名称列表
Processes = []


class MainForm_record():
    def root_form(s):
        s.root_time = tkinter.Tk()
        s.root_time.withdraw()
        # 无需置顶
        # s.root_time.wm_attributes('-topmost', 1)
        s.main_record()
        s.root_time.mainloop()

    def main_record(s):
        def record():
            # 设备录屏
            print('程序获取权限成功，开始录屏...')

            # 开始录屏标记
            with open(record_state, 'w') as fp:
                fp.write('Began to record the screen')

            # 进入录屏临时保存文件夹
            command = 'adb shell cd /sdcard/da_screenrecord'
            screenrecord = public.execute_cmd(command)
            print(screenrecord)
            mkdir_state = screenrecord.split(':')[-1]
            # 创建截图临时保存文件夹
            if mkdir_state == ' No such file or directory\r\n':
                public.execute_cmd('adb shell mkdir /sdcard/da_screenrecord')

            if not os.path.exists(record_count):
                with open(record_count, 'w') as fp:
                    fp.write('0')

            r = int(open(record_count, 'r').read())
            r += 1

            # 创建录屏视频保存文件夹
            if not os.path.exists(record_save):
                os.makedirs(record_save)

            # 录屏前唤醒屏幕
            public.execute_cmd('adb shell input keyevent 224')

            # 获取录屏文件名称
            record_name_finally = open(record_name,'r').read()

            # 录屏
            public.execute_cmd('adb shell screenrecord /sdcard/da_screenrecord/' + record_name_finally + '（' + str(r) + '）' + '.mp4')

        def stop_record():
            while True:
                record_stop = open(record_state,'r').read()
                if record_stop == 'Stop recording screen':

                    # # 获取当前后台程序的pid
                    # pid = os.getpid()
                    # print(pid)
                    # # 关闭后台进程
                    # os.kill(int(pid), signal.SIGINT)

                    # 强制关闭所有相关的后台进程
                    pids = psutil.pids()
                    try:
                        for pid in pids:
                            pid_names = psutil.Process(pid).name()
                            # 获取所有进程名称并添加到列表中
                            Processes.append(pid_names)
                    except psutil.NoSuchProcess:
                        print('不存在该进程，继续执行！')
                    if 'adb.exe' in Processes or 'record_main.exe' in Processes:
                        os.popen('taskkill /F /IM %s ' % 'adb.exe /T','r')
                        os.popen('taskkill /F /IM %s ' % 'record_main.exe /T','r')
                    sys.exit()

        record = threading.Thread(target=record)
        record.setDaemon(True)
        record.start()

        stop_record = threading.Thread(target=stop_record)
        stop_record.setDaemon(True)
        stop_record.start()


# 自动获取权限（UAC）
def run_program():
    main_form = MainForm_record()

    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    if is_admin():
        main_form.root_form()
    else:
        ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, __file__, None, 1)


if __name__ == '__main__':
    run_program()
