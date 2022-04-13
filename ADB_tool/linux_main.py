import os,getpass
import time
import public
import tkinter
import threading

# 初始化文件路径
init_path = public.resource_path(os.path.join('resources','adb_init.ini'))
LOGO_path = public.resource_path(os.path.join('icon', 'android.ico'))
# Linux截图工具路径
gsnap_path = public.resource_path(os.path.join('resources','gsnap'))
username = getpass.getuser()
# 创建临时文件夹
make_dir = 'C:\\Users\\' + username + '\\Documents\\ADB_Tools(DA)\\'
if not os.path.exists(make_dir):
    os.makedirs(make_dir)
# 截图页面启动标志
screen_page = make_dir + 'screen_page_state.txt'
# 自定义截图保存文件夹名
linux_dirname = 'ADB工具-Linux截图（DA）'
linux_save_path = 'C:\\Users\\' + username + '\\Desktop\\' + linux_dirname + '\\'
# Linux截图计数
linux_screen_count = make_dir + 'linux_screen_count.txt'


def main_init(init_str,init_Button,init_Button_disable):
    # 检测设备核心函数
    # 设备初始化
    init_str.set('正在检测设备是否初始化...')
    # 检测该设备是否初始化
    # 检测权限文件是否存在
    check_only_read = public.execute_cmd('adb shell ls -lh /data/.overlay')
    only_read = ' '.join(check_only_read.split()).split(':')[-1]
    print(only_read)
    init_final = public.execute_cmd('adb shell cat /data/adb_init.ini')
    if init_final == 'The device initialized' and only_read != ' No such file or directory':
        init_str.set('该设备已初始化\n无需初始化，可正常使用下方功能')
    else:
        init_str.set('该设备没有初始化\n请点击下方按钮进行设备初始化')
        init_Button_disable.place_forget()
        init_Button.place(x=200, y=110)


def check_init(init_str,init_Button,init_Button_disable,devices_linux_flag,linux_all_button_close):
    def t_check_init():
        # 打印设备类型判断标记flag
        print('devices_linux_flag = ' + str(devices_linux_flag))
        devices_state = public.device_connect()
        if not devices_state:
            init_str.set('请连接设备后再进行检测')
            init_Button.place_forget()
            init_Button_disable.place(x=200, y=110)
            linux_all_button_close()
        else:
            if not devices_linux_flag:
                init_str.set('您所连接的设备为Android\n无法使用Linux模式所有功能')
                init_Button.place_forget()
                init_Button_disable.place(x=200, y=110)
            else:
                try:
                    # 中文状态下
                    adb_finally = public.adb_connect()[1]
                    # 英文状态下
                    adb_english = ' '.join(public.adb_connect()).split(',')[1]

                    # 判断是否为内置ADB，如果为内置ADB需要延迟5S，如果为本地ADB则无需延迟
                    if adb_finally == '不是内部或外部命令，也不是可运行的程序' or adb_english == ' operable program or batch file.':
                        time.sleep(5)
                        main_init(init_str, init_Button, init_Button_disable)
                    else:
                        main_init(init_str, init_Button, init_Button_disable)
                except IndexError:
                    print('出现IndexError,无需处理该异常，继续检测')
                    main_init(init_str, init_Button, init_Button_disable)
                    pass

    t_check_init = threading.Thread(target=t_check_init)
    t_check_init.setDaemon(True)
    t_check_init.start()


def devices_init(init_str,init_Button,init_Button_disable):
    def t_init():
        while True:
            devices_state = public.device_connect()
            if not devices_state:
                init_str.set('请连接设备后再进行检测')
                init_Button.place_forget()
                init_Button_disable.place(x=200, y=110)
            else:
                init_Button.place_forget()
                init_Button_disable.place(x=200, y=110)
                # 检测只读系统
                check_only_read = public.execute_cmd('adb shell ls -lh /data/.overlay')
                only_read = ' '.join(check_only_read.split()).split(':')[-1]
                print(only_read)
                if only_read == ' No such file or directory':
                    print('设备系统为只读，无法上传文件等操作')
                    init_str.set('检测到系统为只读\n正在获取权限并重启设备...')
                    public.execute_cmd('adb shell touch /data/.overlay')
                    public.execute_cmd('adb shell reboot')
                    time.sleep(15)
                    continue
                else:
                    init_str.set('设备系统已获取权限\n设备初始化完成')
                    break

        time.sleep(2)
        public.execute_cmd('adb push ' + init_path + ' /data')
        init_final = public.execute_cmd('adb shell cat /data/adb_init.ini')
        print(init_final)
        init_str.set('该设备已初始化\n无需初始化，可正常使用下方功能')

    t_init = threading.Thread(target=t_init)
    t_init.setDaemon(True)
    t_init.start()


