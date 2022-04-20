import os,getpass
import sys
import time,re,win32api
import public
import tkinter,tkinter.ttk,tkinter.messagebox
import threading
from PIL import Image

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
# 记录照片旋转角度
Image_rotate_path = make_dir + 'linux_screen_rotate.txt'
# 安装页面启动标志
install_page = make_dir + 'install_page_state.txt'


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
        init_Button.place_forget()
        init_Button_disable.place(x=200, y=110)
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
            init_str.set('正在检测设备初始化状态...')
            # 延时1秒等待flag响应
            time.sleep(1)
            device_type = public.device_type_android()
            if not devices_linux_flag and device_type.strip() == 'Android':
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


# 截图工具界面
class Linux_Screen(object):
    def screen_form(self,init_str,linux_screen_Button,linux_screen_Button_disable):
        self.screen_root = tkinter.Toplevel()
        self.screen_root.title('Linux截图工具')
        screenWidth = self.screen_root.winfo_screenwidth()
        screenHeight = self.screen_root.winfo_screenheight()
        w = 310
        h = 200
        x = (screenWidth - w) / 2
        y = (screenHeight - h) / 2
        self.screen_root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.screen_root.iconbitmap(LOGO_path)
        self.screen_root.resizable(0, 0)
        # self.screen_root.wm_attributes('-topmost', 1)

        self.screen_startup(linux_screen_Button,linux_screen_Button_disable)

        self.screen_root.protocol('WM_DELETE_WINDOW',self.close_handle)
        self.main_frame()
        self.device_monitor(init_str)

        return self.screen_root

    def screen_startup(self,linux_screen_Button,linux_screen_Button_disable):
        # 监听截图页面的打开状态
        screen_exists = self.screen_root.winfo_exists()
        print(screen_exists)
        if screen_exists == 1:
            linux_screen_Button.place_forget()
            linux_screen_Button_disable.place(x=20, y=190)

    def close_handle(self):
        # 监听页面消失
        with open(screen_page,'w') as fp:
            fp.write('0')
        self.screen_root.destroy()

    def device_monitor(self,init_str):
        # 监听设备连接状态
        while True:
            devices_state = public.device_connect()
            if not devices_state:
                init_str.set('请连接设备后再使用Linux功能！')
                self.screen_root.destroy()
                sys.exit()
            else:
                pass
            time.sleep(1)

    def main_frame(self):
        # 截图状态栏
        self.screen_str = tkinter.StringVar()
        self.screen_label = tkinter.Label(self.screen_root, textvariable=self.screen_str, bg='black', fg='#FFFFFF',
                                           width=35, height=2)
        self.screen_label.config(command=self.check_gsnap())
        self.screen_label.place(x=35, y=10)
        self.screen_str.set('此处显示截图状态')

        # 截图按钮
        self.linux_screen_button = tkinter.Button(self.screen_root, text='一键截图', width=15)
        self.linux_screen_button.bind('<Button-1>', lambda x: self.screen_main())
        self.linux_screen_button_disable = tkinter.Button(self.screen_root, text='正在截图...', width=15)
        self.linux_screen_button_disable.bind('<Button-1>', lambda x: self.linux_screen_disable_bind())
        self.linux_screen_button_disable.config(state='disable')
        self.linux_screen_button.place(x=20, y=60)

        # 选择旋转角度下拉框及标签
        content = '''请选择旋转角度：'''
        self.image_rotate_label = tkinter.Label(self.screen_root, text=content)
        self.image_rotate_label.place(x=140, y=65)
        public.CreateToolTip(self.image_rotate_label,'截图后会根据选择的角度进行旋转并保存\n旋转默认方向为逆时针')

        # 获取旋转角度默认值
        if not os.path.exists(Image_rotate_path):
            with open(Image_rotate_path,'w') as fp:
                fp.write('0')
        image_rotate_number = open(Image_rotate_path,'r').read()
        # 根据选项判断current值
        if image_rotate_number != '0':
            if image_rotate_number == '90度':
                image_rotate_number = '1'
            elif image_rotate_number == '180度':
                image_rotate_number = '2'
            elif image_rotate_number == '270度':
                image_rotate_number = '3'
            elif image_rotate_number == '360度':
                image_rotate_number = '4'
        else:
            pass

        self.image_rotate_value = tkinter.StringVar()
        self.image_rotate_combobox = tkinter.ttk.Combobox(self.screen_root, state="readonly", width=5, textvariable=self.image_rotate_value)
        # state：“正常”，“只读”或“禁用”之一。在“只读”状态下，可能无法直接编辑该值，并且用户只能从下拉列表中选择值。在“正常”状态下，文本字段可直接编辑。在“禁用”状态下，不可能进行交互。
        self.image_rotate_combobox['value'] = ('0', '90度', '180度', '270度', '360度')
        self.image_rotate_combobox.current(int(image_rotate_number))
        self.image_rotate_combobox.place(x=235, y=65)

        # 打开截图文件夹按钮
        self.open_screen_linux_button = tkinter.Button(self.screen_root, text='打开截图文件夹', width=15)
        self.open_screen_linux_button.bind('<Button-1>', lambda x: self.open_linux_screen_bind())
        self.open_screen_linux_button_disable = tkinter.Button(self.screen_root, text='正在打开...', width=15)
        self.open_screen_linux_button_disable.config(state='disable')
        self.open_screen_linux_button.place(x=20, y=100)

        # 自动打开截图（默认关闭，开启后截图后会自动打开该文件方便截图编辑，添加文字说明等等）
        self.auto_show_on = tkinter.IntVar()
        self.auto_show_checkbutton = tkinter.Checkbutton(self.screen_root,text='自动显示截图（懒人）模式',onvalue=1,offvalue=0,
                                                         variable=self.auto_show_on)
        self.auto_show_checkbutton.place(x=140,y=100)
        public.CreateToolTip(self.auto_show_checkbutton, '默认关闭，打开后会自动显示刚刚截好的图片\n方便对截图文件进行编辑和添加文件说明\n'
                                                         '针对需要对截图进行编辑的人群使用或懒人必备')

        # 截图一键重置功能
        self.linux_reset_button = tkinter.Button(self.screen_root, text='一键重置（Linux）', width=15)
        self.linux_reset_button.bind('<Button-1>', lambda x:self.linux_reset_bind())
        self.linux_reset_button_disable = tkinter.Button(self.screen_root, text='一键重置（Linux）', width=15)
        self.linux_reset_button_disable.config(state='disable')
        self.linux_reset_button_disable.bind('<Button-1>', lambda x: self.linux_reset_disable_bind())
        self.linux_reset_button.place(x=100, y=140)

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
            self.linux_reset_button.place_forget()
            self.linux_reset_button_disable.place(x=100, y=140)
            if not os.path.exists(linux_save_path):
                os.makedirs(linux_save_path)
            if not os.path.exists(linux_screen_count):
                with open(linux_screen_count, 'w') as fp:
                    fp.write('0')
            # 记录旋转角度默认值
            self.rotate_get = self.image_rotate_value.get()
            with open(Image_rotate_path, 'w') as fp:
                fp.write(self.rotate_get)

            # 截图
            f = int(open(linux_screen_count, 'r').read())
            f += 1
            public.execute_cmd('adb shell gsnap /data/1.png /dev/fb0')
            time.sleep(1)
            pull_output = public.execute_cmd('adb pull /data/1.png ' + linux_save_path + str(f) + '.png')
            # 打印下载信息
            print(pull_output)

            # 旋转截图文件
            self.screen_str.set('正在旋转截图文件并保存...')
            if self.rotate_get != '0':
                self.rotate_get = re.findall('(.*?)度',self.rotate_get)[0]
            else:
                pass
            img_path = linux_save_path + str(f) + '.png'
            img_open = Image.open(img_path)
            # expand=1 表示的是原图旋转，如果没有此参数，则内容直接旋转
            img_rotate = img_open.rotate(int(self.rotate_get), expand=1)
            # 保存旋转后的图片
            img_rotate.save(img_path)

            self.screen_str.set('截图成功！文件保存在:\n 桌面\\' + linux_dirname + '\\' + str(f) + '.png')
            with open(linux_screen_count,'w') as fp:
                fp.write(str(f))

            # 截图保存后自动打开判断
            if self.auto_show_on.get() == 1:
                self.screen_str.set('自动显示截图模式已打开\n可以进行编辑、添加文字提示')
                img_rotate.show()
                self.screen_str.set('截图已关闭\n自动显示截图说明：方便编辑图片、添加文字')
            else:
                pass

            self.linux_screen_button_disable.place_forget()
            self.linux_screen_button.place(x=20, y=60)
            self.linux_reset_button_disable.place_forget()
            self.linux_reset_button.place(x=100, y=140)

        t_screen = threading.Thread(target=t_screen)
        t_screen.setDaemon(True)
        t_screen.start()

    def linux_screen_disable_bind(self):
        tkinter.messagebox.showwarning(title='重复警告',message='已有截图任务正在进行中...\n请勿重复截图')

    def open_linux_screen_bind(self):
        # 打开Linux截图文件夹
        self.open_screen_linux_button_disable.place(x=20,y=100)
        if not os.path.exists(linux_save_path):
            os.makedirs(linux_save_path)
        win32api.ShellExecute(0, 'open', linux_save_path, '', '', 1)
        self.open_screen_linux_button_disable.place_forget()

    def linux_reset_bind(self):
        def t_linux_reset():
            linux_reset_message = """
            真的确定要一键重置 Linux截图，重置部分包括如下：
            1.将会删除Linux截图保存文件夹
            2.将会清空所有相关Linux截图工具的缓存文件
            3.将会重置Linux截图文件名计数（重置为零）
            """
            if tkinter.messagebox.askyesno(title='重置警告',message=linux_reset_message):
                filename_list = [linux_save_path,linux_screen_count,Image_rotate_path]
                public.reset_method(filename_list)
                tkinter.messagebox.showinfo(title='完成',message='一键重置完成！！！')

        t_linux_reset = threading.Thread(target=t_linux_reset)
        t_linux_reset.setDaemon(True)
        t_linux_reset.start()

    def linux_reset_disable_bind(self):
        tkinter.messagebox.showwarning(title='录屏警告',message='正在进行截图，无法重置！！！')


