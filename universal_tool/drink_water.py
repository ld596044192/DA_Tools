import datetime
import re
import time
import tkinter,tkinter.ttk,win32api
import tkinter.messagebox
import threading
import os,sys
import public,getpass
from systrayicon import SysTrayIcon
import requests

version_path = public.resource_path(os.path.join('version','version_history.txt'))
LOGO_path = public.resource_path(os.path.join('icon', 'water.ico'))
# upgrade_path = public.resource_path(os.path.join('upgrade', 'upgrade.exe'))
users = getpass.getuser()
dir_path = 'C:\\Users\\' + users + '\\Documents\\little_tools(DA)'
minute_path = dir_path + '\\minute.log'
target_path = dir_path + '\\target.log'
state_path = dir_path + '\\state.log'
install_path = dir_path + '\\install.log'
pid_path = dir_path + '\\pid.log'
# exe_path = public.resource_path(os.path.join('background_program', 'time_main.exe'))
Processes = []
# 同一修改版本号
version = 'V1.0.4'
version_code = 104

if not os.path.exists(dir_path):
    os.makedirs(dir_path)
pwd = os.getcwd()
pid = os.getpid()
with open(install_path,'w') as fp:
    fp.write(pwd)
with open(pid_path,'w') as fp:
    fp.write(str(pid))


