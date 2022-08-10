import os,getpass
import sys
import time,re,win32api,shutil,subprocess
import public,pywinauto_adb
import tkinter,tkinter.ttk,tkinter.messagebox,tkinter.filedialog
import threading,ctypes
from PIL import Image
from pynput.keyboard import Key, Controller

# 初始化文件路径
init_path = public.resource_path(os.path.join('resources','adb_init.ini'))
# 初始化配置文件
camera_system_path = public.resource_path(os.path.join('resources','camera_system.ini'))
# 设置 打开取图模式后的标志路径
camera_open_path = public.resource_path(os.path.join('resources','camera_open/camera_system.ini'))
# 设置 关闭取图模式后的标志路径
camera_close_path = public.resource_path(os.path.join('resources','camera_close/camera_system.ini'))
# 写号结果日志路径
SN_result_path = public.resource_path(os.path.join('temp','SN_result.log'))
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
# 自定义日志保存文件夹名
linux_dirname_log = 'ADB_get_log(DA)'
linux_log_path = 'C:\\Users\\' + username + '\\Desktop\\' + linux_dirname_log + '\\'
# 取图保存路径
linux_camera_name = 'ADB_get_yuv'
linux_camera_save = 'C:\\Users\\' + username + '\\Desktop\\' + linux_camera_name + '\\'
# Linux截图计数
linux_screen_count = make_dir + 'linux_screen_count.txt'
# 取图文件夹计数
linux_camera_count = make_dir + 'linux_camera_count.txt'
# 记录照片旋转角度
Image_rotate_path = make_dir + 'linux_screen_rotate.txt'
# 安装页面启动标志
install_page = make_dir + 'install_page_state.txt'
# 取图页面启动标志
camera_page = make_dir + 'camera_page_state.txt'
# 写号工具页面启动标志
write_number_page = make_dir + 'linux_write_number_state.txt'
# 一键获取日志页面启动标志
get_log_page = make_dir + 'get_log_state.txt'
# 写号工具记录log
write_SN_log = make_dir + 'write_SN_log.log'
# SN号记录标记
SN_path = make_dir + 'SN.txt'
# 实时保存设备序列号
devices_log = make_dir + 'devices.log'
# Entry输入框焦点标记（用于右键菜单粘贴逻辑使用）
install_library_entry_focus_flag = False
install_software_entry_focus_flag = False
# 限制截图提示弹框标记
screen_click_flag = False
# 限制截图重置提示弹框标记
screen_reset_flag = False
# 实例化键盘对象
keyboard = Controller()
# 初始化写号工具记录log
if not os.path.exists(write_SN_log):
    with open(write_SN_log,'w') as fp:
        fp.write('')


def main_init(init_str,init_Button,init_Button_disable,device):
    # 检测设备核心函数
    # 设备初始化
    init_str.set('正在检测设备是否初始化...')
    # 检测该设备是否初始化
    # 检测权限文件是否存在
    only_read = public.linux_only_read(device)
    # init_final = public.execute_cmd('adb -s ' + device + ' shell cat /data/adb_init.ini')
    # if init_final == 'The device initialized' and only_read != ' No such file or directory':
    if only_read.strip() != 'No such file or directory':
        init_str.set('该设备已初始化\n无需初始化，可正常使用下方功能')
        init_Button.place_forget()
        init_Button_disable.place(x=200, y=110)
    else:
        init_str.set('该设备没有初始化\n请点击下方按钮进行设备初始化')
        init_Button_disable.place_forget()
        init_Button.place(x=200, y=110)


def check_init(init_str,init_Button,init_Button_disable,devices_linux_flag,linux_all_button_close,device):
    def t_check_init():
        init_str.set('正在检测设备初始化状态...')
        # 打印设备类型判断标记flag
        print('devices_linux_flag = ' + str(devices_linux_flag))
        devices_state = public.device_connect()
        if not devices_state:
            init_str.set('请连接设备后再进行检测')
            init_Button.place_forget()
            init_Button_disable.place(x=200, y=110)
            linux_all_button_close()
        else:
            # 延时1秒等待flag响应
            time.sleep(1)
            device_type = public.device_type_android(device)
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
                        main_init(init_str, init_Button, init_Button_disable,device)
                    else:
                        main_init(init_str, init_Button, init_Button_disable,device)
                except IndexError:
                    print('出现IndexError,无需处理该异常，继续检测')
                    main_init(init_str, init_Button, init_Button_disable,device)
                    pass

    t_check_init = threading.Thread(target=t_check_init)
    t_check_init.setDaemon(True)
    t_check_init.start()


def devices_init(init_str,init_Button,init_Button_disable,device):
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
                check_only_read = public.execute_cmd('adb -s ' + device + ' shell ls -lh /data/.overlay')
                only_read = ' '.join(check_only_read.split()).split(':')[-1]
                print(only_read)
                if only_read == ' No such file or directory':
                    print('设备系统为只读，无法上传文件等操作')
                    init_str.set('检测到系统为只读\n正在获取权限并重启设备...')
                    public.execute_cmd('adb -s ' + device + ' shell touch /data/.overlay')
                    public.execute_cmd('adb -s ' + device + ' shell reboot')
                    time.sleep(15)
                    continue
                else:
                    init_str.set('设备系统已获取权限\n设备初始化完成')
                    break

        time.sleep(2)
        public.execute_cmd('adb  -s ' + device + ' push ' + init_path + ' /data')
        init_final = public.execute_cmd('adb -s ' + device + ' shell cat /data/adb_init.ini')
        print(init_final)
        init_str.set('该设备已初始化\n无需初始化，可正常使用下方功能')

    t_init = threading.Thread(target=t_init)
    t_init.setDaemon(True)
    t_init.start()