# 安装应用界面
class Linux_Install(object):
    def install_form(self,init_str,linux_screen_Button,linux_screen_Button_disable):
        self.install_root = tkinter.Toplevel()
        self.install_root.title('Linux一键安装工具')
        screenWidth = self.install_root.winfo_screenwidth()
        screenHeight = self.install_root.winfo_screenheight()
        w = 400
        h = 200
        x = (screenWidth - w) / 2
        y = (screenHeight - h) / 2
        self.install_root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.install_root.iconbitmap(LOGO_path)
        self.install_root.resizable(0, 0)
        # self.screen_root.wm_attributes('-topmost', 1)

        self.install_startup(linux_screen_Button,linux_screen_Button_disable)

        self.install_root.protocol('WM_DELETE_WINDOW',self.close_handle)
        self.main_frame()
        self.device_monitor(init_str)

        return self.install_root

    def install_startup(self,linux_install_Button,linux_install_Button_disable):
        # 监听安装页面的打开状态
        install_exists = self.install_root.winfo_exists()
        print(install_exists)
        if install_exists == 1:
            linux_install_Button.place_forget()
            linux_install_Button_disable.place(x=20, y=230)

    def close_handle(self):
        # 监听页面消失
        with open(install_page,'w') as fp:
            fp.write('0')
        self.install_root.destroy()

    def device_monitor(self,init_str):
        # 监听设备连接状态
        while True:
            devices_state = public.device_connect()
            if not devices_state:
                init_str.set('请连接设备后再使用Linux功能！')
                self.install_root.destroy()
                sys.exit()
            else:
                pass
            time.sleep(1)

    def main_frame(self):
        # 安装状态栏
        self.install_str = tkinter.StringVar()
        self.install_label = tkinter.Label(self.install_root, textvariable=self.install_str, bg='black', fg='#FFFFFF',
                                          width=40, height=2)
        self.install_label.place(x=55, y=10)
        self.install_str.set('此处显示安装状态')

        # 导入库标签
        self.install_library_label = tkinter.Label(self.install_root,text='导入库：')
        self.install_library_label.place(x=5,y=65)

        # 导入库输入框
        self.install_library_entry_str = tkinter.StringVar()
        self.install_library_entry = tkinter.Entry(self.install_root,textvariable=self.install_library_entry_str,width=40,highlightcolor='red'
                                           ,highlightthickness=5)
        self.install_library_entry.place(x=60,y=60)
        # 设置默认焦点
        self.install_library_entry.focus_set()

        # 导入应用标签
        self.install_software_label = tkinter.Label(self.install_root, text='导入应用：')
        self.install_software_label.place(x=5, y=95)

        # 导入应用输入框
        self.install_software_entry_str = tkinter.StringVar()
        self.install_software_entry = tkinter.Entry(self.install_root, textvariable=self.install_software_entry_str,
                                                   width=40, highlightcolor='green'
                                                   , highlightthickness=5)
        self.install_software_entry.place(x=60, y=90)

        # 显示右键菜单功能
        self.right_click_menu()

    def right_click_menu(self):
        # 右键菜单 tearoff=False 去掉分隔虚线
        self.install_right_menu = tkinter.Menu(self.install_root, tearoff=False)
        self.install_entry_list = [self.install_library_entry,self.install_software_entry]
        self.install_right_menu.add_command(label='剪切', command=lambda: public.cut(self.install_entry_list))
        self.install_right_menu.add_separator()  # add_separator() 添加分隔实线
        self.install_right_menu.add_command(label='复制', command=lambda: public.copy(self.install_entry_list))
        self.install_right_menu.add_separator()
        self.install_right_menu.add_command(label='粘贴', command=lambda: public.paste(self.install_entry_list))

        def showmenu(event):
            self.install_right_menu.post(event.x_root, event.y_root)  # 将菜单条绑定上事件，坐标为x和y的root位置

        self.install_root.bind('<Button-3>', showmenu)

