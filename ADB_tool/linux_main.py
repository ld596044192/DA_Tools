import os,getpass
import sys
import time,re,win32api,shutil,subprocess
import public,pywinauto_adb
import tkinter,tkinter.ttk,tkinter.messagebox,tkinter.filedialog
import threading,ctypes
from PIL import Image

# 初始化文件路径
init_path = public.resource_path(os.path.join('resources','adb_init.ini'))
# 初始化配置文件
camera_system_path = public.resource_path(os.path.join('resources','camera_system.ini'))
# 设置 打开取图模式后的标志路径
camera_open_path = public.resource_path(os.path.join('resources','camera_open/camera_system.ini'))
# 设置 关闭取图模式后的标志路径
camera_close_path = public.resource_path(os.path.join('resources','camera_close/camera_system.ini'))
# 看图软件路径
yuvplayer_path = public.resource_path(os.path.join('resources','yuvplayer.exe'))
LOGO_path = public.resource_path(os.path.join('icon', 'android.ico'))
# Linux截图工具路径
gsnap_path = public.resource_path(os.path.join('resources','gsnap'))
# 配置camera_system文件路径
system_path = public.resource_path(os.path.join('resources','system'))
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
# 取图保存路径
linux_camera_name = 'ADB_get_yuv'
linux_camera_save = 'C:\\Users\\' + username + '\\Desktop\\' + linux_camera_name + '\\'
# Linux截图计数
linux_screen_count = make_dir + 'linux_screen_count.txt'
# 文件夹计数
linux_camera_count = make_dir + 'linux_camera_count.txt'
# 记录照片旋转角度
Image_rotate_path = make_dir + 'linux_screen_rotate.txt'
# 安装页面启动标志
install_page = make_dir + 'install_page_state.txt'
# 取图页面启动标志
camera_page = make_dir + 'camera_page_state.txt'
# Entry输入框焦点标记（用于右键菜单粘贴逻辑使用）
install_library_entry_focus_flag = False
install_software_entry_focus_flag = False


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
        # screenWidth = self.screen_root.winfo_screenwidth()
        # screenHeight = self.screen_root.winfo_screenheight()
        w = 310
        h = 200
        # x = (screenWidth - w) / 2
        # y = (screenHeight - h) / 2
        self.screen_root.geometry('%dx%d' % (w, h))
        self.screen_root.iconbitmap(LOGO_path)
        self.screen_root.resizable(0, 0)
        # self.screen_root.wm_attributes('-topmost', 1)

        self.screen_startup(linux_screen_Button,linux_screen_Button_disable)

        self.screen_root.protocol('WM_DELETE_WINDOW',self.close_handle)
        self.main_frame()
        # self.device_monitor(init_str)

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

    # def device_monitor(self,init_str):
    #     # 监听设备连接状态
    #     while True:
    #         devices_state = public.device_connect()
    #         if not devices_state:
    #             init_str.set('请连接设备后再使用Linux功能！')
    #             self.screen_root.destroy()
    #             sys.exit()
    #         else:
    #             pass
    #         time.sleep(1)

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
        public.CreateToolTip(self.auto_show_checkbutton, '默认关闭，打开后会自动显示刚刚截好的图片\n方便对截图文件进行编辑和添加文字说明\n'
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
            devices_state = public.device_connect()
            if not devices_state:
                self.screen_str.set('连接设备后重新启动本功能检测')
            else:
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
            devices_state = public.device_connect()
            if not devices_state:
                self.screen_str.set('请重新连接设备后再截图')
            else:
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
        # screenWidth = self.install_root.winfo_screenwidth()
        # screenHeight = self.install_root.winfo_screenheight()
        w = 400
        h = 250
        # x = (screenWidth - w) / 2
        # y = (screenHeight - h) / 2
        # self.install_root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.install_root.geometry('%dx%d' % (w, h))
        self.install_root.iconbitmap(LOGO_path)
        self.install_root.resizable(0, 0)
        # self.install_root.wm_attributes('-topmost', 1)

        self.install_startup(linux_screen_Button,linux_screen_Button_disable)

        self.install_root.protocol('WM_DELETE_WINDOW',self.close_handle)
        self.main_frame()
        # self.device_monitor(init_str)

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

    # def device_monitor(self,init_str):
    #     # 监听设备连接状态
    #     while True:
    #         devices_state = public.device_connect()
    #         if not devices_state:
    #             init_str.set('请连接设备后再使用Linux功能！')
    #         else:
    #             pass
    #         time.sleep(1)

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

        # 导入库输入框 # validate="focusin"属性用于验证输入框焦点判断
        self.install_library_entry_str = tkinter.StringVar()
        self.install_library_entry = tkinter.Entry(self.install_root,textvariable=self.install_library_entry_str,width=40,highlightcolor='red'
                                           ,highlightthickness=5,validate="focusin")
        self.install_library_entry.place(x=60,y=60)
        # 获取焦点时的标记提醒
        self.install_library_entry.bind("<FocusIn>", lambda x:self.install_library_entry_flag())

        # 导入应用标签
        self.install_software_label = tkinter.Label(self.install_root, text='导入应用：')
        self.install_software_label.place(x=5, y=95)

        # 导入应用输入框
        self.install_software_entry_str = tkinter.StringVar()
        self.install_software_entry = tkinter.Entry(self.install_root, textvariable=self.install_software_entry_str,
                                                   width=40, highlightcolor='green',validate="focusin"
                                                   , highlightthickness=5)
        self.install_software_entry.place(x=60, y=90)
        # 获取焦点时的标记提醒
        self.install_software_entry.bind("<FocusIn>", lambda x: self.install_software_entry_flag())
        # 设置默认焦点
        self.install_software_entry.focus_set()

        # 打开so库文件按钮
        self.open_library_button = tkinter.Button(self.install_root,text='浏览',width=4)
        self.open_library_button_disable = tkinter.Button(self.install_root,text='浏览',width=4)
        self.open_library_button_disable.config(state='disable')
        self.open_library_button.bind('<Button-1>',lambda x: self.open_library_files())
        self.open_library_button.place(x=358,y=60)

        # 打开amr应用文件按钮
        self.open_software_button = tkinter.Button(self.install_root, text='浏览', width=4)
        self.open_software_button_disable = tkinter.Button(self.install_root, text='浏览', width=4)
        self.open_software_button_disable.config(state='disable')
        self.open_software_button.bind('<Button-1>', lambda x: self.open_software_files())
        self.open_software_button.place(x=358, y=90)

        # 库文件安装标签
        self.install_library_combobox_label = tkinter.Label(self.install_root, text='库文件安装位置：')
        self.install_library_combobox_label.place(x=5, y=125)
        public.CreateToolTip(self.install_library_combobox_label,'根据实际情况选择安装路径，否则出现问题\n备注：\n'
                                                                 'Linux默认位置：/usr/lib')

        # 安装库文件目录位置下拉框
        self.install_library_value = tkinter.StringVar()
        self.install_library_combobox = tkinter.ttk.Combobox(self.install_root, state="readonly", width=30,
                                                          textvariable=self.install_library_value)
        # state：“正常”，“只读”或“禁用”之一。在“只读”状态下，可能无法直接编辑该值，并且用户只能从下拉列表中选择值。在“正常”状态下，文本字段可直接编辑。在“禁用”状态下，不可能进行交互。
        self.install_library_combobox['value'] = ('Liunx库默认位置','dosmono指定位置 /etc/miniapp/jsapis/')
        self.install_library_combobox.current(0)
        self.install_library_combobox.place(x=110, y=125)

        # 应用包文件安装标签
        self.install_software_combobox_label = tkinter.Label(self.install_root, text='应用包安装位置：')
        self.install_software_combobox_label.place(x=5, y=155)
        public.CreateToolTip(self.install_software_combobox_label, '根据实际情况选择安装路径，否则出现问题\n备注：\n'
                                        '主程序默认安装路径：/etc/miniapp/resources/presetpkgs/8180000000000020.amr\n'
                                        '引导页默认安装路径：/etc/miniapp/resources/presetpkgs/8180000000000026.amr\n'
                                        '喜马拉雅默认安装路径：/etc/miniapp/resources/presetpkgs/8080231999314849.amr')

        # 安装应用包文件目录位置下拉框
        self.install_software_value = tkinter.StringVar()
        self.install_software_combobox = tkinter.ttk.Combobox(self.install_root, state="readonly", width=30,
                                                             textvariable=self.install_software_value)
        # state：“正常”，“只读”或“禁用”之一。在“只读”状态下，可能无法直接编辑该值，并且用户只能从下拉列表中选择值。在“正常”状态下，文本字段可直接编辑。在“禁用”状态下，不可能进行交互。
        self.install_software_combobox['value'] = ('主程序默认安装位置 ','引导页默认安装位置 ','喜马拉雅默认安装位置 ')
        self.install_software_combobox.current(0)
        self.install_software_combobox.place(x=110, y=155)

        # 安装库复选框（勾选此项会安装库）
        self.install_library_str = tkinter.IntVar()
        self.install_library_checkbutton = tkinter.Checkbutton(self.install_root, text='勾选此项安装库', onvalue=1, offvalue=0,
                                                         variable=self.install_library_str)
        self.install_library_checkbutton.place(x=60, y=185)
        public.CreateToolTip(self.install_library_checkbutton,'勾选此选项，软件安装时会把库文件导入设备中')

        # 安装应用包复选框（勾选此项会安装应用包）
        self.install_software_str = tkinter.IntVar()
        self.install_software_checkbutton = tkinter.Checkbutton(self.install_root, text='勾选此项安装应用包', onvalue=1, offvalue=0,
                                                               variable=self.install_software_str)
        self.install_software_checkbutton.place(x=200, y=185)
        public.CreateToolTip(self.install_software_checkbutton,'勾选此选项，软件安装时会把应用包文件导入设备中')
        # 安装应用包复选框默认选中
        self.install_software_checkbutton.select()

        # 一键安装按钮
        self.linux_install_button = tkinter.Button(self.install_root, text='一键安装（Linux）', width=15)
        self.linux_install_button.bind('<Button-1>', lambda x: self.linux_install_bind())
        self.linux_install_button_disable = tkinter.Button(self.install_root, text='一键安装（Linux）', width=15)
        self.linux_install_button_disable.config(state='disable')
        self.linux_install_button.place(x=130, y=215)

        # 显示右键菜单功能
        self.right_click_menu()

    def right_click_menu(self):
        # 右键菜单 tearoff=False 去掉分隔虚线
        self.install_right_menu = tkinter.Menu(self.install_root, tearoff=False)

        # 编辑控件列表
        self.install_entry_list = [self.install_library_entry,self.install_software_entry]
        self.install_right_menu.add_command(label='剪切', command=lambda: public.cut(self.install_entry_list))
        self.install_right_menu.add_separator()  # add_separator() 添加分隔实线
        self.install_right_menu.add_command(label='复制', command=lambda: public.copy(self.install_entry_list))
        self.install_right_menu.add_separator()
        self.install_right_menu.add_command(label='粘贴', command=lambda: self.install_paste())
        self.install_right_menu.add_separator()
        self.install_right_menu.add_command(label='清空', command=lambda: self.install_clear())

        def showmenu(event):
            self.install_right_menu.post(event.x_root, event.y_root)  # 将菜单条绑定上事件，坐标为x和y的root位置

        self.install_root.bind('<Button-3>', showmenu)

    def install_library_entry_flag(self):
        # 导入库输入框获取焦点标记
        global install_library_entry_focus_flag,install_software_entry_focus_flag
        install_library_entry_focus_flag = True
        install_software_entry_focus_flag = False
        print('install_library_entry获得焦点！！！')

    def install_software_entry_flag(self):
        # 导入应用包输入框获取焦点标记
        global install_software_entry_focus_flag,install_library_entry_focus_flag
        install_software_entry_focus_flag = True
        install_library_entry_focus_flag = False
        print('install_software_entry获得焦点！！！')

    def install_paste(self):
        # 粘贴功能的逻辑实现（需要根据焦点获取决定粘贴的组件对象）
        if install_library_entry_focus_flag:
            # install_library_entry获取焦点时要绑定的事件
            self.install_library_entry.event_generate('<<Paste>>')
        elif install_software_entry_focus_flag:
            # install_software_entry获取焦点时要绑定的事件
            self.install_software_entry.event_generate('<<Paste>>')

    def install_clear(self):
        # 清空功能的逻辑实现（需要根据焦点获取决定清空的组件对象）
        if install_library_entry_focus_flag:
            self.install_library_entry_str.set('')
        elif install_software_entry_focus_flag:
            self.install_software_entry_str.set('')

    def open_library_files(self):
        def t_open_library_file():
            # 打开库文件代码
            self.open_library_button_disable.place(x=358,y=60)
            self.open_software_button_disable.place(x=358, y=90)
            library_file = tkinter.filedialog.askopenfile(mode='r', filetypes=[('So Files', '*.so')], title='选择库安装文件')
            library_file_string = str(library_file)
            if not library_file:
                self.install_str.set('没有成功选择库文件\n请重新选择库文件')
            else:
                library_file_finally = eval(library_file_string.split()[1].split('=')[1])
                self.install_library_entry_str.set(library_file_finally)
                print(library_file_finally)
            self.open_library_button_disable.place_forget()
            self.open_software_button_disable.place_forget()

        t_open_library_file = threading.Thread(target=t_open_library_file)
        t_open_library_file.setDaemon(True)
        t_open_library_file.start()

    def open_software_files(self):
        def t_open_software_file():
            # 打开应用包文件代码
            self.open_library_button_disable.place(x=358, y=60)
            self.open_software_button_disable.place(x=358,y=90)
            software_file = tkinter.filedialog.askopenfile(mode='r', filetypes=[('Amr Files', '*.amr')], title='选择应用包安装文件')
            software_file_string = str(software_file)
            if not software_file:
                self.install_str.set('没有成功选择应用包文件\n请重新选择应用包文件')
            else:
                software_file_finally = eval(software_file_string.split()[1].split('=')[1])
                self.install_software_entry_str.set(software_file_finally)
                print(software_file_finally)
            self.open_software_button_disable.place_forget()
            self.open_library_button_disable.place_forget()

        t_open_software_file = threading.Thread(target=t_open_software_file)
        t_open_software_file.setDaemon(True)
        t_open_software_file.start()

    def linux_install_bind(self):
        def t_linux_install():
            # 安装软件核心代码
            self.linux_install_button_disable.place(x=130,y=215)
            # 运行前需要检测是否连接设备
            devices_state = public.device_connect()
            if not devices_state:
                self.install_str.set('检测到没有连接到设备\n请连接设备后再使用本功能')
            else:
                self.install_str.set('正在开始安装应用...')

                if self.install_library_str.get() == 0 and self.install_software_str.get() == 0:
                    # 两个复选框都没选
                    self.install_str.set('安装库和应用包请任意勾选其中一项\n两者选项至少勾选一项')
                    tkinter.messagebox.showwarning(title='安装错误',message='请勾选安装库和应用包其中一项，两者至少勾选一项')
                else:
                    # 各项异常处理
                    if self.install_library_entry_str.get() == '' and self.install_software_entry_str.get() == '':
                        self.install_str.set('安装库文件或应用包为空\n无法成功安装应用')
                        tkinter.messagebox.showwarning(title='安装错误', message='请选择正确的库文件或应用包后再重新安装！')
                    elif self.install_library_entry_str.get() == '' and self.install_library_str.get() == 1:
                        self.install_str.set('安装库文件失败\n请选择库文件后再重新安装！')
                        tkinter.messagebox.showwarning(title='安装错误', message='请选择库文件后再重新安装！')
                    elif self.install_software_entry_str.get() == '' and self.install_software_str.get() == 1:
                        self.install_str.set('安装应用包文件失败\n请选择应用包文件后再重新安装！')
                        tkinter.messagebox.showwarning(title='安装错误', message='请选择应用包文件后再重新安装！')
                    else:
                        # 安装库
                        if self.install_library_str.get() == 1:
                            self.install_str.set('正在导入库...')
                            library_files_path = self.install_library_entry_str.get()
                            if self.install_library_value.get().strip() == 'Liunx库默认位置':
                                public.execute_cmd('adb push ' + library_files_path + ' /usr/lib')
                                print(library_files_path + '已上传')
                            elif self.install_library_value.get().strip() == 'dosmono指定位置 /etc/miniapp/jsapis/':
                                public.execute_cmd('adb push ' + library_files_path + ' /etc/miniapp/jsapis/')
                                print(library_files_path + '已上传')

                        # 安装应用包
                        if self.install_software_str.get() == 1:
                            self.install_str.set('正在导入应用包..')
                            software_files_path = self.install_software_entry_str.get()
                            if self.install_software_value.get().strip() == '主程序默认安装位置':
                                public.execute_cmd('adb push ' + software_files_path +
                                                                           ' /etc/miniapp/resources/presetpkgs/8180000000000020.amr')
                                print(software_files_path + '已上传')
                            elif self.install_software_value.get().strip() == '引导页默认安装位置':
                                public.execute_cmd('adb push ' + software_files_path +
                                                                           ' /etc/miniapp/resources/presetpkgs/8180000000000026.amr')
                            elif self.install_software_value.get().strip() == '喜马拉雅默认安装位置':
                                public.execute_cmd('adb push ' + software_files_path +
                                                   ' /etc/miniapp/resources/presetpkgs/8080231999314849.amr')
                                print(software_files_path + '已上传')

                        # 安装后需要清理缓存
                        self.install_str.set('正在清理缓存并重启设备..')
                        public.execute_cmd('adb shell rm -rf /data/miniapp/data')

                        # 重启
                        public.execute_cmd('adb shell reboot')
                        self.install_str.set('安装应用完成\n等待设备重启后使用即可')

            self.linux_install_button_disable.place_forget()

        t_linux_install = threading.Thread(target=t_linux_install)
        t_linux_install.setDaemon(True)
        t_linux_install.start()


# 获取扫描帧数图片界面
class Linux_Camera(object):
    def camera_form(self,init_str,linux_camera,linux_camera_disable):
        self.camera_root = tkinter.Toplevel()
        self.camera_root.title('Linux获取扫描帧数图片工具')
        # screenWidth = self.install_root.winfo_screenwidth()
        # screenHeight = self.install_root.winfo_screenheight()
        w = 350
        h = 200
        # x = (screenWidth - w) / 2
        # y = (screenHeight - h) / 2
        # self.install_root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.camera_root.geometry('%dx%d' % (w, h))
        self.camera_root.iconbitmap(LOGO_path)
        self.camera_root.resizable(0, 0)
        # self.install_root.wm_attributes('-topmost', 1)

        self.camera_startup(linux_camera,linux_camera_disable)
        #
        self.camera_root.protocol('WM_DELETE_WINDOW',self.close_handle)
        self.main_frame(linux_camera_disable)

        return self.camera_root

    def camera_startup(self,linux_camera,linux_camera_disable):
        # 监听取图页面的打开状态
        camera_exists = self.camera_root.winfo_exists()
        print(camera_exists)
        if camera_exists == 1:
            linux_camera.place_forget()
            linux_camera_disable.place(x=20, y=270)

    def close_handle(self):
        # 监听页面消失
        with open(camera_page,'w') as fp:
            fp.write('0')
        self.camera_root.destroy()

    def main_frame(self,linux_camera_disable):
        # 获取图片状态栏
        self.camera_str = tkinter.StringVar()
        self.camera_label = tkinter.Label(self.camera_root, textvariable=self.camera_str, bg='black', fg='#FFFFFF',
                                           width=40, height=2)
        self.camera_label.place(x=30, y=10)
        self.camera_label.config(command=self.check_system(linux_camera_disable))
        self.camera_str.set('此处显示获取图片状态')

        # 开启取图模式按钮
        self.take_image_mode_close = False
        self.linux_camera_button = tkinter.Button(self.camera_root, text='开启取图模式', width=15)
        self.linux_camera_button.bind('<Button-1>', lambda x: self.open_camera_bind())
        self.linux_camera_button.place(x=30, y=60)
        self.linux_camera_button_disable = tkinter.Button(self.camera_root, text='开启取图模式', width=15)
        self.linux_camera_button_disable_open = tkinter.Button(self.camera_root, text='正在开启中...', width=15)
        self.linux_camera_button_disable_final = tkinter.Button(self.camera_root, text='取图模式已打开', width=15)
        self.linux_camera_button_disable_open.config(state='disable')
        self.linux_camera_button_disable.config(state='disable')
        self.linux_camera_button_disable_final.config(state='disable')

        # 关闭取图模式按钮
        self.linux_camera_button_close = tkinter.Button(self.camera_root, text='关闭取图模式', width=15)
        self.linux_camera_button_close.bind('<Button-1>', lambda x: self.close_camera_bind())
        self.linux_camera_button_close_disable = tkinter.Button(self.camera_root, text='关闭取图模式', width=15)
        self.linux_camera_button_close_disable_open = tkinter.Button(self.camera_root, text='正在关闭中...', width=15)
        self.linux_camera_button_close_disable_final = tkinter.Button(self.camera_root, text='取图模式已关闭', width=15)
        self.linux_camera_button_close_disable_open.config(state='disable')
        self.linux_camera_button_close_disable.config(state='disable')
        self.linux_camera_button_close_disable_final.config(state='disable')
        self.linux_camera_button_close.place(x=200, y=60)

        # 先禁用按钮
        self.linux_camera_button_disable.place(x=30, y=60)
        self.linux_camera_button_close_disable.place(x=200, y=60)

        # 一键取图按钮
        self.linux_get_camera_button = tkinter.Button(self.camera_root, text='一键取图', width=15)
        self.linux_get_camera_button.bind('<Button-1>',lambda x:self.camera_pywinauto_main())
        self.linux_get_camera_button_disable_final = tkinter.Button(self.camera_root, text='正在取图中...', width=15)
        self.linux_get_camera_button_disable = tkinter.Button(self.camera_root, text='一键取图', width=15)
        self.linux_get_camera_button_disable.config(state='disable')
        self.linux_get_camera_button_disable_final.config(state='disable')
        self.linux_get_camera_button.place(x=30,y=100)

        # 先禁用按钮
        self.linux_get_camera_button_disable.place(x=30, y=100)

        # 自动化看图功能复选框
        self.linux_camera_str = tkinter.IntVar()
        self.linux_camera_checkbutton = tkinter.Checkbutton(self.camera_root, text='自动化看图功能', onvalue=1, offvalue=0,
                                                               variable=self.linux_camera_str)
        self.linux_camera_checkbutton.place(x=200, y=100)
        public.CreateToolTip(self.linux_camera_checkbutton, '默认开启，开启后将会自动化打开软件进行查看yuv图片文件\n'
                                                            '具体流程：主要把origin_320X240.yuv用yuvplayer.exe进行打开查看\n'
                                                            '自动化过程中，请勿操作其他软件，否则容易出现异常\n'
                                                            '适用于懒人必备功能或避免过多重复性动作造成时间浪费')
        self.linux_camera_checkbutton.select()

    def check_system(self,linux_camera_disable):
        def t_check_system():
            # 检测 是否配置 适用于取图的system文件
            self.camera_str.set('正在检测是否配置system文件...')
            check_system_cmd = public.execute_cmd('adb shell ls -lh /data/camera_system.ini')
            check_system_cmd_finally = ' '.join(check_system_cmd.split()).split(':')[-1]
            print(check_system_cmd_finally)
            if check_system_cmd_finally.strip() == 'No such file or directory':
                message = '配置取图功能需要重启多次，是否继续？\n点击“取消”则会关闭此页面！'
                if tkinter.messagebox.askokcancel(title='温馨提示', message=message):
                    self.camera_str.set('检测没有配置过system，正在初始化...')
                    # 内置取图配置文件到设备中
                    public.execute_cmd('adb push ' + system_path + ' /etc/config/uci/system')
                    public.execute_cmd('adb push ' + camera_system_path + ' /data/')
                    # 需要重启生效
                    public.execute_cmd('adb shell reboot')
                    time.sleep(18)
                    self.camera_str.set('取图工具初始化成功\n请点击“开启取图模式”按钮开启')

                    # 开放按钮
                    self.linux_camera_button_disable.place_forget()

                else:
                    self.camera_root.destroy()
                    linux_camera_disable.place_forget()
            else:
                self.camera_str.set('已内置system配置文件\n可以开始使用取图功能')
                take_image_mode_info = public.execute_cmd('adb shell cat /data/camera_system.ini')
                if take_image_mode_info.strip() == 'Take image mode on':
                    self.camera_str.set('取图模式已打开\n可以取图啦~')
                    self.linux_camera_button_disable.place_forget()
                    self.linux_camera_button_close_disable.place_forget()
                    self.linux_camera_button_close_disable_final.place_forget()
                    self.linux_camera_button_close.place(x=200,y=60)
                    self.linux_camera_button_disable_final.place(x=30,y=60)
                    self.linux_get_camera_button_disable.place_forget()
                else:
                    self.camera_str.set('取图模式已关闭\n请重新开启取图模式')
                    self.linux_camera_button_disable_final.place_forget()
                    self.linux_camera_button_close_disable.place_forget()
                    self.linux_camera_button_disable.place_forget()
                    self.linux_camera_button_close_disable_final.place(x=200,y=60)
                    self.linux_get_camera_button_disable.place(x=30, y=100)

        t_check_system = threading.Thread(target=t_check_system)
        t_check_system.setDaemon(True)
        t_check_system.start()

    def open_camera_bind(self):
        def t_open_camera():
            # 开启取图模式
            self.take_image_mode_close = False
            # 设置 打开取图模式后的标志
            public.execute_cmd('adb push ' + camera_open_path + ' /data/')
            self.main_camera_bind(self.take_image_mode_close)

        t_open_camera = threading.Thread(target=t_open_camera)
        t_open_camera.setDaemon(True)
        t_open_camera.start()

    def close_camera_bind(self):
        def t_close_camera():
            # 关闭取图模式
            # 取图模式标志
            self.take_image_mode_close = True
            # 设置 打开取图模式后的标志
            public.execute_cmd('adb push ' + camera_close_path + ' /data/')
            self.main_camera_bind(self.take_image_mode_close)

        t_close_camera = threading.Thread(target=t_close_camera)
        t_close_camera.setDaemon(True)
        t_close_camera.start()

    def main_camera_bind(self,take_image_mode_close):
        def t_main_camera():
            # 取图模式核心流程
            if take_image_mode_close:
                self.linux_camera_button_close_disable_open.place(x=200, y=60)
                # 设置取图模式为False (关闭取图模式)
                self.camera_str.set('正在关闭取图模式并重启...')
                public.execute_cmd('adb shell uci set system.algo_imageParameter.isSaveOriginalImage=false')
            else:
                self.linux_camera_button_disable_open.place(x=30, y=60)
                # 设置取图模式为True (开启取图模式)
                self.camera_str.set('正在启动取图模式并重启...')
                public.execute_cmd('adb shell uci set system.algo_imageParameter.isSaveOriginalImage=true')
            # 上传到system
            public.execute_cmd('adb shell uci commit system')
            # 重启
            public.execute_cmd('adb shell reboot')
            time.sleep(18)
            if take_image_mode_close:
                self.camera_str.set('取图模式已关闭\n请重新开启取图模式')
                self.linux_camera_button_close_disable_open.place_forget()
                self.linux_camera_button_close_disable_final.place(x=200, y=60)
                self.linux_camera_button_disable_final.place_forget()
                self.linux_get_camera_button_disable.place(x=30,y=100)
            else:
                self.camera_str.set('取图模式已打开\n可以取图啦~')
                self.linux_camera_button_disable_open.place_forget()
                self.linux_camera_button_close_disable.place_forget()
                self.linux_camera_button_disable_final.place(x=30,y=60)
                self.linux_camera_button_close_disable_final.place_forget()
                self.linux_get_camera_button_disable.place_forget()

        t_main_camera = threading.Thread(target=t_main_camera)
        t_main_camera.setDaemon(True)
        t_main_camera.start()

    def camera_pywinauto_main(self):
        def t_camera_pywinauto():
            # 取图核心主流程
            self.linux_get_camera_button_disable_final.place(x=30,y=100)
            self.camera_str.set('正在检查取图环境...')
            if not os.path.exists(linux_camera_save):
                os.makedirs(linux_camera_save)
            # 检查yuvplayer.exe看图工具是否存在
            yuvplayer_exist = linux_camera_save + 'yuvplayer.exe'
            if not os.path.exists(yuvplayer_exist):
                shutil.copy(yuvplayer_path,yuvplayer_exist)
            self.camera_str.set('取图环境初始化成功\n正在取图中...')
            self.camera_str.set('正在取图中...\n请耐心等待...')
            if not os.path.exists(linux_camera_count):
                with open(linux_camera_count, 'w') as fp:
                    fp.write('0')
            f = int(open(linux_camera_count, 'r').read())
            f += 1
            get_yuv_path = linux_camera_save + 'get_yuv' + str(f)
            # 取图到指定位置
            command = 'adb  pull /tmp/yuv_data ' + get_yuv_path
            # yuv_download = public.execute_cmd('adb  pull /tmp/yuv_data ' + get_yuv_path)
            # print(yuv_download)
            p = subprocess.Popen(command, shell=False, stdout=(subprocess.PIPE), stderr=(subprocess.STDOUT))
            # 开启窗口置顶
            self.camera_root.wm_attributes('-topmost', 1)
            while p.poll() is None:
                line = p.stdout.readline().decode('utf8').split('/')[0].split(']')[0].split('[')
                line1 = ''.join(''.join(line).split())
                line_re = re.findall('(.*?)%', line1)
                print(line_re)
                for i in line_re:
                    print('取图yuv文件正在下载:' + str(i) + '%')
                    self.camera_str.set('取图yuv文件正在下载:' + str(i) + '%\n请耐心等待...')
            # 取消窗口置顶
            self.camera_root.wm_attributes('-topmost', 0)
            if self.linux_camera_str.get() == 1:
                # 判断文件夹中是否含有origin_320X240.yuv，得出目标地址
                yuv_path_dir = []
                yuv_dirs = public.get_dirs(get_yuv_path)
                print(yuv_dirs)
                for yuv_dir_path in yuv_dirs:
                    try:
                        yuv_files = public.get_files(yuv_dir_path)
                        print(yuv_files)
                        if 'origin_320X240.yuv' in yuv_files:
                            yuv_dir_path_select = yuv_dir_path
                            print(yuv_dir_path_select)
                            yuv_path_dir.append(yuv_dir_path_select)
                            print('已检测到 ' + yuv_dir_path_select + '\\origin_320X240.yuv')

                            # 自动化执行
                            self.camera_str.set('正在执行自动化操作...\n温馨提示:自动化过程中勿操作其他')
                            pywinauto_yuv = pywinauto_adb.Carmera()  # 实例化对象
                            pywinauto_yuv.carmera_automation(yuvplayer_exist, yuv_path_dir[0])
                            # 清理yuv文件缓存
                            self.camera_str.set('正在清理yuv文件缓存...')
                            public.execute_cmd('adb shell rm -rf /tmp/yuv_data/ping/*.yuv')
                            public.execute_cmd('adb shell rm -rf /tmp/yuv_data/pong/*.yuv')
                            self.camera_str.set('取图完成！！！\n下次取图前请先关闭看图软件')
                            break
                        else:
                            self.camera_str.set('取图失败，没有找到origin_320X240.yuv\n无法进行自动化操作，请重新扫描后再次取图！')
                            break
                    except TypeError:
                        print('检测到此文件夹为空！')
                        self.camera_str.set('取图失败，没有找到get_yuv文件夹\n无法继续进行取图，请重新扫描后再次取图！')

            # 存储计数
            with open(linux_camera_count, 'w') as fp:
                fp.write(str(f))
            self.linux_get_camera_button_disable_final.place_forget()

        t_camera_pywinauto = threading.Thread(target=t_camera_pywinauto)
        t_camera_pywinauto.setDaemon(True)
        t_camera_pywinauto.start()