# 截图工具界面
class Linux_Screen(object):
    def screen_form(self,init_str,linux_screen_Button,linux_screen_Button_disable,device):
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
        self.main_frame(device)
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

    def main_frame(self,device):
        # 截图状态栏
        self.screen_str = tkinter.StringVar()
        self.screen_label = tkinter.Label(self.screen_root, textvariable=self.screen_str, bg='black', fg='#FFFFFF',
                                           width=35, height=2)
        self.screen_label.config(command=self.check_gsnap(device))
        self.screen_label.place(x=35, y=10)
        self.screen_str.set('此处显示截图状态')

        # 截图按钮
        self.linux_screen_button = tkinter.Button(self.screen_root, text='一键截图', width=15)
        self.linux_screen_button.bind('<Button-1>', lambda x: self.screen_main(device))
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

    def check_gsnap(self,device):
        def t_check_gsnap():
            devices_state = public.device_connect()
            if not devices_state:
                self.screen_str.set('连接设备后重新启动本功能检测')
            else:
                # 检测 是否内置 gsnap 截图工具
                self.screen_str.set('正在检测是否内置截图工具...')
                check_gsnap_cmd = public.execute_cmd('adb -s ' + device + ' shell gsnap')
                check_gsnap_cmd_finally = ' '.join(check_gsnap_cmd.split()).split(':')[-1]
                if check_gsnap_cmd_finally == ' not found':
                    self.screen_str.set('无法找到内置截图工具，正在初始化...')
                    # 内置截图工具到设备中
                    public.execute_cmd('adb -s ' + device + ' push ' + gsnap_path + ' /usr/bin')
                    # 为内置的截图工具赋予执行权限
                    public.execute_cmd('adb -s ' + device + ' shell chmod a+x /usr/bin/gsnap')
                    self.screen_str.set('截图工具初始化成功\n可以正常开始截图')
                else:
                    self.screen_str.set('已内置gsnap截图工具\n可以正常开始截图')

        t_check_gsnap = threading.Thread(target=t_check_gsnap)
        t_check_gsnap.setDaemon(True)
        t_check_gsnap.start()

    def screen_main(self,device):
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
                only_read = public.linux_only_read(device)
                if only_read == ' No such file or directory':
                    self.screen_str.set('检测该设备没有初始化\n请重新初始化后才能使用本功能')
                else:
                    devices = open(devices_log, 'r').read()
                    device_type = public.device_type_android(devices)
                    if device_type.strip() == 'Android':
                        self.screen_str.set('您所连接的设备为Android\n无法使用截图功能')
                    else:
                        check_gsnap_cmd = public.execute_cmd('adb -s ' + device + ' shell gsnap')
                        check_gsnap_cmd_finally = ' '.join(check_gsnap_cmd.split()).split(':')[-1]
                        if check_gsnap_cmd_finally == ' not found':
                            self.check_gsnap(device)
                        else:
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
                            public.execute_cmd('adb -s ' + device + ' shell gsnap /data/1.png /dev/fb0')
                            time.sleep(2)
                            pull_output = public.execute_cmd('adb -s ' + device + ' pull /data/1.png ' + linux_save_path + str(f) + '.png')
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
                                # 开启窗口置顶
                                self.screen_root.wm_attributes('-topmost', 1)
                                img_rotate.show()
                                # 关闭窗口置顶
                                self.screen_root.wm_attributes('-topmost', 0)
                                self.screen_str.set('截图已关闭\n自动显示截图说明：方便编辑图片、添加文字')
                            else:
                                pass

                            # 删除截图缓存
                            public.execute_cmd('adb -s ' + device + ' shell rm -rf /data/1.png')
            self.linux_screen_button_disable.place_forget()
            self.linux_screen_button.place(x=20, y=60)
            self.linux_reset_button_disable.place_forget()
            self.linux_reset_button.place(x=100, y=140)

        t_screen = threading.Thread(target=t_screen)
        t_screen.setDaemon(True)
        t_screen.start()

    def linux_screen_disable_bind(self):
        # 限制弹出框次数为1，防止每次点击都弹出新的对话框
        global screen_click_flag
        if not screen_click_flag:
            screen_click_flag = True
            tkinter.messagebox.showwarning(title='重复警告',message='已有截图任务正在进行中...\n请勿重复截图')
            screen_click_flag = False
        else:
            pass

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
        # 限制弹出框次数为1，防止每次点击都弹出新的对话框
        global screen_reset_flag
        if not screen_reset_flag:
            screen_reset_flag = True
            tkinter.messagebox.showwarning(title='重置警告',message='正在进行截图，无法重置！！！')
            screen_reset_flag = False
        else:
            pass


# 安装应用界面
class Linux_Install(object):
    def install_form(self,init_str,linux_screen_Button,linux_screen_Button_disable,device):
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
        self.main_frame(device)
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

    def main_frame(self,device):
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
        self.install_library_combobox['value'] = ('Liunx库默认位置','dosmono指定位置 /etc/miniapp/jsapis/','牛津词典指定位置 /etc/miniapp/jsapis/')
        self.install_library_combobox.current(0)
        self.install_library_combobox.place(x=110, y=125)

        # 应用包文件安装标签
        self.install_software_combobox_label = tkinter.Label(self.install_root, text='应用包安装位置：')
        self.install_software_combobox_label.place(x=5, y=155)
        public.CreateToolTip(self.install_software_combobox_label, '根据实际情况选择安装路径，否则出现问题\n备注：\n'
                                        '主程序默认安装路径：/etc/miniapp/resources/presetpkgs/8180000000000020.amr\n'
                                        '引导页默认安装路径：/etc/miniapp/resources/presetpkgs/8180000000000026.amr\n'
                                        '喜马拉雅默认安装路径：/etc/miniapp/resources/presetpkgs/8080231999314849.amr\n'
                                        '牛津词典默认安装路径：/etc/miniapp/resources/presetpkgs/8080251822789980.amr')

        # 安装应用包文件目录位置下拉框
        self.install_software_value = tkinter.StringVar()
        self.install_software_combobox = tkinter.ttk.Combobox(self.install_root, state="readonly", width=30,
                                                             textvariable=self.install_software_value)
        # state：“正常”，“只读”或“禁用”之一。在“只读”状态下，可能无法直接编辑该值，并且用户只能从下拉列表中选择值。在“正常”状态下，文本字段可直接编辑。在“禁用”状态下，不可能进行交互。
        self.install_software_combobox['value'] = ('主程序默认安装位置 ','引导页默认安装位置 ','喜马拉雅默认安装位置 ','牛津词典默认安装位置 ')
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
        self.linux_install_button.bind('<Button-1>', lambda x: self.linux_install_bind(device))
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
            # print('获取地址：' + str(library_file))
            library_file_string = str(library_file)
            if not library_file:
                self.install_str.set('没有成功选择库文件\n请重新选择库文件')
            else:
                # replace('/','\\')替换路径符号，提高最准确无误的文件绝对路径
                library_file_finally = eval(library_file_string.split()[1].split('=')[1]).replace('/','\\')
                self.install_library_entry_str.set(library_file_finally)
                print('获取地址：' + str(library_file_finally))
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
            print(software_file_string)
            if not software_file:
                self.install_str.set('没有成功选择应用包文件\n请重新选择应用包文件')
            else:
                try:
                    software_file_finally = eval(software_file_string.split()[1].split('=')[1]).replace('/','\\')
                except SyntaxError:
                    software_file_finally = software_file_string.split("'")[1]
                self.install_software_entry_str.set(software_file_finally)
                print(software_file_finally)
            self.open_software_button_disable.place_forget()
            self.open_library_button_disable.place_forget()

        t_open_software_file = threading.Thread(target=t_open_software_file)
        t_open_software_file.setDaemon(True)
        t_open_software_file.start()

    def linux_install_bind(self,device):
        def t_linux_install():
            # 安装软件核心代码
            self.linux_install_button_disable.place(x=130,y=215)
            # 运行前需要检测是否连接设备
            devices_state = public.device_connect()
            if not devices_state:
                self.install_str.set('检测到没有连接到设备\n请连接设备后再使用本功能')
            else:
                only_read = public.linux_only_read(device)
                if only_read == ' No such file or directory':
                    self.install_str.set('检测该设备没有初始化\n请重新初始化后才能使用本功能')
                else:
                    devices = open(devices_log, 'r').read()
                    device_type = public.device_type_android(devices)
                    if device_type.strip() == 'Android':
                        self.install_str.set('您所连接的设备为Android\n无法使用安装应用功能')
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
                                        main_result = public.execute_cmd('adb -s ' + device + ' push ' + '"' + library_files_path + '"' + ' /usr/lib')
                                        print(main_result)
                                        print(library_files_path + ' 已上传')
                                    elif self.install_library_value.get().strip() == 'dosmono指定位置 /etc/miniapp/jsapis/' or \
                                        self.install_library_value.get().strip() == '牛津词典指定位置 /etc/miniapp/jsapis/':
                                        main_result = public.execute_cmd('adb -s ' + device + ' push ' + '"' + library_files_path + '"' + ' /etc/miniapp/jsapis/')
                                        print(main_result)
                                        print(library_files_path + ' 已上传')

                                # 安装应用包
                                if self.install_software_str.get() == 1:
                                    self.install_str.set('正在导入应用包..')
                                    software_files_path = self.install_software_entry_str.get()
                                    if self.install_software_value.get().strip() == '主程序默认安装位置':
                                        main_result = public.execute_cmd('adb -s ' + device + ' push ' + '"' + software_files_path + '"' +
                                                                                   ' /etc/miniapp/resources/presetpkgs/8180000000000020.amr')
                                        print(main_result)
                                        print(software_files_path + ' 已上传')
                                    elif self.install_software_value.get().strip() == '引导页默认安装位置':
                                        main_result = public.execute_cmd('adb -s ' + device + ' push ' + '"' + software_files_path + '"' +
                                                                                   ' /etc/miniapp/resources/presetpkgs/8180000000000026.amr')
                                        print(main_result)
                                        print(software_files_path + ' 已上传')
                                    elif self.install_software_value.get().strip() == '喜马拉雅默认安装位置':
                                        main_result = public.execute_cmd('adb -s ' + device + ' push ' + '"' + software_files_path + '"' +
                                                           ' /etc/miniapp/resources/presetpkgs/8080231999314849.amr')
                                        print(main_result)
                                        print(software_files_path + ' 已上传')
                                    elif self.install_software_value.get().strip() == '牛津词典默认安装位置':
                                        main_result = public.execute_cmd('adb -s ' + device + ' push ' + '"' + software_files_path + '"' +
                                                           ' /etc/miniapp/resources/presetpkgs/8080251822789980.amr')
                                        print(main_result)
                                        print(software_files_path + ' 已上传')

                                # 安装后需要清理缓存
                                self.install_str.set('正在清理缓存并重启设备..')
                                public.execute_cmd('adb -s ' + device + ' shell rm -rf /data/miniapp/data')

                                # 重启
                                public.execute_cmd('adb -s ' + device + ' shell reboot')
                                self.install_str.set('安装应用完成\n等待设备重启后使用即可')

            self.linux_install_button_disable.place_forget()

        t_linux_install = threading.Thread(target=t_linux_install)
        t_linux_install.setDaemon(True)
        t_linux_install.start()