class Linux_Screen(object):
    def screen_form(self):
        self.screen_root = tkinter.Toplevel()
        self.screen_root.title('Linux截图工具')
        screenWidth = self.screen_root.winfo_screenwidth()
        screenHeight = self.screen_root.winfo_screenheight()
        w = 300
        h = 200
        x = (screenWidth - w) / 2
        y = (screenHeight - h) / 2
        self.screen_root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.screen_root.iconbitmap(LOGO_path)
        self.screen_root.resizable(0, 0)
        self.screen_root.wm_attributes('-topmost', 1)

        self.screen_root.protocol('WM_DELETE_WINDOW',self.close_handle)
        self.main_frame()

        return self.screen_root

    def close_handle(self):
        # 监听页面消失
        with open(screen_page,'w') as fp:
            fp.write('0')
        self.screen_root.destroy()

    def main_frame(self):
        # 截图状态栏
        self.screen_str = tkinter.StringVar()
        self.screen_label = tkinter.Label(self.screen_root, textvariable=self.screen_str, bg='black', fg='#FFFFFF',
                                           width=35, height=2)
        self.screen_label.config(command=self.check_gsnap())
        self.screen_label.place(x=20, y=10)
        self.screen_str.set('此处显示截图状态')

        # 截图按钮
        self.linux_screen_button = tkinter.Button(self.screen_root, text='一键截图', width=15)
        self.linux_screen_button.bind('<Button-1>', lambda x: self.screen_main())
        self.linux_screen_button_disable = tkinter.Button(self.screen_root, text='正在截图...', width=15)
        self.linux_screen_button_disable.config(state='disable')
        self.linux_screen_button.place(x=20, y=60)

    def check_gsnap(self):
        def t_check_gsnap():
            # 检测 是否内置 gsnap 截图工具
            self.screen_str.set('正在检测是否内置截图工具...')
            check_gsnap_cmd = public.execute_cmd('adb shell gsnap')
            check_gsnap_cmd_finally = ' '.join(check_gsnap_cmd.split()).split(':')[-1]
            if check_gsnap_cmd_finally == ' not found':
                self.screen_str.set('无法找到内置截图工具，正在初始化...')
                # 内置截图工具到设备中
                public.execute_cmd('adb push ' + gsnap_path + ' /usr/bin')
                # 为内置的截图工具赋予执行权限
                public.execute_cmd('adb shell chmod a+x /usr/bin/gsnap')
                self.screen_str.set('截图工具初始化成功\n可以正常开始截图')
            else:
                self.screen_str.set('已内置gsnap截图工具\n可以正常开始截图')

        t_check_gsnap = threading.Thread(target=t_check_gsnap)
        t_check_gsnap.setDaemon(True)
        t_check_gsnap.start()

    def screen_main(self):
        # linux截图核心函数
        def t_screen():
            self.screen_str.set('正在截图中...')
            self.linux_screen_button.place_forget()
            self.linux_screen_button_disable.place(x=20, y=60)
            if not os.path.exists(linux_save_path):
                os.makedirs(linux_save_path)
            if not os.path.exists(linux_screen_count):
                with open(linux_screen_count, 'w') as fp:
                    fp.write('0')

            # 截图
            f = int(open(linux_screen_count, 'r').read())
            f += 1
            public.execute_cmd('adb shell gsnap /data/1.png /dev/fb0')
            time.sleep(1)
            pull_output = public.execute_cmd('adb pull /data/1.png ' + linux_save_path + str(f) + '.png')
            # 打印下载信息
            print(pull_output)
            self.screen_str.set('截图成功！文件保存在:\n 桌面\\' + linux_dirname + '\\' + str(f) + '.png')
            with open(linux_screen_count,'w') as fp:
                fp.write(str(f))
            self.linux_screen_button_disable.place_forget()
            self.linux_screen_button.place(x=20, y=60)

        t_screen = threading.Thread(target=t_screen)
        t_screen.setDaemon(True)
        t_screen.start()
