import time
import tkinter,tkinter.ttk
import tkinter.messagebox
import threading
import os,sys
import public,getpass
import quickly,screen_record

username = getpass.getuser()
LOGO_path = public.resource_path(os.path.join('icon', 'android.ico'))
version_path = public.resource_path(os.path.join('version','version_history.txt'))
adb_path = public.resource_path(os.path.join('adb-tools'))
record_state = public.resource_path(os.path.join('temp','record_state.txt'))
# 计数
make_dir = 'C:\\Users\\' + username + '\\Documents\\ADB_Tools(DA)\\'
count_path = make_dir + 'screenshots_count.txt'
# 录屏状态
record_screen_state = make_dir + 'record_state.txt'
# 录屏名称
record_name = make_dir + 'record_name.txt'
# 同一修改版本号
version = 'V1.0.0.3'
version_code = 1003
# 同一修改frame的宽高
width = 600
height = 355
# 统一按钮宽度
width_button = 20


class MainForm(object):
    def root_form(s):
        s.root = tkinter.Tk()
        s.root.title('ADB测试工具' + version + ' tktiner版')
        screenWidth = s.root.winfo_screenwidth()
        screenHeight = s.root.winfo_screenheight()
        w = 600
        h = 400
        x = (screenWidth - w) / 2
        y = (screenHeight - h) / 2
        s.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        s.root.iconbitmap(LOGO_path)
        s.root.resizable(0, 0)
        # s.root.attributes("-toolwindow", 2)  # 去掉窗口最大化最小化按钮，只保留关闭
        # s.root.overrideredirect(1)  # 隐藏标题栏 最大化最小化按钮
        # s.root.config(bg=bg)
        # 软件始终置顶
        s.root.wm_attributes('-topmost', 1)
        # s.root.protocol('WM_DELETE_WINDOW', s.exit)  # 点击Tk窗口关闭时直接调用s.exit，不使用默认关闭
        s.main_menu_bar()
        s.quickly_frame()
        s.root.mainloop()
        return s.root

    def main_menu_bar(s):
        # 切换窗口（选择模式）
        s.main_menu = tkinter.Menubutton(s.root,text='快捷模式')
        s.main_menu1 = tkinter.Menubutton(s.root, text='快捷模式')
        s.main_menu1.place(x=0, y=0)
        s.main_menu1.config(state='disable')
        s.screen_menu = tkinter.Menubutton(s.root, text='截图录屏')
        s.screen_menu1 = tkinter.Menubutton(s.root, text='截图录屏')
        s.screen_menu1.config(state='disable')
        s.verion_menu = tkinter.Menubutton(s.root,text='版本历史')
        s.verion_menu1 = tkinter.Menubutton(s.root, text='版本历史')
        s.verion_menu1.config(state='disable')
        s.main_menu.bind('<Button-1>',lambda x:s.display_main_frame())
        s.verion_menu.bind('<Button-1>',lambda x:s.display_version_frame())
        s.screen_menu.bind('<Button-1>',lambda x:s.display_screenshot_frame())
        s.main_menu.place(x=0,y=0)
        s.screen_menu.place(x=60, y=0)
        s.verion_menu.place(x=120,y=0)

        # 连接设备功能
        s.devices_str = tkinter.StringVar()
        s.devices_state_label = tkinter.Label(s.root,text='设备连接状态：')
        s.devices_str.set('正在检测连接状态...')
        s.devices_state_label.config(command=s.devices_bind())
        s.devices_null = tkinter.StringVar()
        s.devices_success = tkinter.Label(s.root,textvariable=s.devices_str,fg='green')
        s.devices_fail = tkinter.Label(s.root,textvariable=s.devices_null,fg='red')

        s.devices_state_label.place(x=370,y=0)

        # 检测本地adb服务（None则使用内置adb）
        s.adb_state_label = tkinter.Label(s.root, text='ADB服务连接状态：')
        s.adb_state_label.config(command=s.adb_bind())
        s.adb_str = tkinter.StringVar()
        s.adb_success = tkinter.Label(s.root,textvariable=s.adb_str,fg='green')
        s.adb_success.place(x=110,y=375)
        s.adb_state_label.place(x=0,y=375)

    def display_main_frame(s):
        # 显示快捷模式主窗口
        s.quickly_frame()
        s.screen_frame1.place_forget()
        s.verion_menu1.place_forget()
        s.screen_menu1.place_forget()
        s.main_menu1.place(x=0, y=0)
        try:
            s.verion_frame.place_forget()
        except AttributeError:
            print('所选窗口未启动 -警告信息Logs（可忽略）')
            pass

    def display_screenshot_frame(s):
        # 显示截图录屏窗口
        s.screen_frame()
        s.quickly_frame1.place_forget()
        s.main_menu1.place_forget()
        s.screen_menu1.place(x=60, y=0)
        s.verion_menu1.place_forget()
        try:
            s.verion_frame.place_forget()
        except AttributeError:
            print('所选窗口未启动 -警告信息Logs（可忽略）')
            pass

    def display_version_frame(s):
        # 显示版本历史窗口
        s.version_history_frame()
        s.quickly_frame1.place_forget()
        s.main_menu1.place_forget()
        s.screen_menu1.place_forget()
        s.verion_menu1.place(x=120, y=0)
        try:
            s.screen_frame1.place_forget()
        except AttributeError:
            print('所选窗口未启动 -警告信息Logs（可忽略）')
            pass

    def quickly_frame(s):
        s.quickly_frame1 = tkinter.Frame(s.root,width=width,height=height)

        # 返回功能
        s.back_button = tkinter.Button(s.quickly_frame1,text='返回 & 后退',width=width_button)
        s.back_button.bind('<Button-1>',lambda x: s.back_bind())
        s.back_button_disable = tkinter.Button(s.quickly_frame1,text='正在返回...',width=width_button)
        s.back_button_disable.config(state='disable')
        s.back_button.place(x=20,y=20)

        # 进入系统设置功能
        s.settings_button = tkinter.Button(s.quickly_frame1,text='进入系统设置',width=width_button)
        s.settings_button.bind('<Button-1>',lambda x: s.settings_bind())
        s.settings_button_disable = tkinter.Button(s.quickly_frame1,text='正在进入中...',width=width_button)
        s.settings_button_disable.config(state='disable')
        s.settings_button.place(x=190,y=20)

        # 重启设备功能
        s.reboot_button = tkinter.Button(s.quickly_frame1,text='重启设备',width=width_button)
        s.reboot_button.bind('<Button-1>',lambda x: s.reboot_bind())
        s.reboot_str = tkinter.StringVar()
        s.reboot_button_disable = tkinter.Button(s.quickly_frame1,textvariable=s.reboot_str,width=width_button)
        s.reboot_button_disable.config(state='disable')
        s.reboot_button.place(x=20,y=60)

        # 关机设备功能
        s.shutdown_button = tkinter.Button(s.quickly_frame1,text='设备关机',width=width_button)
        s.shutdown_button.bind('<Button-1>',lambda x: s.shutdown_bind())
        s.shutdown_button_disable = tkinter.Button(s.quickly_frame1,text='正在关机...',width=width_button)
        s.shutdown_button_disable.config(state='disable')
        s.shutdown_button.place(x=190,y=60)

        # 清理缓存（初始化）功能
        s.clear_button = tkinter.Button(s.quickly_frame1,text='清理缓存（初始化）',width=width_button)
        s.clear_button.bind('<Button-1>',lambda x: s.clear_bind())
        s.clear_button_disable = tkinter.Button(s.quickly_frame1,text='正在初始化...',width=width_button)
        s.clear_button_disable.config(state='disable')
        s.clear_button.place(x=20,y=100)

        # 终止（结束）程序
        s.kill_button = tkinter.Button(s.quickly_frame1,text='终止（结束）应用',width=width_button)
        s.kill_button.bind('<Button-1>',lambda x: s.kill_bind())
        s.kill_button_disable = tkinter.Button(s.quickly_frame1,text='正在结束...',width=width_button)
        s.kill_button_disable.config(state='disable')
        s.kill_button.place(x=190,y=100)

        # 返回Launcher桌面
        s.desktop_button = tkinter.Button(s.quickly_frame1,text='返回桌面',width=width_button)
        s.desktop_button.bind('<Button-1>',lambda x: s.desktop_bind())
        s.desktop_button_disable = tkinter.Button(s.quickly_frame1,text='正在返回...',width=width_button)
        s.desktop_button_disable.config(state='disable')
        s.desktop_button.place(x=20,y=140)

        # 唤醒屏幕
        s.awake_button = tkinter.Button(s.quickly_frame1,text='唤醒屏幕',width=width_button)
        s.awake_button.bind('<Button-1>', lambda x: s.awake_bind())
        s.awake_button_disable = tkinter.Button(s.quickly_frame1, text='正在唤醒...', width=width_button)
        s.awake_button_disable.config(state='disable')
        s.awake_button.place(x=190, y=140)

        # 使用说明
        content = '''
        使用说明：
        若没连接设备时，点击按钮无任何现象属于正常现象
        连接设备后点击按钮，可在设备上观察调试现象
        '''
        s.instructions_label = tkinter.Label(s.quickly_frame1,text=content,fg='red')
        s.instructions_label.place(x=20,y=180)
        s.quickly_frame1.place(y=20)

    def screen_frame(s):
        # 截图录屏窗口
        s.screen_frame1 = tkinter.Frame(s.root,width=width,height=height)

        # 截图状态栏
        s.screen_str = tkinter.StringVar()
        s.screenshut_label = tkinter.Label(s.screen_frame1,textvariable=s.screen_str,bg='black',fg='#FFFFFF',width=46,height=2)
        s.screenshut_label.place(x=20,y=20)
        s.screen_str.set('此处显示截图状态')

        # 截图文件名
        s.screen_entry = tkinter.Entry(s.screen_frame1,width=35)
        s.screenshut_star = tkinter.Label(s.screen_frame1,text='*',fg='red',font=('宋体',15))
        s.screen_entry.insert(tkinter.END,'test')
        s.screen_entry.place(x=50,y=80)
        s.screenshut_star.place(x=300,y=80)

        # 截图文件名说明
        content = '''* 说明：此处可以修改截图生成的文件名称(默认test)\n生成的文件保存在桌面上的“ADB工具-截图（DA）”里面
                '''
        s.screen_readme_label = tkinter.Label(s.screen_frame1, text=content, fg='red',font=('宋体',10))
        s.screen_readme_label.place(x=20, y=100)

        # 截图按钮
        s.screen_button = tkinter.Button(s.screen_frame1,text='一键截图',width=width_button)
        s.screen_button.bind('<Button-1>', lambda x:s.screenshot_bind())
        s.screen_button_disable = tkinter.Button(s.screen_frame1,text='正在截图...',width=width_button)
        s.screen_button_disable.config(state='disable')
        s.screen_button.place(x=20,y=140)

        # 打开截图文件夹按钮
        s.open_screen_button = tkinter.Button(s.screen_frame1,text='打开截图文件夹',width=width_button)
        s.open_screen_button.bind('<Button-1>', lambda x:s.open_screen_bind())
        s.open_screen_button_disable = tkinter.Button(s.screen_frame1,text='正在打开...',width=width_button)
        s.open_screen_button_disable.config(state='disable')
        s.open_screen_button.place(x=200,y=140)

        # 录屏状态栏
        s.record_str = tkinter.StringVar()
        s.record_label = tkinter.Label(s.screen_frame1, textvariable=s.record_str, bg='black', fg='#FFFFFF',
                                           width=46, height=2)
        s.record_label.place(x=20, y=180)
        s.record_str.set('此处显示录屏状态')

        # 录屏文件名
        s.record_entry = tkinter.Entry(s.screen_frame1, width=35)
        s.record_star = tkinter.Label(s.screen_frame1, text='*', fg='red', font=('宋体', 15))
        s.record_entry.insert(tkinter.END, 'demo')
        s.record_entry.place(x=50, y=230)
        s.record_star.place(x=300, y=230)

        # 录屏文件名说明
        content = '''* 说明：此处可以修改录屏后生成的文件名称(默认demo)\n生成的文件保存在桌面上的“ADB工具-录屏（DA）”里面
                        '''
        s.record_readme_label = tkinter.Label(s.screen_frame1, text=content, fg='red', font=('宋体', 10))
        s.record_readme_label.place(x=20, y=250)

        # 录屏按钮
        s.record_button = tkinter.Button(s.screen_frame1, text='开始录屏', width=width_button)
        s.record_button.bind('<Button-1>', lambda x: s.record_bind())
        s.record_button_disable = tkinter.Button(s.screen_frame1, text='正在录屏中', width=width_button)
        s.record_button_disable.config(state='disable')
        s.record_button.place(x=20, y=280)

        # 停止录屏按钮
        s.record_stop_button = tkinter.Button(s.screen_frame1, text='停止录屏', width=width_button)
        s.record_stop_button.bind('<Button-1>', lambda x:s.record_stop_bind())
        s.record_stop_button_disable = tkinter.Button(s.screen_frame1, text='停止录屏', width=width_button)
        s.record_stop_button_disable.config(state='disable')
        s.record_stop_button_disable.place(x=200, y=280)

        s.screen_frame1.place(y=20)

    def version_history_frame(s):
        # 历史版本信息窗口
        s.verion_frame = tkinter.Frame(s.root,width=width,height=height)
        s.scrollbar = tkinter.Scrollbar(s.verion_frame)
        s.version_listbox = tkinter.Listbox(s.verion_frame, width=50, height=16,yscrollcommand=(s.scrollbar.set))
        s.version_listbox.bindtags((s.version_listbox,'all'))
        s.scrollbar.config(command=(s.version_listbox.yview))
        s.scrollbar.pack(side=(tkinter.RIGHT), fill=(tkinter.Y))
        s.version_listbox.pack()
        version_read = open(version_path,'r',encoding='utf-8')
        for readline in version_read.readlines():
            s.version_listbox.insert(tkinter.END, readline)
        version_read.close()
        s.verion_frame.place(y=75)

    def back_bind(s):
        def t_back():
            s.back_button_disable.place(x=20,y=20)
            quickly.android_back()
            s.back_button_disable.place_forget()

        t_back = threading.Thread(target=t_back)
        t_back.setDaemon(True)
        t_back.start()

    def settings_bind(s):
        def t_settings():
            s.settings_button_disable.place(x=190,y=20)
            quickly.android_settings()
            s.settings_button_disable.place_forget()

        t_settings = threading.Thread(target=t_settings)
        t_settings.setDaemon(True)
        t_settings.start()

    def reboot_bind(s):
        def t_reboot():
            s.reboot_button_disable.place(x=20,y=60)
            s.reboot_str.set('正在重启...')
            state = quickly.android_reboot()
            # 若设备没有连接，获取的是None，则恢复正常按钮状态
            if not state:
                s.reboot_button_disable.place_forget()
            else:
                while True:
                    android_os_status = public.execute_cmd('adb shell getprop sys.boot_completed')
                    if '1' in android_os_status:
                        s.reboot_str.set('重启完成，正在等待开机...')
                        break
                time.sleep(10)
                s.reboot_button_disable.place_forget()

        t_reboot = threading.Thread(target=t_reboot)
        t_reboot.setDaemon(True)
        t_reboot.start()

    def shutdown_bind(s):
        def t_shutdown():
            s.shutdown_button_disable.place(x=190,y=60)
            quickly.android_shutdown()
            s.shutdown_button_disable.place_forget()

        t_shutdown = threading.Thread(target=t_shutdown)
        t_shutdown.setDaemon(True)
        t_shutdown.start()

    def clear_bind(s):
        def t_clear():
            s.clear_button_disable.place(x=20,y=100)
            quickly.clear_cache()
            s.clear_button_disable.place_forget()

        t_clear = threading.Thread(target=t_clear)
        t_clear.setDaemon(True)
        t_clear.start()

    def kill_bind(s):
        def t_kill():
            s.kill_button_disable.place(x=190,y=100)
            quickly.terminate_program()
            s.kill_button_disable.place_forget()

        t_kill = threading.Thread(target=t_kill)
        t_kill.setDaemon(True)
        t_kill.start()

    def desktop_bind(s):
        def t_desktop():
            s.desktop_button_disable.place(x=20,y=140)
            quickly.android_desktop()
            s.desktop_button_disable.place_forget()

        t_desktop = threading.Thread(target=t_desktop)
        t_desktop.setDaemon(True)
        t_desktop.start()

    def awake_bind(s):
        def t_awake():
            s.awake_button_disable.place(x=190,y=140)
            quickly.android_awake()
            s.awake_button_disable.place_forget()

        t_awake = threading.Thread(target=t_awake)
        t_awake.setDaemon(True)
        t_awake.start()

    def devices_bind(s):
        def t_devices():
            while True:
                # 获取设备序列号
                devices_finally = public.device_connect()
                if not devices_finally:
                    s.devices_fail.place(x=470, y=0)
                    s.devices_success.place_forget()
                    s.devices_null.set('未连接任何设备！')
                else:
                    s.devices_fail.place_forget()
                    s.devices_success.place(x=450,y=0)
                    for devices in devices_finally:
                        if len(devices_finally) == 1:
                            s.devices_str.set(devices + ' 已连接')
                        elif len(devices_finally) > 1:
                            s.devices_str.set('多部设备已连接')

        t_devices = threading.Thread(target=t_devices)
        t_devices.setDaemon(True)
        t_devices.start()

    def adb_bind(s):
        def t_adb():
            adb_finally = public.adb_connect()[1]
            if adb_finally == '不是内部或外部命令，也不是可运行的程序':
                os.chdir(adb_path)
                s.adb_str.set('内置ADB已开启！')
            else:
                s.adb_str.set('本地ADB已开启！')

        t_adb = threading.Thread(target=t_adb)
        t_adb.setDaemon(True)
        t_adb.start()

    def main_screenshot(s,touch_name):
        # 截图功能核心逻辑代码
        s.screen_str.set('正在截图中...')
        screenshot_success = screen_record.main_screenshots(touch_name)
        s.screen_str.set(screenshot_success)

    def screenshot_bind(s):
        def t_screenshot():
            s.screen_button_disable.place(x=20, y=140)
            devices_state = public.device_connect()
            touch_name = s.screen_entry.get()
            # 截图文件名长度检测
            if len(touch_name) <= 8:
                # 检测安卓系统是否完全启动，未完全启动时设备本地sdcard没显示，则提示处理；正常显示后则启动截图
                if not devices_state:
                    s.screen_str.set('请连接设备后再截图！')
                else:
                    # 创建临时文件
                    make_state = screen_record.cd_screenshots()
                    if not make_state:
                        s.main_screenshot(touch_name)
                    else:
                        make_state_finally = make_state.split(':')[-1]
                        print(make_state_finally)
                        if make_state_finally == ' No such file or directory\r\n':
                            s.screen_str.set('别着急截图，系统都还没完全启动呢...')
                        else:
                            s.main_screenshot(touch_name)
            else:
                s.screen_str.set('截图文件名过长，请重新输入！')
            s.screen_button_disable.place_forget()

        t_screenshot = threading.Thread(target=t_screenshot)
        t_screenshot.setDaemon(True)
        t_screenshot.start()

    def open_screen_bind(s):
        def open_screen():
            s.open_screen_button_disable.place(x=200,y=140)
            screen_record.open_screenshots()
            s.open_screen_button_disable.place_forget()

        open_screen = threading.Thread(target=open_screen)
        open_screen.setDaemon(True)
        open_screen.start()

    def record_stop_bind(s):
        # 停止录屏标志
        with open(record_state,'w') as fp:
            fp.write('Stop recording screen')
        with open(record_screen_state,'w') as fp:
            fp.write('Stop recording screen')

    def record_bind(s):
        def t_record():
            s.record_stop_button_disable.place_forget()
            s.record_button_disable.place(x=20,y=280)
            s.record_stop_button.place(x=200,y=280)
            # 切换到内置adb-tools路径，使录屏命令生效
            os.chdir(adb_path)
            # 获取录屏名称
            s.record_name = s.record_entry.get()
            with open(record_name,'w') as fp:
                fp.write(s.record_name)
            s.record_str.set('正在启动录屏（自动获取权限）...')
            screen_record.open_record_main()

        def record_time():
            with open(record_state, 'w') as fp:
                fp.write('')
            record_end_finally = screen_record.record_time(s.record_str)
            s.record_str.set('正在保存录屏文件，请稍等...')
            s.record_name = open(record_name,'r').read()
            screen_record.record_pull(s.record_name)
            s.record_str.set('录屏文件保存成功！录屏时间为：' + record_end_finally)
            s.record_button_disable.place_forget()
            s.record_stop_button.place_forget()
            s.record_stop_button_disable.place(x=200, y=280)

        t_record = threading.Thread(target=t_record)
        t_record.setDaemon(True)
        t_record.start()

        record_time = threading.Thread(target=record_time)
        record_time.setDaemon(True)
        record_time.start()