# 获取扫描帧数图片界面
class Linux_Camera(object):
    def camera_form(self,init_str,linux_camera,linux_camera_disable,device):
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
        # self.camera_root.wm_attributes('-topmost', 1)

        self.camera_startup(linux_camera,linux_camera_disable)

        self.camera_root.protocol('WM_DELETE_WINDOW',self.close_handle)
        self.main_frame(linux_camera_disable,device)

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
        # 模拟键盘回车输入以便自动取消消息框
        # keyboard.press('enter')
        keyboard.press(Key.enter)

    def main_frame(self,linux_camera_disable,device):
        # 获取图片状态栏
        self.camera_str = tkinter.StringVar()
        self.camera_label = tkinter.Label(self.camera_root, textvariable=self.camera_str, bg='black', fg='#FFFFFF',
                                           width=40, height=2)
        self.camera_label.place(x=30, y=10)
        self.camera_label.config(command=self.check_system(linux_camera_disable,device))
        self.camera_str.set('此处显示获取图片状态')

        # 开启取图模式按钮
        self.take_image_mode_close = False
        self.linux_camera_button = tkinter.Button(self.camera_root, text='开启取图模式', width=15)
        self.linux_camera_button.bind('<Button-1>', lambda x: self.open_camera_bind(linux_camera_disable,device))
        self.linux_camera_button.place(x=30, y=60)
        self.linux_camera_button_disable = tkinter.Button(self.camera_root, text='开启取图模式', width=15)
        self.linux_camera_button_disable_open = tkinter.Button(self.camera_root, text='正在开启中...', width=15)
        self.linux_camera_button_disable_final = tkinter.Button(self.camera_root, text='取图模式已打开', width=15)
        self.linux_camera_button_disable_open.config(state='disable')
        self.linux_camera_button_disable.config(state='disable')
        self.linux_camera_button_disable_final.config(state='disable')

        # 关闭取图模式按钮
        self.linux_camera_button_close = tkinter.Button(self.camera_root, text='关闭取图模式', width=15)
        self.linux_camera_button_close.bind('<Button-1>', lambda x: self.close_camera_bind(linux_camera_disable,device))
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
        self.linux_get_camera_button.bind('<Button-1>',lambda x:self.camera_pywinauto_main(linux_camera_disable,device))
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

    def check_system(self,linux_camera_disable,device):
        def t_check_system():
            # 检测 是否配置 适用于取图的system文件
            self.camera_str.set('正在检测是否配置system文件...')
            check_system_cmd = public.execute_cmd('adb -s ' + device + ' shell ls -lh /data/camera_system.ini')
            check_system_cmd_finally = ' '.join(check_system_cmd.split()).split(':')[-1]
            print(check_system_cmd_finally)
            if check_system_cmd_finally.strip() == 'No such file or directory':
                message = '配置取图功能需要重启多次，是否继续？\n点击“取消”则会关闭此页面！'
                if tkinter.messagebox.askokcancel(title='温馨提示', message=message,default='cancel'):
                    camera_exists = self.camera_root.winfo_exists()
                    if camera_exists == 0:
                        print('取图模块窗口已关闭，点击无影响！')
                    else:
                        self.camera_str.set('检测没有配置过system，正在初始化...')
                        # 内置取图配置文件到设备中
                        public.execute_cmd('adb -s ' + device + ' push ' + system_path + ' /etc/config/uci/system')
                        public.execute_cmd('adb -s ' + device + ' push ' + camera_system_path + ' /data/')
                        # 需要重启生效
                        public.execute_cmd('adb -s ' + device + ' shell reboot')
                        time.sleep(18)
                        self.camera_str.set('取图工具初始化成功\n请点击“开启取图模式”按钮开启')

                        # 开放按钮
                        self.linux_camera_button_disable.place_forget()
                        self.linux_camera_button_disable_final.place_forget()
                        self.linux_camera_button.place(x=30, y=60)
                else:
                    with open(camera_page, 'w') as fp:
                        fp.write('0')
                    self.close_handle()
            else:
                self.camera_str.set('已内置system配置文件\n可以开始使用取图功能')
                take_image_mode_info = public.execute_cmd('adb -s ' + device + ' shell cat /data/camera_system.ini')
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

    def open_camera_bind(self,linux_camera_disable,device):
        def t_open_camera():
            devices_state = public.device_connect()
            if not devices_state:
                self.camera_str.set('检测到没有连接到设备\n请连接设备后再使用本功能')
            else:
                only_read = public.linux_only_read(device)
                if only_read == ' No such file or directory':
                    public.execute_cmd('adb -s ' + device + ' shell rm -rf /data/camera_system.ini')
                    self.camera_str.set('检测该设备没有初始化\n请重新初始化后才能使用本功能')
                else:
                    devices = open(devices_log, 'r').read()
                    device_type = public.device_type_android(devices)
                    if device_type.strip() == 'Android':
                        self.camera_str.set('您所连接的设备为Android\n无法使用取图功能')
                    else:
                        check_system_cmd = public.execute_cmd('adb -s ' + device + ' shell ls -lh /data/camera_system.ini')
                        check_system_cmd_finally = ' '.join(check_system_cmd.split()).split(':')[-1]
                        print(check_system_cmd_finally)
                        if check_system_cmd_finally.strip() == 'No such file or directory':
                            # 先禁用按钮
                            self.linux_camera_button_disable.place(x=30, y=60)
                            self.linux_camera_button_close_disable.place(x=200, y=60)
                            self.linux_get_camera_button_disable.place(x=30, y=100)
                            self.check_system(linux_camera_disable,device)
                        else:
                            # 开启取图模式
                            self.take_image_mode_close = False
                            # 设置 打开取图模式后的标志
                            public.execute_cmd('adb -s ' + device + ' push ' + camera_open_path + ' /data/')
                            self.main_camera_bind(self.take_image_mode_close,device)

        t_open_camera = threading.Thread(target=t_open_camera)
        t_open_camera.setDaemon(True)
        t_open_camera.start()

    def close_camera_bind(self,linux_camera_disable,device):
        def t_close_camera():
            devices_state = public.device_connect()
            if not devices_state:
                self.camera_str.set('检测到没有连接到设备\n请连接设备后再使用本功能')
            else:
                only_read = public.linux_only_read(device)
                if only_read == ' No such file or directory':
                    public.execute_cmd('adb -s ' + device + ' shell rm -rf /data/camera_system.ini')
                    self.camera_str.set('检测该设备没有初始化\n请重新初始化后才能使用本功能')
                else:
                    check_system_cmd = public.execute_cmd('adb -s ' + device + ' shell ls -lh /data/camera_system.ini')
                    check_system_cmd_finally = ' '.join(check_system_cmd.split()).split(':')[-1]
                    print(check_system_cmd_finally)
                    if check_system_cmd_finally.strip() == 'No such file or directory':
                        # 先禁用按钮
                        self.linux_camera_button_disable.place(x=30, y=60)
                        self.linux_camera_button_close_disable.place(x=200, y=60)
                        self.linux_get_camera_button_disable.place(x=30, y=100)
                        self.check_system(linux_camera_disable,device)
                    else:
                        # 关闭取图模式
                        # 取图模式标志
                        self.take_image_mode_close = True
                        # 设置 打开取图模式后的标志
                        public.execute_cmd('adb -s ' + device + ' push ' + camera_close_path + ' /data/')
                        self.main_camera_bind(self.take_image_mode_close,device)

        t_close_camera = threading.Thread(target=t_close_camera)
        t_close_camera.setDaemon(True)
        t_close_camera.start()

    def main_camera_bind(self,take_image_mode_close,device):
        def t_main_camera():
            # 取图模式核心流程
            if take_image_mode_close:
                self.linux_camera_button_close_disable_open.place(x=200, y=60)
                self.linux_get_camera_button_disable.place(x=30,y=100)
                # 设置取图模式为False (关闭取图模式)
                self.camera_str.set('正在关闭取图模式并重启...')
                public.execute_cmd('adb -s ' + device + ' shell uci set system.algo_imageParameter.isSaveOriginalImage=false')
            else:
                self.linux_camera_button_disable_open.place(x=30, y=60)
                # 设置取图模式为True (开启取图模式)
                self.camera_str.set('正在启动取图模式并重启...')
                public.execute_cmd('adb -s ' + device + ' shell uci set system.algo_imageParameter.isSaveOriginalImage=true')
            # 上传到system
            public.execute_cmd('adb -s ' + device + ' shell uci commit system')
            # 重启
            public.execute_cmd('adb -s ' + device + ' shell reboot')
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

    def camera_pywinauto_main(self,linux_camera_disable,device):
        def t_camera_pywinauto():
            devices_state = public.device_connect()
            if not devices_state:
                self.camera_str.set('检测到没有连接到设备\n请连接设备后再使用本功能')
            else:
                only_read = public.linux_only_read(device)
                if only_read == ' No such file or directory':
                    public.execute_cmd('adb -s ' + device + ' shell rm -rf /data/camera_system.ini')
                    self.camera_str.set('检测该设备没有初始化\n请重新初始化后才能使用本功能')
                else:
                    # 取图核心主流程
                    check_system_cmd = public.execute_cmd('adb -s ' + device + ' shell ls -lh /data/camera_system.ini')
                    check_system_cmd_finally = ' '.join(check_system_cmd.split()).split(':')[-1]
                    print(check_system_cmd_finally)
                    if check_system_cmd_finally.strip() == 'No such file or directory':
                        # 先禁用按钮
                        self.linux_camera_button_disable.place(x=30, y=60)
                        self.linux_camera_button_close_disable.place(x=200, y=60)
                        self.linux_get_camera_button_disable.place(x=30, y=100)
                        self.check_system(linux_camera_disable,device)
                    else:
                        self.linux_get_camera_button_disable_final.place(x=30, y=100)
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
                        command = 'adb -s ' + device + ' pull /tmp/yuv_data ' + get_yuv_path
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
                                        public.execute_cmd('adb -s ' + device + ' shell rm -rf /tmp/yuv_data/ping/*.yuv')
                                        public.execute_cmd('adb -s ' + device + ' shell rm -rf /tmp/yuv_data/pong/*.yuv')
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


