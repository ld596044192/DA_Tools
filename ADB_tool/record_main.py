# 该py程序需要单独打包成一个exe后台程序供主程序调用，放进background_program文件夹即可
import os.path
import time

import public
import getpass
import tkinter
import ctypes,sys,signal
import threading
import psutil

username = getpass.getuser()
adb_path = public.resource_path(os.path.join('adb-tools'))
record_version = public.resource_path(os.path.join('version','record_version.txt'))
# 记录程序位置
exe_path = public.resource_path(os.path.join('temp','exe_path.log'))
# 记录录屏状态和pid
make_dir = 'C:\\Users\\' + username + '\\Documents\\ADB_Tools(DA)\\'
record_state = make_dir + 'record_state.txt'
record_pid = make_dir + 'record_pid.txt'
record_count = make_dir + 'record_count.txt'
# 录屏名称
record_name = make_dir + 'record_name.txt'
# 录屏时间
record_time = make_dir + 'record_time.txt'
# 录屏模式
record_model_log = make_dir + 'record_model.log'
username = getpass.getuser()
# 自定义录屏保存文件名
record_dirname = 'ADB工具-录屏（DA）'
record_save = 'C:\\Users\\' + username + '\\Desktop\\' + record_dirname + '\\'
# 连续模式保存文件
record_model_save_1 = record_save + '连续模式' + '\\'
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
        def main_record(record_time_finally,record_name_model):
            # 录屏 # 最大录屏时间为180秒
            record_cmd = 'adb shell screenrecord --time-limit ' + record_time_finally + ' /sdcard/da_screenrecord/' + record_name_model
            public.execute_cmd(record_cmd)

        def record():
            # 设备录屏
            print('程序获取权限成功，开始录屏...\n')

            # 显示版本历史内容
            fp = open(record_version,'r',encoding='utf-8').readlines()
            for version in fp:
                print(version)

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

            # 获取录屏设置时间
            record_time_finally = open(record_time,'r').read()

            # 获取模式
            record_model_get = open(record_model_log,'r').read()
            # 手动模式
            if record_model_get == '0':
                record_name_model = record_name_finally + '（' + str(r) + '）' + '.mp4'
                main_record(record_time_finally,record_name_model)
            # 连续模式
            elif record_model_get == '1':
                i = 1
                while True:
                    devices_state = public.device_connect()
                    with open(record_state,'w') as fp:
                        fp.write('Began to record the screen')

                    record_name_model = record_name_finally + '（' + str(r) + '）连续-' + str(i) + '.mp4'
                    main_record(record_time_finally, record_name_model)
                    # 连续模式保存文件
                    if not os.path.exists(record_model_save_1):
                        os.makedirs(record_model_save_1)

                    download_cmd = 'adb pull /sdcard/da_screenrecord/' + record_name_model + ' ' + record_model_save_1 + record_name_model
                    # print(download_cmd)
                    public.execute_cmd(download_cmd)

                    # 删除录屏文件缓存（减少占用空间）
                    public.execute_cmd('adb shell rm -r /sdcard/da_screenrecord/*.mp4')

                    with open(record_state,'w') as fp:
                        fp.write('continuous')
                    i += 1
                    time.sleep(2)
                    # 设备突然中断连接，连续模式结束
                    if not devices_state:
                        break

            # 录屏各项异常处理
            print('设备突然中断连接或录屏最大时间到了，录屏结束！')
            with open(record_state,'w') as fp:
                fp.write('Stop recording screen')

        def stop_record():
            # 等待2S后检测
            time.sleep(2)
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