class MainForm(object):
    def __init__(s):
        s.lock = threading.RLock()
        s.stop_flag = False
        s.SysTrayIcon = None  # 判断是否打开系统托盘图标

    # 最小化到托盘
    def minimize(s):
        # 窗口最小化判断，可以说是调用最重要的一步
        s.root.bind("<Unmap>",lambda event: s.hidden())

    def hidden(s):
        if s.root.state() == 'iconic':
            # with open(state_path,'w') as fp:
            #     fp.write('iconic')
            s.Hidden_window()

    # def switch_icon(s, _sysTrayIcon, icon='water.ico'):
    #     # 点击右键菜单项目会传递SysTrayIcon自身给引用的函数，所以这里的_sysTrayIcon = s.sysTrayIcon
    #     # 只是一个改图标的例子，不需要的可以删除此函数
    #     _sysTrayIcon.icon = icon
    #     _sysTrayIcon.refresh()
    #
    #     # 气泡提示的例子
    #     s.show_msg(title='图标更换', msg='图标更换成功！', time=500)

    # def show_msg(s, title='标题', msg='内容', time=500):
    #     s.SysTrayIcon.refresh(title=title, msg=msg, time=time)

    def Hidden_window(s, icon=LOGO_path, hover_text="喝水提醒小工具" + version):
        '''隐藏窗口至托盘区，调用SysTrayIcon的重要函数'''

        # 托盘图标右键菜单, 格式: ('name', None, callback),下面也是二级菜单的例子
        # 24行有自动添加‘退出’，不需要的可删除
        # menu_options = (('一级 菜单', None, s.switch_icon),
        #                 ('二级 菜单', None, (('更改 图标', None, s.switch_icon),)))
        menu_options = ()  # 不需要菜单就空着

        s.root.withdraw()  # 隐藏tk窗口
        if not s.SysTrayIcon: s.SysTrayIcon = SysTrayIcon(
            icon,  # 图标
            hover_text,  # 光标停留显示文字
            menu_options,  # 右键菜单
            on_quit=s.exit,  # 退出调用
            tk_window=s.root,  # Tk窗口
        )
        s.SysTrayIcon.activation()

    def exit(s, _sysTrayIcon=None):
        with open(state_path,'w') as fp:
            fp.write('close')
        s.root.destroy()
        print('exit...')

    def root_form(s):
        s.root = tkinter.Tk()
        s.root.title('喝水提醒小工具' + version + ' tktiner版')
        screenWidth = s.root.winfo_screenwidth()
        screenHeight = s.root.winfo_screenheight()
        w = 400
        h = 270
        x = (screenWidth - w) / 2
        y = (screenHeight - h) / 2
        s.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        s.root.iconbitmap(LOGO_path)
        s.root.resizable(0, 0)
        # s.root.attributes("-toolwindow", 2)  # 去掉窗口最大化最小化按钮，只保留关闭
        # s.root.overrideredirect(1)  # 隐藏标题栏 最大化最小化按钮
        # s.root.config(bg=bg)
        s.main_menu_bar()
        s.drink_water_frame()
        s.stop_button1.place(x=230, y=100)
        s.root.wm_attributes('-topmost', 1)
        # s.root.protocol('WM_DELETE_WINDOW', s.exit)  # 点击Tk窗口关闭时直接调用s.exit，不使用默认关闭
        s.upgrade()
        s.root.protocol('WM_DELETE_WINDOW', s.close_handle)
        # s.root.mainloop()
        return s.root

    def close_handle(s):
        with open(state_path,'w') as fp:
            fp.write('close')
        s.exit()

    def main_menu_bar(s):
        s.main_menu = tkinter.Menubutton(s.root,text='提醒模式')
        s.main_menu1 = tkinter.Menubutton(s.root, text='提醒模式')
        s.main_menu1.place(x=0, y=0)
        s.main_menu1.config(state='disable')
        s.verion_menu = tkinter.Menubutton(s.root,text='版本历史')
        s.verion_menu1 = tkinter.Menubutton(s.root, text='版本历史')
        s.verion_menu1.config(state='disable')
        s.main_menu.bind('<Button-1>',lambda x:s.display_main_frame())
        s.verion_menu.bind('<Button-1>',lambda x:s.display_version_frame())
        s.main_menu.place(x=0,y=0)
        s.verion_menu.place(x=60,y=0)

    def display_main_frame(s):
        # 显示提醒喝水主窗口
        s.verion_frame.pack_forget()
        s.drink_water_frame()
        s.verion_menu1.place_forget()
        s.main_menu1.place(x=0, y=0)
        # 切换模式时需要判断按钮显示
        state = open(state_path,'r').read()
        if state != '':
            s.stop_button1.place(x=230, y=100)
        else:
            s.start_button1.place(x=80, y=100)

    def display_version_frame(s):
        # 显示版本历史窗口
        s.main_frame.pack_forget()
        s.version_history_frame()
        s.main_menu1.place_forget()
        s.verion_menu1.place(x=60, y=0)

    def drink_water_frame(s):
        # 提醒喝水主窗口
        s.main_frame = tkinter.Frame(s.root,width=400,height=250)
        s.text = tkinter.Label(s.main_frame,text='请输入提醒喝水的时间(单位为分钟): ')
        s.text.place(x=20,y=40)

        # s.time = tkinter.IntVar()
        # s.entry = tkinter.Entry(s.main_frame,textvariable=s.time)
        # s.entry.place(x=230,y=40)

        # 下拉框
        s.time = tkinter.StringVar()
        s.combobox = tkinter.ttk.Combobox(s.main_frame,textvariable=s.time)
        s.combobox['value'] = ('5分钟','10分钟','15分钟','20分钟','30分钟','60分钟')
        s.combobox.current(2)
        s.combobox.place(x=220,y=40)

        s.warning_str = tkinter.StringVar()
        s.warning_label = tkinter.Label(s.main_frame,textvariable=s.warning_str,fg='red')
        s.warning_label.place(x=220,y=65)

        s.start_button = tkinter.Button(s.main_frame,text='开始提醒')
        s.start_button1 = tkinter.Button(s.main_frame,text='开始提醒')
        s.start_button1.config(state='disable')
        s.start_button.place(x=80,y=100)

        s.stop_button = tkinter.Button(s.main_frame, text='停止提醒')
        s.stop_button1 = tkinter.Button(s.main_frame, text='停止提醒')
        s.stop_button1.config(state='disable')
        s.stop_button.place(x=230, y=100)

        # 显示版本号
        s.version_name = tkinter.StringVar()
        s.version_label = tkinter.Label(s.main_frame,textvariable=s.version_name)
        s.version_name.set('当前版本号: ' + version)
        s.version_label.place(x=280,y=230)

        s.start_button.bind('<Button-1>',lambda x: s.time_update())
        s.stop_button.bind('<Button-1>',lambda x: s.stop_update())
        s.main_frame.pack(side='bottom')

    def version_history_frame(s):
        # 历史版本信息窗口
        s.verion_frame = tkinter.Frame(s.root,width=400,height=270)
        s.scrollbar = tkinter.Scrollbar(s.verion_frame)
        s.version_listbox = tkinter.Listbox(s.verion_frame, width=55, height=12,yscrollcommand=(s.scrollbar.set))
        s.version_listbox.bindtags((s.version_listbox,'all'))
        s.scrollbar.config(command=(s.version_listbox.yview))
        s.scrollbar.pack(side=(tkinter.RIGHT), fill=(tkinter.Y))
        s.version_listbox.pack()
        version_read = open(version_path,'r',encoding='utf-8')
        for readline in version_read.readlines():
            s.version_listbox.insert(tkinter.END, readline)
        version_read.close()
        s.verion_frame.pack(side='bottom')

    def stop_update(s):
        global stop_flag
        s.stop_flag = True
        s.stop_button1.place(x=230, y=100)
        s.start_button1.place_forget()
        with open(state_path,'w') as fp:
            fp.write('stop')
        return s.stop_flag

    def time_update(s):
        # 清空程序状态
        with open(state_path, 'w') as fp:
            fp.write('')
        try:
            s.start_button1.place(x=80, y=100)
            s.stop_button1.place_forget()
            # 清空错误警告提示
            s.warning_str.set('')

            # 判断输入值是否为包含“分钟”或纯数字的值，不同的值处理的方法不同，采取正则表达式判断
            try:
                s.time_get = s.time.get()
                s.time_finally = re.findall('\d(分钟)',s.time_get)[0]
                if s.time_finally == '分钟':
                    s.minute = int(s.time.get()[:-2].strip())
            except IndexError:
                s.minute = int(s.time.get().strip())

            with open(minute_path, 'w') as fp:
                fp.write(str(s.minute))
            s.now = datetime.datetime.now()
            print(s.now)
            s.delta = datetime.timedelta(minutes=s.minute)
            print(s.delta)
            s.target = s.now + s.delta
            target1 = str(s.target).split(' ')[0]
            target2 = str(s.target).split(' ')[1].split('.')[0]
            target_str = target1 + ' ' + target2
            with open(target_path, 'w') as fp:
                fp.write(target_str)
            print(s.target)
            s.time_threads()
        except ValueError:
            s.stop_button1.place(x=230, y=100)
            s.start_button1.place_forget()
            s.warning_str.set('输入的值不合法！请重新输入\n支持纯数字或“数字+分钟”格式')

    def time_threads(s):
        def time_target():
            s.timing_update()

        def time_main():
            # # 强制调用exe后台程序
            # while True:
            #     pids = psutil.pids()
            #     try:
            #         for pid in pids:
            #             pid_names = psutil.Process(pid).name()
            #             Processes.append(pid_names)
            #     except psutil.NoSuchProcess:
            #         print('不存在该进程，继续执行！')
            #     if 'time_main.exe' not in Processes:
            #         public.execute_cmd(exe_path)
            #     else:
            #         break
            # os.system(exe_path)

            # 单独打包为一个exe时使用
            # public.execute_cmd(exe_path)
            # 不单独打包为一个exe文件时使用这个方法调用其他程序
            win32api.ShellExecute(0, 'open',pwd + '/background_program/time_main.exe' , '', '', 1)

        t1 = threading.Thread(target=time_target)
        t1.setDaemon(True)
        t1.start()

        t2 = threading.Thread(target=time_main)
        t2.setDaemon(True)
        t2.start()

    def timing_update(s):
        def t_update():
            # # 加锁
            # s.lock.acquire()
            while True:
                now = datetime.datetime.now()
                print(now)
                countdown = s.target - now
                print(countdown)
                s.countdown_str = tkinter.StringVar()
                s.time_label = tkinter.Label(s.main_frame, textvariable=s.countdown_str, font=("黑体", 70))
                s.countdown_str.set(str(countdown)[:7])
                s.time_label.place(x=30, y=130)
                if str(countdown)[:7] == '0:00:00' or str(countdown)[:7] == '-1 day,':
                    s.time_label.pack_forget()
                    now = datetime.datetime.now()
                    countdown_zero = now - now
                    s.countdown_str.set(str(countdown_zero)[:7])
                    s.state = open(state_path,'r').read()
                    if s.state == 'ok':
                        with open(state_path,'w') as fp:
                            fp.write('')
                        s.target_datetime = open(target_path,'r').read()
                        s.target = datetime.datetime.strptime(s.target_datetime, "%Y-%m-%d %H:%M:%S")
                        continue
                    # tkinter.messagebox.showwarning(title="FBIWarning", message="您已未喝水{}分钟,请马上喝水,健康生活！".format(s.minute))
                    # s.lock.release()  # 释放锁
                    # s.stop_button1.place(x=230, y=100)
                    # s.start_button1.place_forget()
                    # public.stop_thread(t_time)
                    # sys.exit()
                elif s.stop_flag:
                    s.time_label.pack_forget()
                    now = datetime.datetime.now()
                    countdown_stop = now - now
                    s.countdown_str.set(str(countdown_stop)[:7])
                    # s.lock.release()
                    s.stop_flag = False
                    public.stop_thread(t_time)
                    sys.exit()
                else:
                    s.root.update()
                # 设为0.5秒让显示的倒计时更加精确
                time.sleep(0.5)

        t_time = threading.Thread(target=t_update)
        t_time.setDaemon(True)
        t_time.start()

    def upgrade(s):
        def t_upgrade():
            s.version_name.set('正在检测更新...')
            # 查看github最新版本/检查更新
            response = requests.get("https://api.github.com/repos/ld596044192/DA_Tools/releases/latest")
            version_upgrade = response.json()["tag_name"]
            s.version_name.set('最新版本号: ' + version_upgrade)
            version_split = ''.join(version_upgrade.split('V')).split('.')
            version_finally = ''.join(version_split)
            if version_code < int(version_finally):
                # 单独打包为一个exe时使用
                # public.execute_cmd(upgrade_path)
                # 不单独打包为一个exe文件时使用这个方法调用其他程序
                win32api.ShellExecute(0, 'open',pwd + '/upgrade/upgrade.exe', '', '', 1)
            else:
                s.version_name.set('当前版本为最新版！')
                time.sleep(3)
                s.version_name.set('当前版本号: ' + version)

        t_upgrade = threading.Thread(target=t_upgrade)
        t_upgrade.setDaemon(True)
        t_upgrade.start()