# 写号工具页面
class Linux_WriteNumber(object):
    def write_number_form(self,init_str,write_number_Button,write_number_Button_disable,device):
        self.write_number_root = tkinter.Toplevel()
        self.write_number_root.title('写号/写码工具 - Linux')
        screenWidth = self.write_number_root.winfo_screenwidth()
        screenHeight = self.write_number_root.winfo_screenheight()
        w = 560
        h = 360
        x = (screenWidth - w) / 2
        y = (screenHeight - h) / 2
        self.write_number_root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.write_number_root.geometry('%dx%d' % (w, h))
        self.write_number_root.iconbitmap(LOGO_path)
        self.write_number_root.resizable(0, 0)
        self.write_number_root.wm_attributes('-topmost', 1)

        self.write_number_startup(write_number_Button,write_number_Button_disable)

        self.write_number_root.protocol('WM_DELETE_WINDOW',self.close_handle)
        self.main_frame(device)

        return self.write_number_root

    def write_number_startup(self,write_number_Button,write_number_Button_disable):
        # 监听写号工具页面的打开状态
        write_number_exists = self.write_number_root.winfo_exists()
        print(write_number_exists)
        if write_number_exists == 1:
            write_number_Button.place_forget()
            write_number_Button_disable.place(x=200, y=230)

    def close_handle(self):
        # 监听页面消失
        with open(write_number_page,'w') as fp:
            fp.write('0')
        self.write_number_root.destroy()

    def main_frame(self,device):
        # 获取写号工具状态栏
        self.write_number_str = tkinter.StringVar()
        self.write_number_label = tkinter.Label(self.write_number_root, textvariable=self.write_number_str, bg='black', fg='#FFFFFF',
                                          width=40, height=2)
        self.write_number_label.place(x=60, y=10)
        # self.write_number_label.config(command=self.check_system(linux_camera_disable, device))
        self.write_number_str.set('此处显示写号/写码工具状态')

        self.write_code_label_factory = tkinter.Label(self.write_number_root,text='写码/三元组',fg='red',width=40,font=('华文行楷',15))
        self.write_code_label_factory.place(x=20,y=60)

        # 三元组输入框
        self.write_secretkey_entry_str = tkinter.StringVar()
        self.write_secretkey_entry = tkinter.Entry(self.write_number_root, textvariable=self.write_secretkey_entry_str,
                                                   width=40, highlightcolor='blue', validate="focusin"
                                                   , highlightthickness=5)
        self.write_secretkey_entry.place(x=55, y=90)
        self.write_secretkey_entry.insert(0, '请输入<三元组>')
        self.write_secretkey_entry.config(command=self.write_secretkey_entry_bind())

        # MAC地址输入框
        self.write_mac_entry_str = tkinter.StringVar()
        self.write_mac_entry = tkinter.Entry(self.write_number_root, textvariable=self.write_mac_entry_str,
                                                    width=40, highlightcolor='orange', validate="focusin"
                                                    , highlightthickness=5)
        self.write_mac_entry.place(x=55, y=120)
        self.write_mac_entry.insert(0,'请输入<wifi mac地址>')
        self.write_mac_entry.config(command=self.write_mac_entry_bind())

        # MD5值输入框
        self.write_md5_entry_str = tkinter.StringVar()
        self.write_md5_entry = tkinter.Entry(self.write_number_root, textvariable=self.write_md5_entry_str,
                                                   width=40, highlightcolor='purple', validate="focusin"
                                                   , highlightthickness=5)
        self.write_md5_entry.place(x=55, y=150)
        self.write_md5_entry.insert(0, '请输入<md5>')
        self.write_md5_entry.config(command=self.write_md5_entry_bind())

        # 写码复选框（勾选此项开启写码功能）
        self.write_code_str = tkinter.IntVar()
        self.write_code_checkbutton = tkinter.Checkbutton(self.write_number_root, onvalue=1, offvalue=0,
                                            text='勾选此项开启写码',variable=self.write_code_str)
        self.write_code_checkbutton.place(x=55, y=190)

        # 写码按钮
        self.write_code_button = tkinter.Button(self.write_number_root,text='开始写码')
        self.write_code_button_disable = tkinter.Button(self.write_number_root,text='开始写码')
        self.write_code_button.bind('<Button-1>',lambda x:self.write_code_bind(device))
        self.write_code_button_disable.config(state='disable')
        self.write_code_button.place(x=200,y=190)

        self.write_number_label_factory = tkinter.Label(self.write_number_root, text='写号', fg='red', width=40,
                                                        font=('华文行楷', 15))
        self.write_number_label_factory.place(x=20, y=230)

        # SN号输入框
        self.write_SN_entry_str = tkinter.StringVar()
        self.write_SN_entry = tkinter.Entry(self.write_number_root, textvariable=self.write_SN_entry_str,
                                             width=40, highlightcolor='red', validate="focusin"
                                             , highlightthickness=5)
        self.write_SN_entry.place(x=55, y=260)
        self.write_SN_entry.insert(0, '请输入<SN号>')
        self.write_SN_entry.config(command=self.write_SN_entry_bind())

        # 写号单选按钮
        self.write_15_str = tkinter.IntVar()
        self.write_15_radio_button = tkinter.Radiobutton(self.write_number_root, text='15位数', variable=self.write_15_str, value=0)
        self.write_15_radio_button.place(x=170, y=293)

        # 写号按钮
        self.write_SN_button = tkinter.Button(self.write_number_root, text='开始写号',width=20)
        self.write_SN_button.bind('<Button-1>', lambda x: self.write_SN_bind(device))
        self.write_SN_button_disable = tkinter.Button(self.write_number_root, text='正在写号...',width=20)
        self.write_SN_button_disable.config(state='disable')
        self.write_SN_button.place(x=130, y=320)

        # 已写号记录ListBox
        self.write_SN_listbox_frame = tkinter.Frame(self.write_number_root,width=200,height=198)
        # 创建滚动条
        self.write_SN_scrollbar = tkinter.Scrollbar(self.write_SN_listbox_frame)
        # listbox控件创建并与滚动条绑定
        self.write_SN_listbox = tkinter.Listbox(self.write_SN_listbox_frame,width=27,height=10,yscrollcommand=(self.write_SN_scrollbar.set))
        # listbox内容数据联动滚动条
        self.write_SN_scrollbar.config(command=(self.write_SN_listbox.yview))
        # 显示滚动条
        self.write_SN_scrollbar.pack(side=(tkinter.RIGHT), fill=(tkinter.Y))
        self.write_SN_listbox.config(command=self.write_SN_listbox_bind())
        self.write_SN_listbox.pack()
        self.write_SN_listbox_frame.place(x=350,y=180)

    def write_mac_entry_bind(self):
        # MAC地址提示语逻辑
        def t_write_mac_entry():
            try:
                while True:
                    write_mac_result = self.write_mac_entry_str.get()
                    # print(write_mac_result)
                    if write_mac_result.strip() != '' and write_mac_result.strip() != '请输入<wifi mac地址>':
                        def entry_pass():
                            # 为空，不处理
                            return
                        self.write_mac_entry.bind('<FocusIn>',lambda x: entry_pass())
                        self.write_mac_entry.bind('<FocusOut>', lambda x: entry_pass())
                    else:
                        self.write_mac_entry.bind('<FocusIn>', lambda x: self.write_mac_entry.delete(0, tkinter.END))
                        self.write_mac_entry.bind('<FocusOut>', lambda x: self.write_mac_entry.insert(0, '请输入<wifi mac地址>'))
                    time.sleep(1)
            except tkinter.TclError:
                print('退出警告，可忽略此消息')

        t_write_mac_entry = threading.Thread(target=t_write_mac_entry)
        t_write_mac_entry.setDaemon(True)
        t_write_mac_entry.start()

    def write_secretkey_entry_bind(self):
        # 三元组提示语逻辑
        def t_write_secretkey_entry():
            try:
                while True:
                    write_secretkey_result = self.write_secretkey_entry_str.get()
                    # print(write_mac_result)
                    if write_secretkey_result.strip() != '' and write_secretkey_result.strip() != '请输入<三元组>':
                        def entry_pass():
                            # 为空，不处理
                            return
                        self.write_secretkey_entry.bind('<FocusIn>',lambda x: entry_pass())
                        self.write_secretkey_entry.bind('<FocusOut>', lambda x: entry_pass())
                    else:
                        self.write_secretkey_entry.bind('<FocusIn>',
                                                        lambda x: self.write_secretkey_entry.delete(0, tkinter.END))
                        self.write_secretkey_entry.bind('<FocusOut>',
                                                        lambda x: self.write_secretkey_entry.insert(0, '请输入<三元组>'))
                    time.sleep(1)
            except tkinter.TclError:
                pass

        t_write_secretkey_entry = threading.Thread(target=t_write_secretkey_entry)
        t_write_secretkey_entry.setDaemon(True)
        t_write_secretkey_entry.start()

    def write_md5_entry_bind(self):
        # MD5值提示语逻辑
        def t_write_md5_entry():
            try:
                while True:
                    write_md5_result = self.write_md5_entry_str.get()
                    # print(write_mac_result)
                    if write_md5_result.strip() != '' and write_md5_result.strip() != '请输入<md5>':
                        def entry_pass():
                            # 为空，不处理
                            return
                        self.write_md5_entry.bind('<FocusIn>',lambda x: entry_pass())
                        self.write_md5_entry.bind('<FocusOut>', lambda x: entry_pass())
                    else:
                        self.write_md5_entry.bind('<FocusIn>',
                                                        lambda x: self.write_md5_entry.delete(0, tkinter.END))
                        self.write_md5_entry.bind('<FocusOut>',
                                                        lambda x: self.write_md5_entry.insert(0, '请输入<md5>'))
                    time.sleep(1)
            except tkinter.TclError:
                pass

        t_write_md5_entry = threading.Thread(target=t_write_md5_entry)
        t_write_md5_entry.setDaemon(True)
        t_write_md5_entry.start()

    def write_SN_listbox_bind(self):
        # 实时检测SN写号记录
        self.write_SN_listbox.insert(tkinter.END,'# 此处显示已写入SN号记录')
        self.write_SN_listbox.insert(tkinter.END,'# 已写入的SN号和设备MAC地址')
        write_SN_read = open(write_SN_log, 'r')
        for readline in write_SN_read.readlines():
            self.write_SN_listbox.insert(tkinter.END, readline)

    def write_SN_entry_bind(self):
        # SN号提示语逻辑
        def t_write_SN_entry():
            try:
                while True:
                    write_SN_result = self.write_SN_entry_str.get()
                    # print(write_mac_result)
                    if write_SN_result.strip() != '' and write_SN_result.strip() != '请输入<SN号>':
                        def entry_pass():
                            # 为空，不处理
                            return
                        self.write_SN_entry.bind('<FocusIn>',lambda x: entry_pass())
                        self.write_SN_entry.bind('<FocusOut>', lambda x: entry_pass())
                    else:
                        self.write_SN_entry.bind('<FocusIn>',
                                                        lambda x: self.write_SN_entry.delete(0, tkinter.END))
                        self.write_SN_entry.bind('<FocusOut>',
                                                        lambda x: self.write_SN_entry.insert(0, '请输入<SN号>'))
                    time.sleep(1)
            except tkinter.TclError:
                pass

        t_write_SN_entry = threading.Thread(target=t_write_SN_entry)
        t_write_SN_entry.setDaemon(True)
        t_write_SN_entry.start()

    def write_code_bind(self,device):
        def t_write_code():
            # 写码逻辑
            self.write_code_button_disable.place(x=200,y=190)
            devices_state = public.device_connect()
            if not devices_state:
                self.write_number_str.set('检测到没有连接到设备\n请连接设备后再使用本功能')
            else:
                if self.write_code_str.get() == 1:
                    if self.write_mac_entry_str.get() == '' or self.write_md5_entry_str.get() == '' or \
                       self.write_secretkey_entry_str.get() == '' or self.write_mac_entry_str.get() == '请输入<wifi mac地址>' or \
                       self.write_md5_entry_str.get() == '请输入<md5>' or self.write_secretkey_entry_str.get() == '请输入<三元组>':
                       self.write_number_str.set('输入框不能为空！！！')
                    else:
                        # 写入MAC地址
                        self.write_number_str.set('正在写入WMAC...')
                        WMAC = self.write_mac_entry_str.get().strip()
                        mac_result = public.execute_cmd('adb -s ' + device + ' shell factory ATE_SET_WMAC ' + WMAC)
                        print('adb shell factory ATE_SET_WMAC结果：\n' + mac_result)
                        # 写入三元组和MD5
                        self.write_number_str.set('正在写入三元组和MD5...')
                        SECRETKEY = self.write_secretkey_entry_str.get().strip()
                        MD5 = self.write_md5_entry_str.get().strip()
                        # secretkey_md5_result = public.execute_cmd('adb -s ' + device + ' shell factory ATE_SET_SECRETKEY_MD5 '
                        #                                           + SECRETKEY + ' ' + MD5)
                        cmd = 'adb -s ' + device + ' shell factory ATE_SET_SECRETKEY_MD5 ' + SECRETKEY + ' ' + MD5
                        p = subprocess.Popen(cmd, shell=False, stdout=(subprocess.PIPE),
                                             stderr=(subprocess.STDOUT))
                        secretkey_md5_result = p.stdout.readlines()
                        print('adb shell factory ATE_SET_SECRETKEY_MD5结果：\n' + str(secretkey_md5_result))
                        # 重启生效
                        public.execute_cmd('adb -s ' + device + ' shell reboot')
                        self.write_number_str.set('写码完成！！！\n等待设备重启后即可激活')
                        # 写码成功后就清空，方便写下一个码
                        self.write_mac_entry_str.set('请输入<wifi mac地址>')
                        self.write_md5_entry_str.set('请输入<md5>')
                        self.write_secretkey_entry_str.set('请输入<三元组>')
                else:
                    self.write_number_str.set('请勾选此处开始写码才能写码！！！')
            self.write_code_button_disable.place_forget()

        t_write_code = threading.Thread(target=t_write_code)
        t_write_code.setDaemon(True)
        t_write_code.start()

    def write_SN_bind(self,device):
        def write_SN_save(SN):
            # 添加SN号记录并保存
            wifi_mac = public.wifi_mac_result(device)
            with open(write_SN_log,'a+') as fp:
                fp.write('SN号：' + SN + '\n' + '设备MAC：' + wifi_mac + '\n')
                fp.write('-------------------------\n')
            # 创建设备内部SN号记录标记
            with open(SN_path, 'w') as fp:
                fp.write(SN)
            sn_result = public.execute_cmd('adb -s ' + device + ' push ' + SN_path + ' /data/SN.txt')
            print(sn_result)
            # 记录完后删除缓存
            os.remove(SN_path)
            # 实时显示SN记录
            self.write_SN_listbox.insert(tkinter.END,'SN号：' + SN)
            self.write_SN_listbox.insert(tkinter.END,'设备MAC：' + wifi_mac)
            self.write_SN_listbox.insert(tkinter.END,'-------------------------')
            self.write_SN_listbox.see(tkinter.END)

        def t_write_SN():
            print('开始写号....')
            self.write_SN_button_disable.place(x=130,y=320)
            devices_state = public.device_connect()
            if not devices_state:
                self.write_number_str.set('检测到没有连接到设备\n请连接设备后再使用本功能')
            else:
                devices = open(devices_log, 'r').read()
                device_type = public.device_type_android(devices)
                if device_type.strip() == 'Android':
                    self.write_number_str.set('您所连接的设备为Android\n无法使用写号功能')
                else:
                    SN = self.write_SN_entry_str.get().strip()
                    print(SN)
                    print('当前输入的SN位数为 ' + str(len(SN)))
                    devices_state = public.device_connect()
                    if not devices_state:
                        self.write_number_str.set('请重新连接设备后再写号')
                    else:
                        # 已写入SN号无法再次写号
                        SN_list = []
                        write_SN_read = open(write_SN_log, 'r').readlines()
                        # print(write_SN_read)
                        for sn in write_SN_read:
                            sn_finally = re.findall('SN号：(.*?)\n', sn)
                            if sn_finally == []:
                                pass
                            else:
                                SN_finally = ''.join(sn_finally)
                                SN_list.append(SN_finally)
                        sn_read = public.execute_cmd('adb -s ' + device + ' shell cat /data/SN.txt')
                        if SN in SN_list and SN == sn_read:
                            self.write_number_str.set(SN + '已被当前设备写入\n请看右侧列表查看对应设备MAC')
                        else:
                            if self.write_15_str.get() == 0:
                                # 15位数
                                print('监听 15位数 选项')
                                if len(SN) == 15:
                                    self.write_number_str.set('正在为设备写入\n' + SN)
                                    SN_result = public.execute_cmd('adb -s ' + device + ' shell factory ATE_SET_SN ' + SN)
                                    print(SN_result)
                                    with open(SN_result_path,'w') as fp:
                                        fp.write(SN_result)
                                    public.execute_cmd('adb -s ' + device + ' push ' + SN_result_path + ' /data')
                                    success = public.execute_cmd('adb -s ' + device + ' shell grep "SUCCESS" /data/SN_result.log')
                                    print(success)
                                    if success.strip() == 'SUCCESS':
                                        write_SN_save(SN)
                                        self.write_number_str.set('正在清理数据缓存并重启...')
                                        # SN号写入后需要重新激活才会有效，否则无法绑定设备
                                        public.execute_cmd('adb -s ' + device + ' shell rm -rf /data/miniapp/data')
                                        public.execute_cmd('adb -s ' + device + ' shell reboot')
                                        self.write_number_str.set(SN + '\n已被成功写入！！！')
                                    else:
                                        self.write_number_str.set('写号失败！！！\n请重新输入再试试')
                                else:
                                    self.write_number_str.set('你输入的SN号不合法！！！')
            self.write_SN_button_disable.place_forget()

        t_write_SN = threading.Thread(target=t_write_SN)
        t_write_SN.setDaemon(True)
        t_write_SN.start()


