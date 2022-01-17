# 该py程序需要单独打包成一个exe后台程序供主程序调用，放进background_program文件夹即可
import datetime
import os.path
import sys
import time
import tkinter,tkinter.ttk
import tkinter.messagebox
import threading
import getpass,signal

import public

users = getpass.getuser()
dir_path = 'C:\\Users\\' + users + '\\Documents\\little_tools(DA)'
minute_path = dir_path + '\\minute.log'
target_path = dir_path + '\\target.log'
state_path = dir_path + '\\state.log'
log_path = dir_path + '\\time.log'

with open(log_path,'w') as fp:
    fp.write('')
# 获取当前进程pid
pid = os.getpid()


class MainForm_blackground():
    def root_form(s):
        s.root_time = tkinter.Tk()
        s.root_time.withdraw()
        s.root_time.wm_attributes('-topmost', 1)
        s.timing_update()
        s.root_time.mainloop()

    # def time_update(s):
    #     s.minute = open(minute_path, 'r').read()
    #     s.now = datetime.datetime.now()
    #     print(s.now)
    #     s.delta = datetime.timedelta(minutes=int(s.minute))
    #     print(s.delta)
    #     s.target = s.now + s.delta
    #     print(s.target)
    #     s.timing_update()

    def stop_update(s):
        # 程序状态需要实时更新
        s.state = open(state_path, 'r').read()
        if s.state == 'stop' or s.state == 'close':
            s.root_time.destroy()
            os.kill(pid, signal.SIGKILL)
            sys.exit()

    def timing_update(s):
        def t_update():
            public.cmd_editor_disable()
            s.minute = open(minute_path, 'r').read()
            s.target_datetime = open(target_path,'r').read()
            # 字符串类型转换为时间datetime类型
            s.target = datetime.datetime.strptime(s.target_datetime, "%Y-%m-%d %H:%M:%S")
            while True:
                now = datetime.datetime.now()
                print(now)
                countdown = s.target - now
                print(countdown)
                # 时间日志（便于开发调试）
                with open(log_path,'a') as fp:
                    fp.write(str(countdown)[:7] + '\n')
                if str(countdown)[:7] == '0:00:00':
                    ok = tkinter.messagebox.showwarning(title="FBIWarning", message="您已未喝水{}分钟,请马上喝水,健康生活！".format(s.minute))
                    if ok == 'ok':
                        # 循环计时功能
                        with open(state_path,'w') as fp:
                            fp.write('ok')
                        s.now = datetime.datetime.now()
                        s.delta = datetime.timedelta(minutes=int(s.minute))
                        s.target = s.now + s.delta
                        # 处理计时格式
                        target1 = str(s.target).split(' ')[0]
                        target2 = str(s.target).split(' ')[1].split('.')[0]
                        target_str = target1 + ' ' + target2
                        with open(target_path,'w') as fp:
                            fp.write(target_str)
                        continue
                        # s.root_time.destroy()
                        # os.kill(pid, signal.SIGKILL)
                        # sys.exit()
                time.sleep(1)

        def t_stop_update():
            while True:
                # 停止并终止执行后台程序
                s.stop_update()
                time.sleep(1)

        t_time1 = threading.Thread(target=t_update)
        t_time1.setDaemon(True)
        t_time1.start()

        t_time2 = threading.Thread(target=t_stop_update)
        t_time2.setDaemon(True)
        t_time2.start()


if __name__ == '__main__':
    main_form = MainForm_blackground()
    main_form.root_form()