# 一键获取日志界面
class Linux_Log(object):
    def log_form(self,init_str,linux_log_Button,linux_log_Button_disable,device):
        self.log_root = tkinter.Toplevel()
        self.log_root.title('Linux一键获取日志')
        # screenWidth = self.log_root.winfo_screenwidth()
        # screenHeight = self.log_root.winfo_screenheight()
        w = 310
        h = 250
        # x = (screenWidth - w) / 2
        # y = (screenHeight - h) / 2
        # self.log_root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.log_root.geometry('%dx%d' % (w, h))
        self.log_root.iconbitmap(LOGO_path)
        self.log_root.resizable(0, 0)
        # self.log_root.wm_attributes('-topmost', 1)

        self.log_startup(linux_log_Button,linux_log_Button_disable)

        self.log_root.protocol('WM_DELETE_WINDOW',self.close_handle)
        self.main_frame(device)

        return self.log_root

    def log_startup(self,linux_log_Button,linux_log_Button_disable):
        # 监听一键获取日志页面的打开状态
        log_exists = self.log_root.winfo_exists()
        print(log_exists)
        if log_exists == 1:
            linux_log_Button.place_forget()
            linux_log_Button_disable.place(x=200, y=270)

    def close_handle(self):
        # 监听页面消失
        with open(get_log_page,'w') as fp:
            fp.write('0')
        self.log_root.destroy()

    def main_frame(self,device):
        # 一键获取日志状态栏
        self.get_log_str = tkinter.StringVar()
        self.get_log_label = tkinter.Label(self.log_root, textvariable=self.get_log_str, bg='black', fg='#FFFFFF',
                                           width=35, height=2)
        # self.screen_label.config(command=self.check_gsnap(device))
        self.get_log_label.place(x=35, y=10)
        self.get_log_str.set('此处显示获取日志状态')

        # 一键获取crash_reports（崩溃）按钮
        self.get_crash_reports_button = tkinter.Button(self.log_root, text='获取crash_reports（崩溃日志）', width=30)
        self.get_crash_reports_button.bind('<Button-1>', lambda x: self.get_crash_reports_bind(device))
        self.get_crash_reports_button_disable = tkinter.Button(self.log_root, text='正在获取crash_reports...', width=30)
        self.get_crash_reports_button_disable.config(state='disable')
        self.get_crash_reports_button.place(x=50, y=60)

        # 一键获取syslog.log（系统日志）按钮
        self.get_syslog_button = tkinter.Button(self.log_root, text='获取syslog（系统日志）', width=30)
        self.get_syslog_button.bind('<Button-1>', lambda x: self.get_syslog_bind(device))
        self.get_syslog_button_disable = tkinter.Button(self.log_root, text='正在获取syslog...', width=30)
        self.get_syslog_button_disable.config(state='disable')
        self.get_syslog_button.place(x=50, y=95)

        # 打开日志文件夹按钮
        self.open_syslog_button = tkinter.Button(self.log_root, text='打开日志文件夹', width=30)
        self.open_syslog_button.bind('<Button-1>', lambda x: self.open_syslog_bind())
        self.open_syslog_button_disable = tkinter.Button(self.log_root, text='正在打开日志文件夹...', width=30)
        self.open_syslog_button_disable.config(state='disable')
        self.open_syslog_button.place(x=50, y=130)

        # 一键清空日志按钮
        self.clean_syslog_button = tkinter.Button(self.log_root, text='一键清空日志', width=30)
        self.clean_syslog_button.bind('<Button-1>', lambda x: self.clean_syslog_bind(device))
        self.clean_syslog_button_disable = tkinter.Button(self.log_root, text='正在清空日志...', width=30)
        self.clean_syslog_button_disable.config(state='disable')
        self.clean_syslog_button.place(x=50, y=165)

        # 一键重置日志文件夹按钮
        self.reset_syslog_button = tkinter.Button(self.log_root, text='一键重置日志文件夹', width=30)
        self.reset_syslog_button.bind('<Button-1>', lambda x: self.reset_syslog_bind())
        self.reset_syslog_button_disable = tkinter.Button(self.log_root, text='正在重置日志文件夹...', width=30)
        self.reset_syslog_button_disable.config(state='disable')
        self.reset_syslog_button.place(x=50, y=200)

    def get_crash_reports_bind(self,device):
        def t_get_crash_reports():
            # 一键获取crash_reports
            self.get_crash_reports_button_disable.place(x=50, y=60)
            self.get_log_str.set('正在获取崩溃日志crash_reports...')
            devices_state = public.device_connect()
            if not devices_state:
                self.get_log_str.set('检测到没有连接到设备\n请连接设备后再使用本功能')
            else:
                only_read = public.linux_only_read(device)
                if only_read == ' No such file or directory':
                    self.get_log_str.set('检测该设备没有初始化\n请重新初始化后才能使用本功能')
                else:
                    devices = open(devices_log, 'r').read()
                    device_type = public.device_type_android(devices)
                    if device_type.strip() == 'Android':
                        self.get_log_str.set('您所连接的设备为Android\n无法使用一键获取日志功能')
                    else:
                        crash_reports_dir = linux_log_path + 'crash_reports'
                        if not os.path.exists(crash_reports_dir):
                            os.makedirs(crash_reports_dir)
                        now = time.localtime()
                        now_time = time.strftime("%Y-%m-%d_%H%M%S", now)
                        print('获取crash_reports时的当前时间：' + str(now_time))
                        crash_reports_result = public.execute_cmd('adb -s ' + device + ' pull /data/crash_reports ' + crash_reports_dir + '\\crash_reports-' + now_time)
                        print('crash_reports获取结果：' + crash_reports_result)
                        crash_reports_result_str = crash_reports_result.split(':')[-1].strip()
                        if crash_reports_result_str == "remote object '/data/crash_reports' does not exist":
                            self.get_log_str.set('没有找到崩溃日志crash_reports\n无需保存文件！')
                        else:
                            self.get_log_str.set('崩溃日志crash_reports已保存！文件保存在:\n 桌面\\' + linux_dirname_log + '\\crash_reports')
            self.get_crash_reports_button_disable.place_forget()

        t_get_crash_reports = threading.Thread(target=t_get_crash_reports)
        t_get_crash_reports.setDaemon(True)
        t_get_crash_reports.start()

    def get_syslog_bind(self,device):
        def t_get_syslog():
            # 一键获取syslog
            self.get_syslog_button_disable.place(x=50, y=95)
            self.get_log_str.set('正在获取系统日志syslog.log...')
            devices_state = public.device_connect()
            if not devices_state:
                self.get_log_str.set('检测到没有连接到设备\n请连接设备后再使用本功能')
            else:
                only_read = public.linux_only_read(device)
                if only_read == ' No such file or directory':
                    self.get_log_str.set('检测该设备没有初始化\n请重新初始化后才能使用本功能')
                else:
                    devices = open(devices_log, 'r').read()
                    device_type = public.device_type_android(devices)
                    if device_type.strip() == 'Android':
                        self.get_log_str.set('您所连接的设备为Android\n无法使用一键获取日志功能')
                    else:
                        syslog_dir = linux_log_path + 'syslog.log'
                        if not os.path.exists(syslog_dir):
                            os.makedirs(syslog_dir)
                        now = time.localtime()
                        now_time = time.strftime("%Y-%m-%d_%H%M%S", now)
                        print('获取syslog.log时的当前时间：' + str(now_time))
                        # 新建带日期存放日志的文件夹
                        syslog_dir_all = syslog_dir + '\\syslog.log-' + now_time
                        os.makedirs(syslog_dir_all)
                        # 获取syslog文件夹
                        self.get_log_str.set('正在pull 更早时间的syslog文件夹...')
                        syslog_result = public.execute_cmd('adb -s ' + device + ' pull /data/syslog ' + syslog_dir_all)
                        print('syslog文件夹获取结果：' + syslog_result)
                        # 获取syslog.log文件
                        self.get_log_str.set('正在pull syslog.log文件...')
                        syslog_log_result = public.execute_cmd('adb -s ' + device + ' pull /data/syslog.log ' + syslog_dir_all)
                        print('syslog.log获取结果：' + syslog_log_result)
                        # 获取syslog.log.*文件（*代表数字0~8）
                        for f in range(0,9):
                            self.get_log_str.set('正在pull syslog.log.'+ str(f) +'文件...')
                            syslog_log_result = public.execute_cmd('adb -s ' + device + ' pull /data/syslog.log.' + str(f) +
                                                 ' ' + syslog_dir_all)
                            syslog_log_result_str = syslog_log_result.split(':')[-1].strip()
                            if syslog_log_result_str == "remote object '/data/syslog.log.%s' does not exist" % str(f):
                                # 搜索到没有的文件就停止pull
                                break
                            print('syslog.log.' + str(f) + '获取结果：' + syslog_log_result)
                        self.get_log_str.set('系统日志syslog.log已保存！文件保存在:\n 桌面\\' + linux_dirname_log + '\\syslog.log')
            self.get_syslog_button_disable.place_forget()

        t_get_syslog = threading.Thread(target=t_get_syslog)
        t_get_syslog.setDaemon(True)
        t_get_syslog.start()

    def open_syslog_bind(self):
        # 打开日志文件夹
        self.open_syslog_button_disable.place(x=50, y=130)
        if not os.path.exists(linux_log_path):
            os.makedirs(linux_log_path)
        win32api.ShellExecute(0, 'open', linux_log_path, '', '', 1)
        self.open_syslog_button_disable.place_forget()

    def clean_syslog_bind(self,device):
        def t_clean_syslog():
            # 一键清空日志
            self.clean_syslog_button_disable.place(x=50,y=165)
            devices_state = public.device_connect()
            if not devices_state:
                self.get_log_str.set('检测到没有连接到设备\n请连接设备后再使用本功能')
            else:
                only_read = public.linux_only_read(device)
                if only_read == ' No such file or directory':
                    self.get_log_str.set('检测该设备没有初始化\n请重新初始化后才能使用本功能')
                else:
                    devices = open(devices_log, 'r').read()
                    device_type = public.device_type_android(devices)
                    if device_type.strip() == 'Android':
                        self.get_log_str.set('您所连接的设备为Android\n无法使用一键获取日志功能')
                    else:
                        clean_log_content = '确定要一键清空设备中的所有日志吗？\n' \
                                            '（1）清空设备中的所有崩溃日志crash_reports\n' \
                                            '（2）清空设备中的所有系统日志syslog\n' \
                                            '点击“确定”立刻清空设备中的所有日志，点击“取消”关闭'
                        if tkinter.messagebox.askyesno('清空确认',clean_log_content):
                            self.get_log_str.set('正在清空设备中的所有日志中...')
                            public.execute_cmd('adb -s ' + device + ' shell rm -rf /data/crash_reports')
                            public.execute_cmd('adb -s ' + device + ' shell rm -rf /data/syslog')
                            public.execute_cmd('adb -s ' + device + ' shell rm -rf /data/syslog.*')
                            self.get_log_str.set('已清空设备中的所有日志！')
            self.clean_syslog_button_disable.place_forget()

        t_clean_syslog = threading.Thread(target=t_clean_syslog)
        t_clean_syslog.setDaemon(True)
        t_clean_syslog.start()

    def reset_syslog_bind(self):
        def t_reset_syslog():
            # 一键重置日志文件夹
            self.reset_syslog_button_disable.place(x=50,y=200)
            devices_state = public.device_connect()
            reset_log_content = '确定要一键重置日志文件夹吗？\n' \
                                '（1）清空本地中的所有崩溃日志crash_reports\n' \
                                '（2）清空本地中的所有系统日志syslog\n' \
                                '（3）清空本地中的ADB_get_log(DA)文件夹\n' \
                                '点击“确定”立刻清空本地中的所有日志，点击“取消”关闭'
            if tkinter.messagebox.askyesno('重置确认',reset_log_content):
                self.get_log_str.set('正在重置日志文件夹中...')
                try:
                    shutil.rmtree(linux_log_path)
                    print(linux_log_path + ' 已删除！！！')
                except FileNotFoundError:
                    pass
                self.get_log_str.set('已重置日志文件夹！')
            self.reset_syslog_button_disable.place_forget()

        t_reset_syslog = threading.Thread(target=t_reset_syslog)
        t_reset_syslog.setDaemon(True)
        t_reset_syslog.start()

