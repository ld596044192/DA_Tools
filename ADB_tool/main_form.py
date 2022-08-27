import re
import shutil
import signal
import sys
import time
import tkinter,tkinter.ttk,tkinter.messagebox,tkinter.filedialog
import threading
import os
import public,getpass,pyperclip,win32api
import quickly,screen_record,linux_main,customize_main
import logging
import traceback

# 全局变量标记-设备类型
devices_linux_flag = False
# 全局变量标记-设备检测
adb_service_flag = True
# 全局变量标记-设备UUID
uuid_server_flag = False
# 全局变量标记-获取UUID需要重启时需要处理的标识
uuid_reboot_flag = False
# 全局变量标记-获取UUID时执行处理
uuid_run_flag = False
# 全局变量标记 - 防冲突功能标识
conflict_model_flag = False
# 全局变量标记 - 选择apk路径
apk_path_install_flag = False
# 全局变量标记 - 选择apk路径
apk_install_flag = False
# 点击按钮第一次需要进行处理的标记
first_button_flag = False
tkinter_messagebox_flag = False
# 冲突软件列表
conflict_software_list = ['PhoenixSuit.exe']
username = getpass.getuser()
LOGO_path = public.resource_path(os.path.join('icon', 'android.ico'))
version_path = public.resource_path(os.path.join('version','version_history.txt'))
adb_path = public.resource_path(os.path.join('resources','adb-tools.zip'))
adb_version_path = public.resource_path(os.path.join('resources','Android Debug Bridge version.txt'))
uuid_path = public.resource_path(os.path.join('resources','UUID.ini'))
record_state = public.resource_path(os.path.join('temp','record_state.txt'))
devices_type_log = public.resource_path(os.path.join('temp','devices_type_log.txt'))  # 记录设备类型
my_logo_path = public.resource_path(os.path.join('resources','my_logo.gif'))
linux_sn_path = public.resource_path(os.path.join('resources','linux_sn.ini'))
# 创建临时文件夹
make_dir = 'C:\\Users\\' + username + '\\Documents\\ADB_Tools(DA)\\'
if not os.path.exists(make_dir):
    os.makedirs(make_dir)
count_path = make_dir + 'screenshots_count.txt'
# 主程序启动标志
root_state = make_dir + 'root_state.txt'
# 截图页面启动标志
screen_page = make_dir + 'screen_page_state.txt'
# 安装页面启动标志
install_page = make_dir + 'install_page_state.txt'
# 取图页面启动标志
camera_page = make_dir + 'camera_page_state.txt'
# 写号工具页面启动标志
write_number_page = make_dir + 'linux_write_number_state.txt'
# 一键获取日志页面启动标志
get_log_page = make_dir + 'get_log_state.txt'
# 简易ADB - adb-tools检测标志
adb_tools_flag = make_dir + 'adb-tools'
# 卸载APK标记
uninstall_flag = True
# ------------------------------- 录屏功能
# 录屏状态
record_screen_state = make_dir + 'record_state.txt'
# 录屏名称
record_name = make_dir + 'record_name.txt'
# 录屏时间
record_time_txt = make_dir + 'record_time.txt'
# 记录程序位置
exe_path = public.resource_path(os.path.join('temp','exe_path.log'))
# 录屏模式
record_model_log = make_dir + 'record_model.log'
record_count = make_dir + 'record_count.txt'
# 录屏停止处理
record_stop_config = make_dir + 'record_stop.ini'
# ------------------------------- 录屏功能
# ADB升级状态
adb_upgrade_flag = make_dir + 'adb_state.ini'
# 冲突软件名称记录
conflict_software_path = make_dir + 'conflict_software.txt'
# 冲突软件路径记录
conflict_path = make_dir + 'conflict_software_path.txt'
# 记录设置环境变量日志
environ_log = make_dir + 'environ_log.log'
# 临时保存系统日志
syslog_log = make_dir + 'syslog.log'
# 实时保存设备序列号
devices_log = make_dir + 'devices.log'
# 记录apk包路径（检测包名）
apk_path_package_log = make_dir + 'apk_path_package.log'
# 存储aapt分析apk包信息
apk_aapt_log = make_dir + 'apk_aapt_log.log'
# 记录apk包路径（安装apk）
apk_path_log = make_dir + 'apk_path.log'
# 记录apk安装信息
apk_install_log = make_dir + 'apk_install_log.log'
# 启动前初始化
with open(adb_upgrade_flag,'w') as fp:
    fp.write('ADB is the latest version')
with open(conflict_software_path,'w') as fp:
    fp.write('')
# 统一修改版本号
version = 'V1.0.1.5'
version_code = 1015.0
# 统一修改frame的宽高
width = 367
height = 405
# 统一按钮宽度
width_button = 20
# 统一root窗口总宽高
main_width = 600
main_height = 450
# 设置单选按钮跳转时间
radio_waiting_time = 15
# 引入日志
logging.basicConfig(filename=make_dir + 'log.txt',
                    level=logging.DEBUG,
                    filemode='a+',
                    format='[%(asctime)s] [%(levelname)s] >>> \n%(message)s',
                    datefmt='%Y-%m-%d %I:%M:%S')


class MainForm(object):
    def root_form(s):
        s.root = tkinter.Tk()
        s.root.title('ADB测试工具' + version + ' Windows版')
        screenWidth = s.root.winfo_screenwidth()
        screenHeight = s.root.winfo_screenheight()
        w = main_width
        h = main_height
        x = (screenWidth - w) / 2
        y = (screenHeight - h) / 2
        s.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        s.root.iconbitmap(LOGO_path)
        s.root.resizable(0, 0)
        # s.root.attributes("-toolwindow", 2)  # 去掉窗口最大化最小化按钮，只保留关闭
        # s.root.overrideredirect(1)  # 隐藏标题栏 最大化最小化按钮
        # s.root.config(bg=bg)
        # 软件始终置顶
        # s.root.wm_attributes('-topmost', 1)
        # s.root.protocol('WM_DELETE_WINDOW', s.exit)  # 点击Tk窗口关闭时直接调用s.exit，不使用默认关闭
        # 主程序启动标志
        with open(root_state,'w') as fp:
            fp.write('1')

        # 初始化
        s.software_init()
        # 默认显示窗口页面
        s.main_menu_bar()
        s.quickly_frame()

        s.root.mainloop()
        return s.root

    def software_init(s):
        # 每次启动本软件都需要进行初始化

        # 初始化Linux模式下的特定按钮状态
        init_button_files = [screen_page,install_page,camera_page,write_number_page,get_log_page]
        for init_button_file in init_button_files:
            try:
                os.remove(init_button_file)
            except FileNotFoundError:
                pass

        # 创建特定必须的文件
        if not os.path.exists(apk_aapt_log):
            with open(apk_aapt_log,'w') as fp:
                fp.write('')

        # 每次启动需要加载的frame
        s.moving_device_frame()
        s.moving_software_info()

    def main_menu_bar(s):
        # 切换窗口（选择模式）
        s.main_menu = tkinter.Menubutton(s.root,text='快捷模式')
        s.main_menu1 = tkinter.Menubutton(s.root, text='快捷模式')
        s.main_menu1.place(x=0, y=0)
        s.main_menu1.config(state='disable')
        s.screen_menu = tkinter.Menubutton(s.root, text='截图录屏')
        s.screen_menu1 = tkinter.Menubutton(s.root, text='截图录屏')
        s.screen_menu1.config(state='disable')

        s.install_menu = tkinter.Menubutton(s.root, text='安装卸载')
        s.install_menu1 = tkinter.Menubutton(s.root, text='安装卸载')
        s.install_menu1.config(state='disable')

        s.linux_menu = tkinter.Menubutton(s.root, text='Linux模式')
        s.linux_menu1 = tkinter.Menubutton(s.root, text='Linux模式')
        s.linux_menu1.config(state='disable')

        s.customize_menu = tkinter.Menubutton(s.root, text='自定义模式')
        s.customize_menu1 = tkinter.Menubutton(s.root, text='自定义模式')
        s.customize_menu1.config(state='disable')

        s.verion_menu = tkinter.Menubutton(s.root,text='版本历史')
        s.verion_menu1 = tkinter.Menubutton(s.root, text='版本历史')
        s.verion_menu1.config(state='disable')

        s.main_menu.bind('<Button-1>',lambda x:s.display_main_frame())
        s.verion_menu.bind('<Button-1>',lambda x:s.display_version_frame())
        s.screen_menu.bind('<Button-1>',lambda x:s.display_screenshot_frame())
        s.linux_menu.bind('<Button-1>',lambda x:s.display_linux_frame())
        s.install_menu.bind('<Button-1>',lambda x:s.display_install_frame())
        s.customize_menu.bind('<Button-1>',lambda x:s.display_customize_frame())

        s.main_menu.place(x=0,y=0)
        s.screen_menu.place(x=60, y=0)
        s.install_menu.place(x=120,y=0)
        s.linux_menu.place(x=180,y=0)
        s.customize_menu.place(x=240,y=0)
        s.verion_menu.place(x=305,y=0)

        # 连接设备功能
        s.devices_state_label = tkinter.Label(s.root,text='设备连接状态：')
        s.devices_null = tkinter.StringVar()
        s.devices_str = tkinter.StringVar()
        s.devices_success = tkinter.Label(s.root,textvariable=s.devices_str,fg='green')
        s.devices_fail = tkinter.Label(s.root,textvariable=s.devices_null,fg='red')
        s.devices_success.place(x=450, y=0)
        s.devices_state_label.config(command=s.devices_bind())
        s.devices_state_label.place(x=370,y=0)

        # 检测本地adb服务（None则使用内置adb）
        s.adb_state_label = tkinter.Label(s.root, text='ADB服务连接状态：')
        s.adb_state_label.config(command=s.adb_bind())
        s.adb_str = tkinter.StringVar()
        s.adb_success = tkinter.Label(s.root,textvariable=s.adb_str,fg='green')
        s.adb_str.set('正在检测ADB服务连接状态...')
        s.adb_success.place(x=110,y=425)
        s.adb_state_label.place(x=0,y=425)

        # 检测设备类型 Android Linux
        s.devices_type_label = tkinter.Label(s.root,text='设备类型：')
        s.devices_type_str = tkinter.StringVar()
        s.devices_type_error = tkinter.StringVar()
        s.devices_type_success = tkinter.Label(s.root,textvariable=s.devices_type_str,fg='green')
        s.devices_type_fail = tkinter.Label(s.root,textvariable=s.devices_type_error,fg='red')
        s.devices_type_str.set('正在检测设备类型...')
        s.devices_type_label.place(x=270,y=425)
        s.devices_type_success.place(x=325,y=425)

        # 设备序列号下拉框说明
        content = '''
                连接多设备时所有序列号都在下面哦~
                可根据序列号选择对应设备进行操作
                '''
        s.more_devices_label = tkinter.Label(s.root, text=content, fg='red')
        s.more_devices_label.place(x=310, y=20)

        # 所有设备序列号下拉框选择
        s.more_devices_list = [' ']
        s.more_devices_value = tkinter.StringVar()
        s.more_devices_combobox = tkinter.ttk.Combobox(s.root, state="readonly", width=25,
                                                             textvariable=s.more_devices_value)
        s.more_devices_combobox.config(command=s.more_devices_bind())
        # state：“正常”，“只读”或“禁用”之一。在“只读”状态下，可能无法直接编辑该值，并且用户只能从下拉列表中选择值。在“正常”状态下，文本字段可直接编辑。在“禁用”状态下，不可能进行交互。
        s.more_devices_combobox.place(x=380, y=80)

        # 循环单选按钮
        s.moving_str = tkinter.IntVar()
        s.moving_radio_button1 = tkinter.Radiobutton(s.root, variable=s.moving_str, value=0)
        s.moving_radio_button1.place(x=375, y=335)
        s.moving_radio_button2 = tkinter.Radiobutton(s.root, variable=s.moving_str, value=1)
        s.moving_radio_button2.place(x=390, y=335)
        s.moving_radio_button1.config(command=s.moving_radio_bind())

    def moving_radio_bind(s):
        def t_moving_radio():
            # 循环跳转单选按钮
            while True:
                s.moving_str.set(0)
                time.sleep(radio_waiting_time)
                s.moving_str.set(1)
                time.sleep(radio_waiting_time)

        t_moving_radio = threading.Thread(target=t_moving_radio)
        t_moving_radio.setDaemon(True)
        t_moving_radio.start()

    def moving_device_frame(s):
        # 动态设备信息frame
        s.moving_device_frame1 = tkinter.Frame(s.root,width=210,height=220)

        # 设备类型
        s.devices_mode_str = tkinter.StringVar()
        s.devices_mode = tkinter.Label(s.moving_device_frame1,textvariable=s.devices_mode_str,width=29,bg='black',fg='#FFFFFF')
        s.devices_mode.place(x=0,y=0)
        s.devices_mode_str.set('此处显示设备类型')

        # 获取设备序列号（安卓+Linux）
        s.devices_sn_str = tkinter.StringVar()
        s.devices_sn = tkinter.Label(s.moving_device_frame1, textvariable=s.devices_sn_str, width=29, bg='black',
                                       fg='#FFFFFF')
        s.devices_sn.place(x=0, y=30)
        s.devices_sn_str.set('此处显示设备序列号（安卓）')

        # 获取设备MAC（物理）地址
        s.devices_mac_str = tkinter.StringVar()
        s.devices_mac = tkinter.Label(s.moving_device_frame1, textvariable=s.devices_mac_str, width=29, bg='black',
                                     fg='#FFFFFF')
        s.devices_mac.place(x=0, y=60)
        s.devices_mac_str.set('此处显示设备MAC地址')

        # 获取设备ip地址
        s.devices_ip_str = tkinter.StringVar()
        s.devices_ip = tkinter.Label(s.moving_device_frame1, textvariable=s.devices_ip_str, width=29, bg='black',
                                      fg='#FFFFFF')
        s.devices_ip.place(x=0, y=90)
        s.devices_ip_str.set('此处显示设备ip地址')

        # 获取安卓版本号  wraplength表示内容超过该宽度就会自动换行
        s.android_version_str = tkinter.StringVar()
        s.android_version = tkinter.Label(s.moving_device_frame1, textvariable=s.android_version_str, width=29, bg='black',
                                     fg='#FFFFFF',wraplength=200)
        s.android_version.place(x=0, y=120)
        s.android_version_str.set('此处显示安卓版本号')

        # 获取安卓的应用版本号和固件版本号
        s.software_version_str = tkinter.StringVar()
        s.software_version = tkinter.Label(s.moving_device_frame1, textvariable=s.software_version_str, width=29,
                                          bg='black',
                                          fg='#FFFFFF')
        s.software_version.place(x=0, y=150)
        s.software_version_str.set('此处显示安卓应用版本号')
        s.firmware_version_str = tkinter.StringVar()
        s.firmware_version = tkinter.Label(s.moving_device_frame1, textvariable=s.firmware_version_str, width=29,
                                           bg='black',fg='#FFFFFF',wraplength=200)
        s.firmware_version.place(x=0, y=180)
        s.firmware_version_str.set('此处显示安卓固件版本号')

    def moving_software_info(s):
        s.moving_software_info_frame = tkinter.Frame(s.root,width=210,height=220)
        # 个人常用头像
        my_log_photo = tkinter.PhotoImage(file=my_logo_path)
        s.my_logo_label = tkinter.Label(s.moving_software_info_frame,bg='red')
        s.my_logo_label.config(image=my_log_photo)
        s.my_logo_label.image = my_log_photo
        s.my_logo_label.place(x=45,y=10)

        # 个人简介信息
        my_info_content = 'ADB工具制作者：达之领域\n' \
                          '联系方式：596044192@qq.com\n' \
                          '        ld596044192@gmail.com'
        s.my_info_label = tkinter.Label(s.moving_software_info_frame,text=my_info_content,justify=tkinter.LEFT)
        s.my_info_label.place(x=10,y=150)

    def more_devices_bind(s):
        def t_more_devices():
            devices_current_flag = False
            # 多设备连接匹配
            while True:
                adb_install_state = open(adb_upgrade_flag, 'r').read()
                # conflict_software_flag = public.find_pid_name(conflict_software_list)
                if adb_install_state == 'ADB upgrade':
                    s.more_devices_list = ['ADB升级中不可用']
                    s.more_devices_combobox['value'] = s.more_devices_list
                    s.more_devices_combobox.current(0)
                    print('ADB升级中3...')
                else:
                    # if conflict_software_flag:
                    #     # print('测试是否已屏蔽 - 多设备检测')
                    #     pass
                    # else:
                    devices_list = public.device_connect()
                    # print(devices_list)
                    if not devices_list:
                        s.more_devices_list = ['没有连接任何设备']
                        s.more_devices_combobox['value'] = s.more_devices_list
                        s.more_devices_combobox.current(0)
                        devices_current_flag = False
                        continue
                    elif s.more_devices_value.get().strip() == 'List of':
                        print(s.more_devices_list)
                        print('删除异常List of...')
                        index = s.more_devices_list.index('List of')
                        print('异常数据索引 ：' + str(index))
                        s.more_devices_list.pop(index)  # 删除“List of”异常元素
                        s.more_devices_combobox['value'] = s.more_devices_list
                        try:
                            s.more_devices_combobox.current(0)
                        except tkinter.TclError:
                            print('出现TclError，忽略即可！！！')
                        continue
                    else:
                        s.more_devices_list = devices_list
                        s.more_devices_combobox['value'] = s.more_devices_list
                        # 保存设备序列号以便后面功能使用，实时同步
                        with open(devices_log, 'w') as fp:
                            fp.write(s.more_devices_value.get())
                        if not devices_current_flag:
                            # 首次连接设备后只匹配首个序列号一次
                            s.more_devices_combobox.current(0)
                            devices_current_flag = True
                            continue
                        else:
                            pass
                time.sleep(1)

        t_more_devices = threading.Thread(target=t_more_devices)
        t_more_devices.setDaemon(True)
        t_more_devices.start()

    def display_main_frame(s):
        # 显示快捷模式主窗口
        s.quickly_frame()
        s.verion_menu1.place_forget()
        s.screen_menu1.place_forget()
        s.install_menu1.place_forget()
        s.linux_menu1.place_forget()
        s.customize_menu1.place_forget()
        s.main_menu1.place(x=0, y=0)
        try:
            s.screen_frame1.place_forget()
            s.linux_frame1.place_forget()
            s.verion_frame_full.place_forget()
            s.install_frame1.place_forget()
            s.customize_frame1.place_forget()
        except AttributeError:
            print('所选窗口未启动 -警告信息Logs（可忽略）')
            pass

    def display_screenshot_frame(s):
        # 显示截图录屏窗口
        s.screen_frame()
        s.main_menu1.place_forget()
        s.linux_menu1.place_forget()
        s.install_menu1.place_forget()
        s.customize_menu1.place_forget()
        s.screen_menu1.place(x=60, y=0)
        s.verion_menu1.place_forget()
        try:
            s.quickly_frame1.place_forget()
            s.linux_frame1.place_forget()
            s.verion_frame_full.place_forget()
            s.install_frame1.place_forget()
            s.customize_frame1.place_forget()
        except AttributeError:
            print('所选窗口未启动 -警告信息Logs（可忽略）')
            pass

    def display_install_frame(s):
        # 显示安装卸载窗口
        s.install_menu1.place(x=120, y=0)
        s.install_frame()
        s.screen_menu1.place_forget()
        s.main_menu1.place_forget()
        s.verion_menu1.place_forget()
        s.linux_menu1.place_forget()
        s.customize_menu1.place_forget()
        try:
            s.quickly_frame1.place_forget()
            s.screen_frame1.place_forget()
            s.verion_frame_full.place_forget()
            s.linux_frame1.place_forget()
            s.customize_frame1.place_forget()
        except AttributeError:
            print('所选窗口未启动 -警告信息Logs（可忽略）')
            pass

        # 初始化按钮
        if apk_install_flag:
            s.apk_button_disable.place(x=20,y=325)
            s.install_str.set('正在安装apk中...')

    def display_linux_frame(s):
        # 显示Linux模式窗口
        s.linux_menu1.place(x=180, y=0)
        s.linux_frame()
        s.screen_menu1.place_forget()
        s.main_menu1.place_forget()
        s.verion_menu1.place_forget()
        s.install_menu1.place_forget()
        s.customize_menu1.place_forget()
        try:
            s.quickly_frame1.place_forget()
            s.screen_frame1.place_forget()
            s.verion_frame_full.place_forget()
            s.install_frame1.place_forget()
            s.customize_frame1.place_forget()
        except AttributeError:
            print('所选窗口未启动 -警告信息Logs（可忽略）')
            pass

    def display_customize_frame(s):
        # 显示自定义模式窗口
        s.customize_menu1.place(x=240, y=0)
        s.customize_frame()
        s.main_menu1.place_forget()
        s.screen_menu1.place_forget()
        s.linux_menu1.place_forget()
        s.install_menu1.place_forget()
        s.verion_menu1.place_forget()
        try:
            s.linux_frame1.place_forget()
            s.quickly_frame1.place_forget()
            s.screen_frame1.place_forget()
            s.install_frame1.place_forget()
            s.verion_frame.place_forget()
        except AttributeError:
            print('所选窗口未启动 -警告信息Logs（可忽略）')
            pass

    def display_version_frame(s):
        # 显示版本历史窗口
        s.version_history_frame()
        s.main_menu1.place_forget()
        s.screen_menu1.place_forget()
        s.linux_menu1.place_forget()
        s.install_menu1.place_forget()
        s.customize_menu1.place_forget()
        s.verion_menu1.place(x=305, y=0)
        try:
            s.linux_frame1.place_forget()
            s.quickly_frame1.place_forget()
            s.screen_frame1.place_forget()
            s.install_frame1.place_forget()
        except AttributeError:
            print('所选窗口未启动 -警告信息Logs（可忽略）')
            pass

    def quickly_frame(s):
        s.quickly_frame1 = tkinter.Frame(s.root,width=width,height=height)

        # 返回功能
        s.back_button = tkinter.Button(s.quickly_frame1,text='返回 & 后退（安卓）',width=width_button)
        s.back_button.bind('<Button-1>',lambda x: s.back_bind())
        s.back_button_disable = tkinter.Button(s.quickly_frame1,text='正在返回...',width=width_button)
        s.back_button_disable.config(state='disable')
        s.back_button.place(x=20,y=20)

        # 进入系统设置功能
        s.settings_button = tkinter.Button(s.quickly_frame1,text='进入系统设置（安卓）',width=width_button)
        s.settings_button.bind('<Button-1>',lambda x: s.settings_bind())
        s.settings_button_disable = tkinter.Button(s.quickly_frame1,text='正在进入中...',width=width_button)
        s.settings_button_disable.config(state='disable')
        s.settings_button.place(x=190,y=20)

        # 重启设备功能（通用）
        s.reboot_button = tkinter.Button(s.quickly_frame1,text='重启设备（通用）',width=width_button)
        s.reboot_button.bind('<Button-1>',lambda x: s.reboot_bind())
        s.reboot_str = tkinter.StringVar()
        s.reboot_button_disable = tkinter.Button(s.quickly_frame1,textvariable=s.reboot_str,width=width_button)
        s.reboot_button_disable.config(state='disable')
        s.reboot_button.place(x=20,y=60)

        # 关机设备功能
        s.shutdown_button = tkinter.Button(s.quickly_frame1,text='设备关机（安卓）',width=width_button)
        s.shutdown_button.bind('<Button-1>',lambda x: s.shutdown_bind())
        s.shutdown_button_disable = tkinter.Button(s.quickly_frame1,text='正在关机...',width=width_button)
        s.shutdown_button_disable.config(state='disable')
        s.shutdown_button.place(x=190,y=60)

        # 清理缓存（初始化）功能
        s.clear_button = tkinter.Button(s.quickly_frame1,text='清理缓存（初始化-安卓）',width=width_button)
        s.clear_button.bind('<Button-1>',lambda x: s.clear_bind())
        s.clear_button_disable = tkinter.Button(s.quickly_frame1,text='正在初始化...',width=width_button)
        s.clear_button_disable.config(state='disable')
        s.clear_button.place(x=20,y=100)

        # 终止（结束）程序
        s.kill_button = tkinter.Button(s.quickly_frame1,text='终止（结束）应用（安卓）',width=width_button)
        s.kill_button.bind('<Button-1>',lambda x: s.kill_bind())
        s.kill_button_disable = tkinter.Button(s.quickly_frame1,text='正在结束...',width=width_button)
        s.kill_button_disable.config(state='disable')
        s.kill_button.place(x=190,y=100)

        # 返回Launcher桌面
        s.desktop_button = tkinter.Button(s.quickly_frame1,text='返回桌面（安卓）',width=width_button)
        s.desktop_button.bind('<Button-1>',lambda x: s.desktop_bind())
        s.desktop_button_disable = tkinter.Button(s.quickly_frame1,text='正在返回...',width=width_button)
        s.desktop_button_disable.config(state='disable')
        s.desktop_button.place(x=20,y=140)

        # 唤醒屏幕
        s.awake_button = tkinter.Button(s.quickly_frame1,text='唤醒屏幕（安卓）',width=width_button)
        s.awake_button.bind('<Button-1>', lambda x: s.awake_bind())
        s.awake_button_disable = tkinter.Button(s.quickly_frame1, text='正在唤醒...', width=width_button)
        s.awake_button_disable.config(state='disable')
        s.awake_button.place(x=190, y=140)

        # 关机设备功能（Linux）
        s.linux_shutdown_button = tkinter.Button(s.quickly_frame1, text='设备关机（Linux）', width=width_button)
        s.linux_shutdown_button.bind('<Button-1>', lambda x: s.linux_shutdown_bind())
        s.linux_shutdown_button_disable = tkinter.Button(s.quickly_frame1, text='正在关机...', width=width_button)
        s.linux_shutdown_button_disable.config(state='disable')
        s.linux_shutdown_button.place(x=20, y=180)

        # 一键复制SN序列号功能（通用）
        s.copy_SN_button = tkinter.Button(s.quickly_frame1, text='一键复制序列号（通用）', width=width_button)
        s.copy_SN_button.bind('<Button-1>', lambda x: s.copy_SN_bind())
        s.copy_SN_button_disable = tkinter.Button(s.quickly_frame1, text='正在一键复制中...', width=width_button)
        s.copy_SN_button_disable.config(state='disable')
        s.copy_SN_button.place(x=190, y=180)

        # 使用说明
        content = '''
        使用说明：
        若没连接设备时，点击按钮无任何现象属于正常现象
        连接设备后点击按钮，可在设备上观察调试现象
        若设备类型与按钮提示的类型不符合时无现象为正常
        '''
        s.instructions_label = tkinter.Label(s.quickly_frame1,text=content,fg='red')
        s.instructions_label.place(x=20,y=220)
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
        # s.record_readme_label = tkinter.Label(s.screen_frame1, text=content, fg='red', font=('宋体', 10))
        s.record_readme_button = tkinter.Button(s.screen_frame1,text='点击显示录屏注意事项',width=width_button)
        s.record_readme_button.bind('<Button-1>',lambda x:s.record_readme_bind())
        s.record_readme_button.place(x=120, y=260)

        # 录屏时间说明
        content = '''请选择录屏时间：'''
        s.record_time_label = tkinter.Label(s.screen_frame1, text=content)
        s.record_time_label.place(x=20, y=300)

        # 录屏时间下拉框
        s.record_time = tkinter.StringVar()
        s.record_combobox = tkinter.ttk.Combobox(s.screen_frame1, state="readonly",width=5, textvariable=s.record_time)
        # state：“正常”，“只读”或“禁用”之一。在“只读”状态下，可能无法直接编辑该值，并且用户只能从下拉列表中选择值。在“正常”状态下，文本字段可直接编辑。在“禁用”状态下，不可能进行交互。
        s.record_combobox['value'] = ('180秒', '120秒', '60秒', '30秒', '10秒')
        s.record_combobox.current(0)
        s.record_combobox.place(x=120, y=300)

        # 录屏模式单选按钮
        s.record_model_str = tkinter.IntVar()
        s.record_radio_button1 = tkinter.Radiobutton(s.screen_frame1,text='手动模式',variable=s.record_model_str,value=0)
        s.record_radio_button1.place(x=200,y=300)
        s.record_radio_button2 = tkinter.Radiobutton(s.screen_frame1, text='连续模式', variable=s.record_model_str, value=1)
        s.record_radio_button2.place(x=270, y=300)
        # 气泡提示对话框
        public.CreateToolTip(s.record_radio_button1,text='手动模式：到达指定时间就会自动停止（没到达指定时间时也可以手动停止）\n且不会重新录制')
        public.CreateToolTip(s.record_radio_button2,text='连续模式：到达指定时间会自动重新录制（除非手动停止）\n，每一轮录制后都会自动保存')

        # 录屏按钮
        s.record_button = tkinter.Button(s.screen_frame1, text='开始录屏', width=width_button)
        s.record_button.bind('<Button-1>', lambda x: s.record_bind())
        s.record_button_disable = tkinter.Button(s.screen_frame1, text='正在录屏中', width=width_button)
        s.record_button_disable.config(state='disable')
        s.record_button.place(x=20, y=330)

        # 停止录屏按钮
        s.record_stop_button = tkinter.Button(s.screen_frame1, text='停止录屏', width=width_button)
        s.record_stop_button.bind('<Button-1>', lambda x:s.record_stop_bind())
        s.record_stop_button_disable = tkinter.Button(s.screen_frame1, text='停止录屏', width=width_button)
        s.record_stop_button_disable.config(state='disable')
        s.record_stop_button_disable.place(x=200, y=330)

        # 打开录屏文件夹按钮
        s.open_record_button = tkinter.Button(s.screen_frame1, text='打开录屏文件夹', width=width_button)
        s.open_record_button.bind('<Button-1>', lambda x: s.open_record_bind())
        s.open_record_button_disable = tkinter.Button(s.screen_frame1, text='正在打开...', width=width_button)
        s.open_record_button_disable.config(state='disable')
        s.open_record_button.place(x=20, y=370)

        # 一键重置按钮
        s.reset_button = tkinter.Button(s.screen_frame1, text='一键重置', width=width_button)
        s.reset_button.bind('<Button-1>', lambda x: s.reset_bind())
        s.reset_button_disable = tkinter.Button(s.screen_frame1, text='一键重置', width=width_button)
        s.reset_button_disable.config(state='disable')
        s.reset_button_disable.bind('<Button-1>',lambda x: s.reset_disable_bind())
        s.reset_button.place(x=200, y=370)

        s.screen_frame1.place(y=20)

    def record_readme_bind(s):
        def t_record_readme():
            # 显示录屏注意事项内容
            content = '''* 说明：
            1.上方可以修改录屏后生成的文件名称(默认demo)
            2.生成的文件保存在桌面上的“ADB工具-录屏（DA）”里面
            3.录屏使用说明：录屏时需要操作设备，不操作就保存生成的文件时长为00:00
            4.录屏时请勿使用本地ADB服务，否则会中断录屏
            5.如果你正在进行设备固件升级，需要使用ADB本地服务，请勿使用录屏功能（因为录屏结束时会中断ADB服务）
            '''
            tkinter.messagebox.showinfo('录屏注意事项',content)

        t_record_readme = threading.Thread(target=t_record_readme)
        t_record_readme.setDaemon(True)
        t_record_readme.start()

    def install_frame(s):
        # 显示安装与卸载模式窗口
        s.install_frame1 = tkinter.Frame(s.root, width=width, height=height)

        # 卸载状态栏
        s.uninstall_str = tkinter.StringVar()
        s.uninstall_label = tkinter.Label(s.install_frame1, textvariable=s.uninstall_str, bg='black', fg='#FFFFFF',
                                           width=46, height=2)
        s.uninstall_label.place(x=20, y=20)
        s.uninstall_str.set('此处显示卸载apk状态')

        # 检测包名按钮
        s.check_package_name_button = tkinter.Button(s.install_frame1, text='点击检测当前包名', width=width_button)
        s.check_package_name_button.bind('<Button-1>', lambda x: s.check_package_name_bind(uninstall_flag))
        s.check_package_name_button_disable = tkinter.Button(s.install_frame1, text='正在检测中...', width=width_button)
        s.check_package_name_button_disable.config(state='disable')
        s.check_package_name_button.place(x=20, y=80)

        # 卸载APk按钮
        s.uninstall_button = tkinter.Button(s.install_frame1, text='一键卸载APK', width=width_button)
        s.uninstall_button.bind('<Button-1>', lambda x: s.uninstall_bind())
        s.uninstall_button_disable = tkinter.Button(s.install_frame1, text='正在卸载中...', width=width_button)
        s.uninstall_button_disable.config(state='disable')
        s.uninstall_button.place(x=200, y=80)

        # 检测包名说明
        check_package_content = '请把apk包拖拽到下方框后，点击“获取apk包名”可获得Apk包名\n' \
                                '若拖放功能不可用，也可以点击“浏览”选择apk包哦~'
        s.check_package_label = tkinter.Label(s.install_frame1,fg='red',text=check_package_content)
        s.check_package_label.place(x=20,y=120)

        # apk包文件路径单行文本框
        s.apk_path_package_str = tkinter.StringVar()
        s.apk_path_package_entry = tkinter.Entry(s.install_frame1,textvariable=(s.apk_path_package_str),
                                                    width=40, highlightcolor='yellow', validate="focusin"
                                                    , highlightthickness=5)
        s.apk_path_package_entry.place(x=20,y=160)

        # apk文件获取路径拖拽功能（windnd）
        public.windnd_hook_files(s.apk_path_package_entry,s.apk_path_package_str)
        if not os.path.exists(apk_path_package_log):
            with open(apk_path_package_log, 'w') as fp:
                fp.write('')
        path_msg = open(apk_path_package_log,'r').read()
        s.apk_path_package_entry.insert(tkinter.END,path_msg)

        # 浏览apk文件按钮
        s.apk_path_package_button = tkinter.Button(s.install_frame1,text='浏览')
        s.apk_path_package_button_disable = tkinter.Button(s.install_frame1,text='浏览')
        s.apk_path_package_button.bind('<Button-1>',lambda x:s.open_apk_path_files(apk_path_install_flag))
        s.apk_path_package_button_disable.config(state='disable')
        s.apk_path_package_button.place(x=320,y=160)

        # 检测apk文件包名按钮
        s.apk_package_button = tkinter.Button(s.install_frame1,text='获取apk文件包名',width=width_button)
        s.apk_package_button_disable = tkinter.Button(s.install_frame1,text='获取apk文件包名',width=width_button)
        s.apk_package_button_disable.config(state='disable')
        s.apk_package_button.bind('<Button-1>',lambda x:s.apk_package_bind())
        s.apk_package_button.place(x=20,y=200)

        # 一键复制粘贴apk包名按钮
        s.apk_package_copy_button = tkinter.Button(s.install_frame1, text='一键复制包名', width=width_button)
        s.apk_package_copy_button_disable = tkinter.Button(s.install_frame1, text='正在复制中...', width=width_button)
        s.apk_package_copy_button_disable.config(state='disable')
        s.apk_package_copy_button.bind('<Button-1>', lambda x: s.apk_package_copy_bind())
        s.apk_package_copy_button.place(x=200, y=200)

        # 安装状态栏
        s.install_str = tkinter.StringVar()
        s.install_label = tkinter.Label(s.install_frame1, textvariable=s.install_str, bg='black', fg='#FFFFFF',
                                          width=46, height=2)
        s.install_label.place(x=20, y=240)
        s.install_str.set('此处显示安装apk状态')

        # 安装apk单行文本框
        s.apk_path_str = tkinter.StringVar()
        s.apk_path_entry = tkinter.Entry(s.install_frame1, textvariable=s.apk_path_str,
                                                 width=40, highlightcolor='yellow', validate="focusin"
                                                 , highlightthickness=5)
        s.apk_path_entry.place(x=20, y=285)

        # 安装apk拖拽功能（windnd）
        public.windnd_hook_files(s.apk_path_entry, s.apk_path_str)
        if not os.path.exists(apk_path_log):
            with open(apk_path_log, 'w') as fp:
                fp.write('')
        apk_path_msg = open(apk_path_log, 'r').read()
        s.apk_path_entry.insert(tkinter.END, apk_path_msg)

        # 浏览apk文件按钮（安装apk）
        s.apk_path_button = tkinter.Button(s.install_frame1, text='浏览')
        s.apk_path_button_disable = tkinter.Button(s.install_frame1, text='浏览')
        s.apk_path_button.bind('<Button-1>', lambda x: s.apk_path_insatll_bind())
        s.apk_path_button_disable.config(state='disable')
        s.apk_path_button.place(x=320, y=285)

        # 安装apk文件按钮
        s.apk_button = tkinter.Button(s.install_frame1, text='一键安装apk', width=width_button)
        s.apk_button_disable = tkinter.Button(s.install_frame1, text='正在安装中...', width=width_button)
        s.apk_button_disable.config(state='disable')
        s.apk_button.bind('<Button-1>', lambda x: s.apk_install_bind())
        s.apk_button.place(x=20, y=325)

        # 查看安装信息按钮
        s.apk_install_info_button = tkinter.Button(s.install_frame1, text='查看安装信息', width=width_button)
        s.apk_install_info_button_disable = tkinter.Button(s.install_frame1, text='查看安装信息', width=width_button)
        s.apk_install_info_button_disable.config(state='disable')
        s.apk_install_info_button.bind('<Button-1>', lambda x: s.apk_install_info_bind())
        s.apk_install_info_button.place(x=200, y=325)

        # 选择apk安装模式label
        s.apk_install_mode_label = tkinter.Label(s.install_frame1,text='请选择安装模式：')
        s.apk_install_mode_label.place(x=20,y=365)

        # apk安装模式下拉框选择
        s.apk_install_mode_value = tkinter.StringVar()
        s.apk_install_mode_combobox = tkinter.ttk.Combobox(s.install_frame1, state="readonly", width=25,
                                                       textvariable=s.apk_install_mode_value)
        s.apk_install_mode_combobox['value'] = ('默认','-d选项 无视版本高低安装')
        s.apk_install_mode_combobox.current(0)
        # state：“正常”，“只读”或“禁用”之一。在“只读”状态下，可能无法直接编辑该值，并且用户只能从下拉列表中选择值。在“正常”状态下，文本字段可直接编辑。在“禁用”状态下，不可能进行交互。
        s.apk_install_mode_combobox.place(x=120, y=365)

        s.install_frame1.place(y=20)

    def linux_frame(s):
        # 显示Linux模式窗口
        s.linux_frame1 = tkinter.Frame(s.root, width=width, height=height)

        # 设备初始化说明
        init_content = '注意：Linux设备使用本软件功能前需要初始化！\n否则无法正常使用下面功能哦'
        s.init_label = tkinter.Label(s.linux_frame1, text=init_content, fg='red',font=('宋体', 10))
        s.init_label.place(x=20, y=20)

        # 初始化按钮
        s.init_str = tkinter.StringVar()
        s.linux_init_Button = tkinter.Button(s.linux_frame1, text='初始化设备', width=width_button)
        s.linux_init_Button_disable = tkinter.Button(s.linux_frame1, text='初始化设备', width=width_button)
        s.linux_init_Button_disable.config(state='disable')
        s.linux_init_Button.bind('<Button-1>', lambda x: linux_main.devices_init(s.init_str,s.linux_init_Button
                                                    ,s.linux_init_Button_disable,s.more_devices_value.get()))
        s.linux_init_Button_disable.place(x=200, y=110)

        # 重新检测按钮
        s.init_again_Button = tkinter.Button(s.linux_frame1, text='点击重新检测', width=width_button)
        s.init_again_Button.bind('<Button-1>',lambda x:linux_main.check_init(s.init_str,s.linux_init_Button
                                    ,s.linux_init_Button_disable,devices_linux_flag,s.linux_all_button_close
                                    ,s.more_devices_value.get()))
        s.init_again_Button.place(x=20,y=110)

        # 初始化状态栏
        s.init_label = tkinter.Label(s.linux_frame1, textvariable=s.init_str, bg='black', fg='#FFFFFF',
                                       width=46, height=2)
        s.init_label.config(command=linux_main.check_init(s.init_str,s.linux_init_Button,s.linux_init_Button_disable,
                                devices_linux_flag,s.linux_all_button_close,s.more_devices_value.get()))
        s.init_label.place(x=20, y=60)
        s.init_str.set('此处显示初始化状态')

        # 功能禁用状态标签
        button_disable_content = '该设备没有初始化，已隐藏所有功能\n请点击上方按钮进行设备初始化\n以便开启所有Linux功能' \
                                 '\n温馨提示：\n如果设备已初始化但功能无法使用\n请检查设备是否正常已连接\n如已连接请点击“重新检测”按钮进行检测'
        s.linux_button_label = tkinter.Label(s.linux_frame1, text=button_disable_content, fg='red',
                                     width=46, height=7)
        s.linux_button_bind()

        # 截图功能
        s.linux_screen_Button = tkinter.Button(s.linux_frame1,text='截图工具（Linux）',width=width_button)
        s.linux_screen_Button_disable = tkinter.Button(s.linux_frame1,text='截图工具（Linux）',width=width_button)
        s.linux_screen_Button.bind('<Button-1>',lambda x:s.linux_screen_bind())
        s.linux_screen_Button_disable.config(state='disable')
        s.linux_screen_Button.place(x=20,y=190)

        # 关闭开发者模式
        s.linux_developer_mode_Button_close = tkinter.Button(s.linux_frame1, text='访问设备本地盘', width=width_button)
        s.linux_developer_mode_Button_close_disable = tkinter.Button(s.linux_frame1, text='正在关闭开发者模式...', width=width_button)
        s.linux_developer_mode_Button_close.bind('<Button-1>', lambda x: s.linux_developer_mode_close_bind())
        s.linux_developer_mode_Button_close_disable.config(state='disable')
        s.linux_developer_mode_Button_close.place(x=200, y=190)
        s.linux_developer_mode_content = """访问设备本地盘需要关闭ADB命令，届时本工具不能连接该设备\n恢复ADB命令需要手动在设备上的“设置-关于-固件版本”，连续点击5下后输入密码“2022#888”后点击确定再重启
恢复ADB命令后，计算机不能访问设备本地盘，但本工具可连接该设备\n在adb shell中通过cd /mnt/UDISK/ 也可访问到本地盘的数据"""
        public.CreateToolTip(s.linux_developer_mode_Button_close,s.linux_developer_mode_content)

        # 安装软件
        s.linux_install = tkinter.Button(s.linux_frame1, text='一键安装工具（Linux）', width=width_button)
        s.linux_install_disable = tkinter.Button(s.linux_frame1, text='一键安装工具（Linux）', width=width_button)
        s.linux_install.bind('<Button-1>', lambda x: s.linux_install_bind())
        s.linux_install_disable.config(state='disable')
        s.linux_install.place(x=20,y=230)

        # 一键取图
        s.linux_camera = tkinter.Button(s.linux_frame1, text='一键取图工具（Linux）', width=width_button)
        s.linux_camera_disable = tkinter.Button(s.linux_frame1, text='一键取图工具（Linux）', width=width_button)
        s.linux_camera.bind('<Button-1>', lambda x: s.linux_camera_bind())
        s.linux_camera_disable.config(state='disable')
        s.linux_camera.place(x=20, y=270)

        # 写号工具
        s.write_number = tkinter.Button(s.linux_frame1, text='写号工具（Linux）', width=width_button)
        s.write_number_disable = tkinter.Button(s.linux_frame1, text='写号工具（Linux）', width=width_button)
        s.write_number.bind('<Button-1>', lambda x: s.write_number_bind())
        s.write_number_disable.config(state='disable')
        s.write_number.place(x=200, y=230)

        # 一键获取日志
        s.get_log = tkinter.Button(s.linux_frame1, text='一键获取日志（Linux）', width=width_button)
        s.get_log_disable = tkinter.Button(s.linux_frame1, text='一键获取日志（Linux）', width=width_button)
        s.get_log.bind('<Button-1>', lambda x: s.get_log_bind())
        s.get_log_disable.config(state='disable')
        s.get_log.place(x=200, y=270)

        # UUID状态栏
        s.uuid_str = tkinter.StringVar()
        s.uuid_label = tkinter.Label(s.linux_frame1, textvariable=s.uuid_str, bg='black', fg='#FFFFFF',
                                     width=46, height=2)
        s.uuid_label.place(x=20, y=310)
        # s.uuid_str.set('此处显示当前连接设备的UUID\n可以点击下方按钮直接粘贴哦~')

        # UUID重复获取功能
        s.uuid_get = tkinter.Button(s.linux_frame1, text='重新获取UUID', width=width_button)
        s.uuid_get_disable = tkinter.Button(s.linux_frame1, text='正在获取中...', width=width_button)
        s.uuid_get.bind('<Button-1>', lambda x: s.uuid_main_bind())
        s.uuid_get_disable.config(state='disable')
        s.uuid_get.place(x=20, y=360)
        # uuid_remind_content1 = '点击“重新获取”会获取设备的UUID\n' \
        #                       '温馨提示：由于设备机制导致获取UUID时会存在失败的可能性\n' \
        #                       '因此获取设备UUID失败后请再重新获取（直到成功后就无需再获取了）'
        # public.CreateToolTip(s.uuid_get,uuid_remind_content1)

        # UUID复制粘贴功能
        s.uuid_paste = tkinter.Button(s.linux_frame1, text='一键复制UUID', width=width_button)
        s.uuid_paste_disable = tkinter.Button(s.linux_frame1, text='正在复制中...', width=width_button)
        s.uuid_paste.bind('<Button-1>', lambda x: s.uuid_paste_bind())
        s.uuid_paste_disable.config(state='disable')
        s.uuid_paste.place(x=200, y=360)
        # uuid_remind_content2 = '温馨提示：由于设备机制导致获取UUID时会存在失败的可能性\n' \
        #                        '因此获取设备UUID失败后请再重新获取（直到成功后就无需再获取了）'
        # public.CreateToolTip(s.uuid_paste,uuid_remind_content2)

        # 开始默认禁用，根据情况开启
        s.linux_all_button_close()

        s.linux_frame1.place(y=20)

    def customize_frame(s):
        s.customize_frame1 = tkinter.Frame(s.root,width=width,height=height)

        # 查询设备应用流量值
        s.flow_button = tkinter.Button(s.customize_frame1, text='查询应用流量值', width=width_button)
        s.flow_button.bind('<Button-1>', lambda x: s.flow_bind())
        s.flow_button_disable = tkinter.Button(s.customize_frame1, text='查询应用流量值', width=width_button)
        s.flow_button_disable.config(state='disable')
        s.flow_button.place(x=20, y=20)

        s.customize_frame1.place(y=20)

    def linux_all_button_close(s):
        def linux_all_button_place_forget():
            global uuid_server_flag
            global uuid_reboot_flag
            global uuid_run_flag

            # 特殊情况下禁用linux模式所有功能（包含已disable状态的按钮）
            s.linux_screen_Button.place_forget()
            s.linux_screen_Button_disable.place_forget()
            s.linux_developer_mode_Button_close.place_forget()
            s.linux_developer_mode_Button_close_disable.place_forget()
            s.linux_install.place_forget()
            s.linux_install_disable.place_forget()
            s.linux_camera.place_forget()
            s.linux_camera_disable.place_forget()
            s.write_number.place_forget()
            s.write_number_disable.place_forget()
            s.uuid_label.place_forget()
            s.uuid_paste.place_forget()
            s.uuid_paste_disable.place_forget()
            s.uuid_get.place_forget()
            s.uuid_get_disable.place_forget()
            s.get_log.place_forget()
            s.get_log_disable.place_forget()

            # 恢复绑定事件的标识
            if not uuid_reboot_flag:
                uuid_server_flag = False
            else:
                pass
            uuid_run_flag = False

            s.linux_button_label.place(x=20, y=220)

        devices = public.device_connect()
        if not devices:
            s.linux_init_Button.place_forget()
            s.linux_init_Button_disable.place(x=200, y=110)

            linux_all_button_place_forget()
        else:
            linux_all_button_place_forget()

    def linux_all_button_open(s):
        global uuid_server_flag

        # 先禁用初始化按钮
        s.linux_init_Button.place_forget()
        s.linux_init_Button_disable.place(x=200, y=110)

        # 先初始化按钮状态
        if not os.path.exists(screen_page):
            with open(screen_page,'w') as fp:
                fp.write('0')
        if not os.path.exists(install_page):
            with open(install_page, 'w') as fp:
                fp.write('0')
        if not os.path.exists(camera_page):
            with open(camera_page, 'w') as fp:
                fp.write('0')
        if not os.path.exists(write_number_page):
            with open(write_number_page, 'w') as fp:
                fp.write('0')
        if not os.path.exists(get_log_page):
            with open(get_log_page, 'w') as fp:
                fp.write('0')

        # 读取一次Linux所有页面状态
        screen_page_state = open(screen_page,'r').read()
        install_page_state = open(install_page,'r').read()
        camera_page_state = open(camera_page,'r').read()
        write_number_page_state = open(write_number_page,'r').read()
        get_log_page_state = open(get_log_page,'r').read()
        if screen_page_state == '':
            s.linux_screen_Button_disable.place(x=20, y=190)
        else:
            s.linux_screen_Button_disable.place_forget()
            s.linux_screen_Button.place(x=20, y=190)
        if install_page_state == '':
            s.linux_install_disable.place(x=20, y=230)
        else:
            s.linux_install_disable.place_forget()
            s.linux_install.place(x=20, y=230)
        if camera_page_state == '':
            s.linux_camera_disable.place(x=20, y=270)
        else:
            s.linux_camera_disable.place_forget()
            s.linux_camera.place(x=20, y=270)
        if write_number_page_state == '':
            s.write_number_disable.place(x=200, y=230)
        else:
            s.write_number_disable.place_forget()
            s.write_number.place(x=200, y=230)
        if get_log_page_state == '':
            s.get_log_disable.place(x=200, y=270)
        else:
            s.get_log_disable.place_forget()
            s.get_log.place(x=200, y=270)

        # 正常情况下开启linux模式所有功能
        s.linux_button_label.place_forget()
        s.linux_developer_mode_Button_close.place(x=200,y=190)
        s.uuid_label.place(x=20, y=310)
        s.uuid_paste.place(x=200, y=360)
        s.uuid_get.place(x=20, y=360)

        # 启动特定的绑定事件
        if not uuid_server_flag:
            s.uuid_get_bind()  # 自动获取设备UUID
            uuid_server_flag = True

    def version_history_frame(s):
        # 历史版本信息窗口
        s.verion_frame_full = tkinter.Frame(s.root,width=width,height=height)
        s.verion_frame = tkinter.Frame(s.verion_frame_full,width=width,height=height)
        s.scrollbar = tkinter.Scrollbar(s.verion_frame)
        s.version_listbox = tkinter.Listbox(s.verion_frame, width=50, height=19,yscrollcommand=(s.scrollbar.set))
        s.version_listbox.bindtags((s.version_listbox,'all'))
        s.scrollbar.config(command=(s.version_listbox.yview))
        s.scrollbar.pack(side=(tkinter.RIGHT), fill=(tkinter.Y))
        s.version_listbox.pack()
        version_read = open(version_path,'r',encoding='utf-8')
        for readline in version_read.readlines():
            s.version_listbox.insert(tkinter.END, readline)
        version_read.close()
        s.verion_frame.place(y=55)
        s.verion_frame_full.place(y=20)

    def back_bind(s):
        def t_back():
            s.back_button_disable.place(x=20,y=20)
            devices_SN = s.more_devices_value.get()
            quickly.android_back(devices_SN)
            s.back_button_disable.place_forget()

        t_back = threading.Thread(target=t_back)
        t_back.setDaemon(True)
        t_back.start()

    def settings_bind(s):
        def t_settings():
            s.settings_button_disable.place(x=190,y=20)
            devices_SN = s.more_devices_value.get()
            quickly.android_settings(devices_SN)
            s.settings_button_disable.place_forget()

        t_settings = threading.Thread(target=t_settings)
        t_settings.setDaemon(True)
        t_settings.start()

    def reboot_bind(s):
        def t_reboot():
            s.reboot_button_disable.place(x=20,y=60)
            s.reboot_str.set('正在重启...')
            devices_SN = s.more_devices_value.get()
            state = quickly.current_reboot(devices_SN)
            # 若设备没有连接，获取的是None，则恢复正常按钮状态
            if not state:
                s.reboot_button_disable.place_forget()
            else:
                while True:
                    android_os_status = public.execute_cmd('adb -s ' + devices_SN + ' shell getprop sys.boot_completed')
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
            devices_SN = s.more_devices_value.get()
            quickly.android_shutdown(devices_SN)
            s.shutdown_button_disable.place_forget()

        t_shutdown = threading.Thread(target=t_shutdown)
        t_shutdown.setDaemon(True)
        t_shutdown.start()

    def clear_bind(s):
        def t_clear():
            s.clear_button_disable.place(x=20,y=100)
            devices_SN = s.more_devices_value.get()
            quickly.clear_cache(devices_SN)
            s.clear_button_disable.place_forget()

        t_clear = threading.Thread(target=t_clear)
        t_clear.setDaemon(True)
        t_clear.start()

    def kill_bind(s):
        def t_kill():
            s.kill_button_disable.place(x=190,y=100)
            devices_SN = s.more_devices_value.get()
            quickly.terminate_program(devices_SN)
            s.kill_button_disable.place_forget()

        t_kill = threading.Thread(target=t_kill)
        t_kill.setDaemon(True)
        t_kill.start()

    def desktop_bind(s):
        def t_desktop():
            s.desktop_button_disable.place(x=20,y=140)
            devices_SN = s.more_devices_value.get()
            quickly.android_desktop(devices_SN)
            s.desktop_button_disable.place_forget()

        t_desktop = threading.Thread(target=t_desktop)
        t_desktop.setDaemon(True)
        t_desktop.start()

    def awake_bind(s):
        def t_awake():
            s.awake_button_disable.place(x=190,y=140)
            devices_SN = s.more_devices_value.get()
            quickly.android_awake(devices_SN)
            s.awake_button_disable.place_forget()

        t_awake = threading.Thread(target=t_awake)
        t_awake.setDaemon(True)
        t_awake.start()

    def linux_shutdown_bind(s):
        def t_linux_shutdown():
            s.linux_shutdown_button_disable.place(x=20, y=180)
            devices_SN = s.more_devices_value.get()
            quickly.linux_shutdown(devices_SN)
            s.linux_shutdown_button_disable.place_forget()

        t_linux_shutdown = threading.Thread(target=t_linux_shutdown)
        t_linux_shutdown.setDaemon(True)
        t_linux_shutdown.start()

    def copy_SN_bind(s):
        def t_copy_SN():
            s.copy_SN_button_disable.place(x=190, y=180)
            devices_state = public.device_connect()
            if not devices_state:
                tkinter.messagebox.showinfo('粘贴失败', '请连接设备后再复制粘贴吧！！！')
            else:
                devices_SN = s.more_devices_value.get()
                quickly.current_copy_SN(devices_SN)
            s.copy_SN_button_disable.place_forget()

        t_copy_SN = threading.Thread(target=t_copy_SN)
        t_copy_SN.setDaemon(True)
        t_copy_SN.start()

    def devices_bind(s):
        def moving_radio_set():
            if s.moving_str.get() == 0:
                # 隐藏非选中的frame
                try:
                    s.moving_software_info_frame.place_forget()
                except AttributeError:
                    pass
                # 显示选中的frame
                s.moving_device_frame1.place(x=375,y=115)
            elif s.moving_str.get() == 1:
                # 隐藏非选中的frame
                s.moving_device_frame1.place_forget()
                # 显示选中的frame
                s.moving_software_info_frame.place(x=375,y=115)

        def moving_devices():
            # 恢复被隐藏的label
            s.software_version.place(x=0, y=150)

            s.devices_null.set('未连接任何设备！')
            s.devices_type_error.set('未连接任何设备！')
            s.devices_mode_str.set('此处显示设备类型')
            # 取消事件绑定
            s.devices_sn.unbind('<Button-1>')
            s.devices_mac.unbind('<Button-1>')
            s.devices_ip.unbind('<Button-1>')
            s.android_version.unbind('<Button-1>')
            # 还原提示
            s.devices_sn_str.set('此处显示设备序列号（安卓）')
            s.devices_mac_str.set('此处显示设备MAC地址')
            s.devices_ip_str.set('此处显示设备ip地址')
            s.android_version_str.set('此处显示安卓版本号')
            s.software_version_str.set('此处显示安卓应用版本号')
            s.firmware_version_str.set('此处显示安卓固件版本号')

        def t_devices():
            global adb_server_flag,conflict_model_flag
            s.devices_str.set('正在检测设备连接状态...')
            while True:
                # 显示动态单选frame
                moving_radio_set()
                adb_install_state = open(adb_upgrade_flag, 'r').read()
                conflict_software_flag = public.find_pid_name(conflict_software_list)
                conflict_software_name = open(conflict_software_path,'r').read()
                # print('冲突软件标志：' + str(conflict_software_flag))
                # print(conflict_software_name)
                if conflict_software_flag:
                    # 强制关闭冲突软件
                    public.execute_cmd('taskkill /F /IM %s ' % conflict_software_name + ' /T')
                    # 重要提示需要置顶
                    s.root.wm_attributes('-topmost', 1)
                    if tkinter.messagebox.askokcancel('防冲突警告', '已检测到冲突软件 ' + conflict_software_name + ' 正在运行\n'
                                                   '已自动强制关闭冲突软件！！！\n'
                                                   '如果你坚持使用冲突软件，则需要点击“确定”关闭本软件，否则点击“取消”不关闭本软件'):
                                                    # 取消置顶
                                                    s.root.wm_attributes('-topmost', 0)
                                                    my_pid = os.getpid()
                                                    os.kill(my_pid,signal.SIGINT)
                    # 取消置顶
                    s.root.wm_attributes('-topmost', 0)
                else:
                    # if adb_server_flag:
                    #     adb_server_flag = False
                    if adb_install_state == 'ADB upgrade':
                        print('ADB正在升级1....')
                        s.devices_fail.place_forget()
                        s.devices_type_fail.place_forget()
                        s.devices_type_success.place(x=325, y=425)
                        s.devices_success.place(x=450, y=0)
                        s.devices_str.set('ADB正在升级中...')
                        s.devices_type_str.set('ADB正在升级中...')
                    else:
                        devices_finally = public.device_connect()
                        # print('检测设备连接状态 === ' + str(devices_finally))
                        if not devices_finally:
                            s.devices_fail.place(x=470, y=0)
                            s.devices_type_fail.place(x=325,y=425)
                            s.devices_success.place_forget()
                            s.devices_type_success.place_forget()
                            # 动态设备参数调整
                            moving_devices()
                            # 确保切换设备类型时Linux相关功能按钮不会主动显示出来
                            try:
                                s.linux_all_button_close()
                            except AttributeError:
                                pass
                        else:
                            # print('成功检测设备 ++++++ ')
                            s.devices_fail.place_forget()
                            s.devices_type_fail.place_forget()
                            s.devices_success.place(x=450,y=0)
                            s.devices_type_success.place(x=325,y=425)
                            for devices in devices_finally:
                                if len(devices_finally) == 1:
                                    if len(devices) > 15:
                                        # 超过长度限制用...表示
                                        s.devices_str.set(devices[:13] + '... 已连接')
                                    else:
                                        s.devices_str.set(devices + ' 已连接')
                                    continue
                                elif len(devices_finally) > 1:
                                    s.devices_str.set('多部设备已连接')
                                    continue
                            s.update_status()
                time.sleep(1)

        def devices_type():
            try:
                s.devices_type_str.set('正在检测设备类型...')
            except AttributeError:
                pass
            # 设置停顿时间放置线程阻塞
            time.sleep(2)
            while True:
                # 检测设备类型
                global devices_linux_flag
                adb_install_state = open(adb_upgrade_flag,'r').read()
                # conflict_software_flag = public.find_pid_name(conflict_software_list)
                if adb_install_state == 'ADB upgrade':
                    print('ADB正在升级2....')
                else:
                    # if conflict_software_flag:
                    #     # print('测试是否屏蔽 - 检测设备类型')
                    #     pass
                    # else:
                    # print('正在检测设备类型 -----------')
                    try:
                        device_SN = s.more_devices_value.get()
                        device_type = public.device_type_android(device_SN)
                        # print(device_type.strip())  # 调试Logs
                        # 增加strip方法，去掉结果的两边空格以便进行识别
                        if device_type.strip() == 'Android':
                            s.devices_type_str.set('Android（安卓）')
                            devices_linux_flag = False
                            with open(devices_type_log,'w') as fp:
                                fp.write(device_type.strip())
                            # print('安卓')
                            continue
                        elif device_type.strip() == '/bin/sh: getprop: not found':
                            # Linux无法使用adb shell getprop命令
                            device_type_linux = public.execute_cmd('adb -s ' + device_SN + ' shell cat /proc/version')
                            device_type_linux_finally = device_type_linux.split(' ')[0]
                            # print(device_type_linux_finally)  # 调试Logs
                            if device_type_linux_finally == 'Linux':
                                s.devices_type_str.set('Linux')
                                devices_linux_flag = True
                                with open(devices_type_log, 'w') as fp:
                                    fp.write(device_type.strip())
                                # print('Linux')
                                continue
                            else:
                                s.devices_type_str.set('未知设备')
                                # print('未知设备')
                                continue
                    except AttributeError:
                        print('出现AttributeError无影响，请忽略')
                        pass
                time.sleep(1)

        t_devices = threading.Thread(target=t_devices)
        t_devices.setDaemon(True)
        t_devices.start()

        devices_type = threading.Thread(target=devices_type)
        devices_type.setDaemon(True)
        devices_type.start()

    def adb_bind(s):
        # 检测ADB服务状态
        def adb_install_main():
             shutil.copy(adb_path, make_dir)
             # 解压
             zip_path = make_dir + 'adb-tools.zip'
             public.zip_extract(zip_path, make_dir)
             # 清理压缩包
             os.remove(zip_path)
             # 配置环境变量
             public.temporary_environ(adb_tools_flag)
             public.permanent_environ(adb_tools_flag)
             # 打印测试
             print(public.execute_cmd('adb version'))

        def adb_install_upgrade():
            if not os.path.exists(adb_tools_flag):
                adb_install_main()
            else:
                # ADB调试桥版本升级
                adb_version_new = int(open(adb_version_path,'r').read())
                print(adb_version_new)
                adb_version = int(public.adb_version())
                print('当前ADB版本号：' + str(adb_version))
                if adb_version < adb_version_new:
                    # 升级启动状态
                    with open(adb_upgrade_flag, 'w') as fp:
                        fp.write('ADB upgrade')
                    s.adb_str.set('ADB有新版本，正在升级...')
                    # 需要时间停掉所有ADB的行为
                    time.sleep(5)
                    public.execute_cmd('adb kill-server')  # 关闭ADB服务
                    try:
                        shutil.rmtree(adb_tools_flag)  # 删除旧版本ADB文件
                    except FileNotFoundError:
                        print('没有该文件无需删除！！！')
                    adb_install_main()

                    # 版本号格式处理
                    adb_version_list = []
                    adb_version_new_finally = '.'.join(str(adb_version_new)).split('.')
                    i = 1
                    for adb_version in adb_version_new_finally:
                        if i <= 2:
                            adb_version += '.'
                            adb_version_list.append(adb_version)
                        else:
                            adb_version = adb_version
                            adb_version_list.append(adb_version)
                        i += 1

                    adb_version_finally = ''.join(adb_version_list)
                    s.adb_str.set('ADB成功升级为 ' + adb_version_finally)
                    print('ADB升级已完成！')
                    # 升级完成状态
                    with open(adb_upgrade_flag, 'w') as fp:
                        fp.write('ADB upgrade is complete')
                    time.sleep(3)
                else:
                    pass

        def t_adb():
            # time.sleep(5)  # 等待ADB服务启动完毕
            while True:
                time.sleep(1)
                # conflict_software_flag = public.find_pid_name(conflict_software_list)
                # if conflict_software_flag:
                #     # print('测试是否屏蔽 - ADB服务启动')
                #     pass
                # else:
                # 中文状态下
                adb_finally = public.adb_connect()[1]
                print(adb_finally)
                try:
                    # 英文状态下
                    adb_english = ' '.join(public.adb_connect()).split(',')[1]
                    print(adb_english)
                    if adb_finally.strip() == '不是内部或外部命令，也不是可运行的程序' or adb_english.strip() == 'operable program or batch file.':
                        # os.chdir(adb_path)
                        # s.adb_str.set('内置ADB已开启！')
                        s.adb_str.set('正在配置ADB...')
                        adb_install_upgrade()
                        s.adb_str.set('ADB已配置成功！')
                        time.sleep(3)
                        s.adb_str.set('本地ADB已开启！')
                        break
                    else:
                        adb_install_upgrade()  # 用于ADB升级
                        s.adb_str.set('本地ADB已开启！')
                        print(public.execute_cmd('adb version'))
                        break
                except (IndexError,ValueError):
                    print('IndexError异常，无影响！')
                    if adb_finally == '不是内部或外部命令，也不是可运行的程序':
                        # os.chdir(adb_path)
                        # s.adb_str.set('内置ADB已开启！')
                        s.adb_str.set('正在配置ADB...')
                        adb_install_upgrade()
                        s.adb_str.set('ADB已配置成功！')
                        time.sleep(3)
                        s.adb_str.set('本地ADB已开启！')
                        break
                    else:
                        adb_install_upgrade()  # 用于ADB升级
                        s.adb_str.set('本地ADB已开启！')
                        print(public.execute_cmd('adb version'))
                        break

        t_adb = threading.Thread(target=t_adb)
        t_adb.setDaemon(True)
        t_adb.start()

    def main_screenshot(s,touch_name):
        # 截图功能核心逻辑代码
        devices_SN = s.more_devices_value.get()
        screenshot_success = screen_record.main_screenshots(touch_name,devices_SN)
        s.screen_str.set(screenshot_success)

    def screenshot_bind(s):
        def t_screenshot():
            s.screen_button_disable.place(x=20, y=140)
            devices_state = public.device_connect()
            touch_name = s.screen_entry.get()
            s.screen_str.set('正在截图中...')
            # 截图文件名长度检测
            if len(touch_name) <= 8:
                # 检测安卓系统是否完全启动，未完全启动时设备本地sdcard没显示，则提示处理；正常显示后则启动截图
                if not devices_state:
                    s.screen_str.set('请连接设备后再截图！')
                else:
                    # 创建临时文件
                    devices_SN = s.more_devices_value.get()
                    make_state = screen_record.cd_screenshots(devices_SN)
                    if make_state == 'Non-Android Devices':
                        s.screen_str.set('检测到非安卓设备\n请使用安卓设备进行操作')
                    else:
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
        s.record_stop_button_disable.place(x=200, y=330)
        with open(record_state,'w') as fp:
            fp.write('Stop recording screen')
        with open(record_screen_state,'w') as fp:
            fp.write('Stop recording screen')

    def record_bind(s):
        def t_record():
            # 录屏运行
            global record_stop_flag
            s.record_stop_button_disable.place_forget()
            s.record_button_disable.place(x=20, y=330)
            s.record_stop_button.place(x=200, y=330)
            s.reset_button_disable.place(x=200, y=370)
            devices_state = public.device_connect()
            s.record_str.set('正在启动录屏（请稍候）...')
            if not devices_state:
                s.record_str.set('请连接设备后再录屏！')
                # 按钮复原
                s.record_button_disable.place_forget()
                s.record_stop_button_disable.place(x=200, y=330)
                s.reset_button_disable.place_forget()
            else:
                # s.record_str.set('正在启动录屏（自动获取权限）...')

                # 记录录屏模式
                s.record_model_selected = s.record_model_str.get()
                print('录屏模式：' + str(s.record_model_selected))
                with open(record_model_log,'w') as fp:
                    fp.write(str(s.record_model_selected))

                # 获取录屏时间
                s.record_time_get = s.record_time.get()
                s.record_time_re = re.findall('(.*?)秒',s.record_time_get)
                s.record_time_selected = ''.join(s.record_time_re)
                # with open(record_time_txt,'w') as fp:
                #     fp.write(s.record_time_selected)

                # # 记录当前程序位置
                # now_path = os.getcwd()
                # print(now_path)
                # with open(exe_path,'w') as fp:
                #     fp.write(now_path)

                # # 切换到内置adb-tools路径，使录屏命令生效
                # os.chdir(adb_path)
                # # 响应内置ADB（防止切换到内置ADB时导致失效）
                # public.execute_cmd('adb start-server')

                # # 确保切换内置ADB并连接上设备后再执行停止机制
                # while True:
                #     devices_states = devices_state
                #     if devices_states:
                #         record_stop_flag = True
                #         break

                with open(record_stop_config, 'w') as fp:
                    fp.write('0')
                # 获取录屏名称
                s.record_name = s.record_entry.get()
                # with open(record_name,'w') as fp:
                #     fp.write(s.record_name)
                devices_SN = s.more_devices_value.get()
                screen_record.record(s.record_name,s.record_time_selected,str(s.record_model_selected),devices_SN)

        def record_time():
            # 显示录屏状态
            devices_state = public.device_connect()
            if not devices_state:
                pass
            else:
                with open(record_state, 'w') as fp:
                    fp.write('')
                # record_end_finally = screen_record.record_time(s.record_str)
                screen_record.record_time(s.record_str)
                record_model_get = open(record_model_log, 'r').read()
                record_state_finally = open(record_screen_state,'r').read()
                if record_model_get == '0':
                    if record_state_finally == 'Non-Android Devices':
                        pass
                    else:
                        s.record_str.set('正在保存录屏文件，请稍等...')
                        # s.record_name = open(record_name,'r').read()
                        s.record_name = s.record_entry.get()
                        devices_SN = s.more_devices_value.get()
                        screen_record.record_pull(s.record_name, record_model_get,devices_SN)
                        time.sleep(3)  # 延迟3S同步状态
                        # s.record_str.set('注意：录屏时间仅供参考，具体查看文件时长\n录屏文件保存成功！录屏时间为：' + record_end_finally)
                        s.record_str.set('录屏文件保存成功！\n打开录屏文件夹即可查看哦~')
                elif record_model_get == '1':
                    # # 返回原始地址，防止与本地ADB服务发生冲突导致无法使用
                    # original_path = open(exe_path, 'r').read()
                    # os.chdir(original_path)
                    #
                    # # 关闭ADB服务，以免影响本地ADB服务的开启
                    # public.execute_cmd('adb kill-server')

                    if record_state_finally == 'Non-Android Devices':
                        pass
                    else:
                        # 连续模式计数
                        r = int(open(record_count, 'r').read())
                        r += 1
                        with open(record_count, 'w') as fp:
                            fp.write(str(r))
                        s.record_str.set('正在保存连续模式录屏文件，请稍等...')
                        s.record_name = s.record_entry.get()
                        devices_SN = s.more_devices_value.get()
                        screen_record.record_pull(s.record_name,record_model_get,devices_SN)
                        time.sleep(3)  # 延迟3S同步状态
                        s.record_str.set('连续模式已结束！（录屏文件已保存）')
                s.record_button_disable.place_forget()
                s.record_stop_button_disable.place(x=200, y=330)
                s.reset_button_disable.place_forget()

        def record_stop():
            # 录屏停止机制
            global record_stop_flag
            record_stop_flag = False
            with open(record_screen_state,'w') as fp:
                fp.write('')
            with open(record_stop_config,'w') as fp:
                fp.write('')
            while True:
                record_device = public.device_connect()
                record_stop_state = open(record_screen_state,'r').read()
                record_stop_ini = open(record_stop_config,'r').read()
                if record_stop_state == 'Stop recording screen' and record_stop_ini == '0':
                    # os.popen('taskkill /F /IM %s ' % 'adb.exe /T', 'r')
                    # os.popen('taskkill /F /IM %s ' % 'record_main.exe /T', 'r')
                    try:
                        public.stop_thread(t_record)
                        public.stop_thread(record_time)
                    except ValueError:
                        pass
                    s.record_button_disable.place_forget()
                    s.record_stop_button_disable.place(x=200, y=330)
                    s.reset_button_disable.place_forget()
                    s.record_str.set('录屏已被中断！！！')
                    break
                elif record_stop_state == 'Stop recording screen' and record_stop_ini == '1':
                    # os.popen('taskkill /F /IM %s ' % 'record_main.exe /T', 'r')
                    # 通过关闭并重启ADB达到录屏命令的自动断开，以便自动生成录屏文件
                    print('正在断开并重启ADB服务...')
                    devices_SN = s.more_devices_value.get()
                    # 关闭ADB服务
                    public.execute_cmd('adb -s ' + devices_SN + ' kill-server')
                    # 重启ADB服务
                    public.execute_cmd('adb -s ' + devices_SN + ' start-server')
                    print('ADB服务重启成功！！！')
                    try:
                        # 连续模式停止
                        public.stop_thread(t_record)
                        print('主动中断连续模式！！！')
                    except ValueError:
                        print('手动模式无需强制中断线程---')
                        pass
                    # 等待文件保存完毕或ADB服务完全启动再复原按钮
                    time.sleep(7)
                    s.record_button_disable.place_forget()
                    s.record_stop_button_disable.place(x=200, y=330)
                    s.reset_button_disable.place_forget()
                    break
                elif not record_device and record_stop_ini == '0':
                    # 未录屏前断开设备
                    # os.popen('taskkill /F /IM %s ' % 'record_main.exe /T', 'r')
                    s.record_str.set('设备突然中断连接，录屏结束！')
                    s.record_button_disable.place_forget()
                    s.record_stop_button_disable.place(x=200, y=330)
                    s.reset_button_disable.place_forget()
                    break
                elif record_stop_state == 'Non-Android Devices':
                    print('检测到非安卓设备，无法正常录屏')
                    s.record_str.set('检测到非安卓设备\n请使用安卓设备进行操作')
                    s.record_button_disable.place_forget()
                    s.record_stop_button_disable.place(x=200, y=330)
                    s.reset_button_disable.place_forget()
                    break

        t_record = threading.Thread(target=t_record)
        t_record.setDaemon(True)
        t_record.start()

        record_time = threading.Thread(target=record_time)
        record_time.setDaemon(True)
        record_time.start()

        record_stop = threading.Thread(target=record_stop)
        record_stop.setDaemon(True)
        record_stop.start()

    def open_record_bind(s):
        def open_record():
            s.open_record_button_disable.place(x=20,y=370)
            screen_record.open_screenrecords()
            s.open_record_button_disable.place_forget()

        open_record = threading.Thread(target=open_record)
        open_record.setDaemon(True)
        open_record.start()

    def reset_bind(s):
        def t_reset():
            reset_message = """
            真的确定要一键重置 截图录屏，重置部分包括如下：
            1.将会清空所有的截图录屏保存文件夹
            2.将会清空所有相关截图录屏的缓存文件
            3.将会重置截图录屏的文件名计数（重置为零）
            """
            if tkinter.messagebox.askyesno(title='重置警告',message=reset_message):
                screen_record.reset_screenrecord()
                tkinter.messagebox.showinfo(title='完成',message='一键重置完成！！！')

        t_reset = threading.Thread(target=t_reset)
        t_reset.setDaemon(True)
        t_reset.start()

    def reset_disable_bind(s):
        tkinter.messagebox.showwarning(title='录屏警告',message='正在进行录屏，无法重置！！！')

    def linux_button_bind(s):
        def t_linux_button():
            def check_only_read():
                devices_SN = s.more_devices_value.get()
                check_only_read = public.execute_cmd('adb -s ' + devices_SN + ' shell ls -lh /data/.overlay')
                only_read = ' '.join(check_only_read.split()).split(':')[-1]
                return only_read

            while True:
                # linux_frame_exists = s.linux_frame1.winfo_exists()
                devices_finally = public.device_connect()
                s.init_text = s.init_str.get()
                only_read = check_only_read()
                if not devices_linux_flag or not devices_finally or only_read.strip() == 'No such file or directory':
                    s.linux_all_button_close()
                elif devices_linux_flag and devices_finally and only_read.strip() != 'No such file or directory':
                    s.linux_all_button_open()
                elif only_read.strip() == 'ls requires an argument':
                    error_content = '检测初始化只读权限异常错误，解决方案如下：' \
                                    '1.重新拔插设备后点击重新检测' \
                                    '2.重启软件后再重新检测初始化' \
                                    'PS：建议按照以上方案进行操作，以免功能无法正常使用！'
                    tkinter.messagebox.showerror(title='初始化错误',message=error_content)
                    break
                time.sleep(1)

        t_linux_button = threading.Thread(target=t_linux_button)
        t_linux_button.setDaemon(True)
        t_linux_button.start()

    def linux_screen_bind(s):
        def t_screen():
            # 初始化截图页面的状态
            with open(screen_page, 'w') as fp:
                fp.write('')
            linux_screen = linux_main.Linux_Screen()
            device_SN = s.more_devices_value.get()
            linux_screen.screen_form(s.init_str,s.linux_screen_Button,s.linux_screen_Button_disable,device_SN)

        def t_screen_close():
            # 监听截图页面的关闭状态
            with open(screen_page, 'w') as fp:
                fp.write('')
            while True:
                # 通过没有连接设备判断可优化按钮闪现情况
                devices_connect = public.device_connect()
                screen_page_state = open(screen_page,'r').read()
                if not devices_connect:
                    break
                else:
                    if screen_page_state == '0':
                        s.linux_screen_Button_disable.place_forget()
                        s.linux_screen_Button.place(x=20, y=190)
                        break

        t_screen = threading.Thread(target=t_screen)
        t_screen.setDaemon(True)
        t_screen.start()

        t_screen_close = threading.Thread(target=t_screen_close)
        t_screen_close.setDaemon(True)
        t_screen_close.start()

    def linux_developer_mode_close_bind(s):
        def t_developer_mode_close():
            # 关闭开发者模式
            linux_developer_mode_content = '你确定要关闭开发者选项并访问设备本地盘吗？\n\n点击“确定”则访问设备本地盘且无法使用ADB命令\n点击“取消”则不能访问设备本地盘'
            if tkinter.messagebox.askokcancel(title='',message=linux_developer_mode_content):
                s.init_str.set('正在关闭开发者模式并重启设备中...')
                s.linux_developer_mode_Button_close.place_forget()
                s.linux_developer_mode_Button_close_disable.place(x=200,y=190)
                device_SN = s.more_devices_value.get()
                public.execute_cmd('adb -s ' + device_SN + ' shell rm -rf /data/.adb_config')
                public.execute_cmd('adb -s ' + device_SN + ' shell reboot')
                time.sleep(18)
                s.init_str.set('现在可以访问设备本地盘了\nADB命令不可用')
            else:
                pass

        t_developer_mode_close = threading.Thread(target=t_developer_mode_close)
        t_developer_mode_close.setDaemon(True)
        t_developer_mode_close.start()

    def linux_install_bind(s):
        def t_install():
            # 初始化安装页面的状态
            with open(install_page, 'w') as fp:
                fp.write('')
            linux_install = linux_main.Linux_Install()
            device_SN = s.more_devices_value.get()
            linux_install.install_form(s.init_str,s.linux_install,s.linux_install_disable,device_SN)

        def t_install_close():
            # 监听安装页面的关闭状态
            with open(install_page, 'w') as fp:
                fp.write('')
            while True:
                devices_connect = public.device_connect()
                install_page_state = open(install_page,'r').read()
                if not devices_connect:
                    break
                else:
                    if install_page_state == '0':
                        s.linux_install_disable.place_forget()
                        s.linux_install.place(x=20, y=230)
                        break

        t_install = threading.Thread(target=t_install)
        t_install.setDaemon(True)
        t_install.start()

        t_install_close = threading.Thread(target=t_install_close)
        t_install_close.setDaemon(True)
        t_install_close.start()

    def linux_camera_bind(s):
        def t_camera():
            # 初始化取图页面的状态
            with open(camera_page, 'w') as fp:
                fp.write('')
            linux_camera = linux_main.Linux_Camera()
            device_SN = s.more_devices_value.get()
            linux_camera.camera_form(s.init_str,s.linux_camera,s.linux_camera_disable,device_SN)

        def t_camera_close():
            # 监听取图页面的关闭状态
            with open(camera_page, 'w') as fp:
                fp.write('')
            while True:
                devices_connect = public.device_connect()
                install_page_state = open(camera_page, 'r').read()
                if not devices_connect:
                    break
                else:
                    if install_page_state == '0':
                        s.linux_camera_disable.place_forget()
                        s.linux_camera.place(x=20, y=270)
                        break

        t_camera = threading.Thread(target=t_camera)
        t_camera.setDaemon(True)
        t_camera.start()

        t_camera_close = threading.Thread(target=t_camera_close)
        t_camera_close.setDaemon(True)
        t_camera_close.start()

    def uninstall_bind(s):
        def t_uninstall():
            global uninstall_flag
            # 卸载APK流程
            s.uninstall_button_disable.place(x=200,y=80)
            s.uninstall_str.set('正在卸载APK中...')
            # 卸载标记
            uninstall_flag = False
            s.check_package_name_bind(uninstall_flag)
            s.uninstall_button_disable.place_forget()

        t_uninstall = threading.Thread(target=t_uninstall)
        t_uninstall.setDaemon(True)
        t_uninstall.start()

    def check_package_name_bind(s,uninstall_flag):
        def t_check_package_name():
            global uninstall_flag
            # 检测当前包名
            s.check_package_name_button_disable.place(x=20,y=80)
            devices_state = public.device_connect()
            if not devices_state:
                s.uninstall_str.set('请连接设备后再重新检测')
            else:
                try:
                    s.uninstall_str.set('正在检测当前包名...')
                    device_SN = s.more_devices_value.get()
                    package_name = public.found_packages(device_SN)
                    print(package_name)
                    s.uninstall_str.set('已检测到当前包名\n' + package_name)
                    # 增加此项可提供包名的复制粘贴
                    with open(apk_aapt_log,'w') as fp:
                        fp.write(package_name)

                    if not uninstall_flag:
                        s.uninstall_str.set('检测到' + package_name + '\n正在卸载中...')
                        public.execute_cmd('adb uninstall ' + package_name)
                        uninstall_flag = True
                        s.uninstall_str.set('APK已卸载成功！')
                    else:
                        pass
                except (IndexError,TypeError):
                    s.uninstall_str.set('检测到非安卓设备\n请使用安卓设备进行操作')

            s.check_package_name_button_disable.place_forget()

        t_check_package_name = threading.Thread(target=t_check_package_name)
        t_check_package_name.setDaemon(True)
        t_check_package_name.start()

    def write_number_bind(s):
        def t_write_number():
            # 初始化写号工具页面的状态
            with open(write_number_page, 'w') as fp:
                fp.write('')
            linux_write_number = linux_main.Linux_WriteNumber()
            device_SN = s.more_devices_value.get()
            linux_write_number.write_number_form(s.init_str,s.write_number,s.write_number_disable,device_SN)

        def t_write_number_close():
            # 监听写号工具页面的关闭状态
            with open(write_number_page, 'w') as fp:
                fp.write('')
            while True:
                devices_connect = public.device_connect()
                write_number_page_state = open(write_number_page, 'r').read()
                if not devices_connect:
                    break
                else:
                    if write_number_page_state == '0':
                        s.write_number_disable.place_forget()
                        s.write_number.place(x=200, y=230)
                        break

        t_write_number = threading.Thread(target=t_write_number)
        t_write_number.setDaemon(True)
        t_write_number.start()

        t_write_number_close = threading.Thread(target=t_write_number_close)
        t_write_number_close.setDaemon(True)
        t_write_number_close.start()

    def uuid_main_bind(s):
        def t_uuid_main():
            # 手动获取UUID
            global uuid_run_flag
            # 恢复标识
            uuid_run_flag = True
            s.uuid_get_bind()
            return uuid_run_flag

        t_uuid_main = threading.Thread(target=t_uuid_main)
        t_uuid_main.setDaemon(True)
        t_uuid_main.start()

    def uuid_get_bind(s):
        def t_uuid_get():
            global uuid_reboot_flag
            global uuid_run_flag

            # 重新获取UUID
            s.uuid_get_disable.place(x=20,y=360)
            s.uuid_paste_disable.place(x=200, y=360)
            devices_state = public.device_connect()
            s.uuid_str.set('正在获取设备UUID中...')
            if not devices_state:
                s.uuid_str.set('请连接设备后再重新获取UUID')
            else:
                # 直接获取UUID
                devices_sn = s.more_devices_value.get()
                uuid_get_result = public.execute_cmd('adb -s ' + devices_sn + ' shell ls -lh /data/UUID.ini')
                uuid_get_result_finally = ' '.join(uuid_get_result.split()).split(':')[-1]
                if uuid_get_result_finally.strip() == 'No such file or directory':
                    uuid_result = public.execute_cmd('adb -s ' + devices_sn + ' shell cat /data/UUID.ini').strip()
                    s.uuid_str.set('已获取到该设备的UUID为\n' + uuid_result)
                else:
                    uuid = public.execute_cmd('adb -s ' + devices_sn + ' shell ag_os')
                    uuid_re = re.findall('uuid:(.*?)\\n',uuid)
                    uuid_result = ''.join(uuid_re).strip()
                    # 写入UUID后上传到设备中进行读取
                    with open(uuid_path,'w') as fp:
                        fp.write(uuid_result)
                    public.execute_cmd('adb -s ' + devices_sn+ ' push ' + uuid_path + ' /data/UUID.ini')
                    s.uuid_str.set('已获取到该设备的UUID为\n' + uuid_result)

            s.uuid_get_disable.place_forget()
            s.uuid_paste_disable.place_forget()

        t_uuid_get = threading.Thread(target=t_uuid_get)
        t_uuid_get.setDaemon(True)
        t_uuid_get.start()

    def uuid_paste_bind(s):
        def t_uuid_paste():
            # 一键复制UUID
            s.uuid_paste_disable.place(x=200,y=360)
            device_SN = s.more_devices_value.get()
            uuid_get_result = public.execute_cmd('adb -s ' + device_SN + ' shell ls -lh /data/UUID.ini')
            uuid_get_result_finally = ' '.join(uuid_get_result.split()).split(':')[-1]
            # agOsUUID_result = public.execute_cmd('adb -s ' + device_SN + ' shell ls -lh /data/agOsUUID.txt')
            # agOsUUID_result_finally = ' '.join(agOsUUID_result.split()).split(':')[-1]
            # and agOsUUID_result_finally.strip() == 'No such file or directory':
            if uuid_get_result_finally.strip() == 'No such file or directory':
                s.uuid_str.set('无法复制粘贴UUID\n请点击下方“重新获取UUID”获取UUID吧！')
            else:
                uuid_result = public.execute_cmd('adb -s ' + device_SN + ' shell cat /data/UUID.ini').strip()
                public.pyperclip_copy_paste(uuid_result)
            #     # 复制UUID到剪贴板
            #     devices_uuid = public.execute_cmd('adb -s ' + device_SN + ' shell cat /data/UUID.ini')
            #     devices_uuid_finally = ' '.join(devices_uuid.strip().split()).split(':')[-1]
            #     if devices_uuid_finally.strip() == 'No such file or directory':
            #         uuid_result = public.execute_cmd('adb -s ' + device_SN + ' shell cat /data/agOsUUID.txt').strip()
            #         pyperclip.copy(uuid_result)
            #         # 从剪贴板那粘贴
            #         pyperclip.paste()
            #         s.root.wm_attributes('-topmost', 1)
            #         tkinter.messagebox.showinfo('粘贴提醒', '已复制粘贴 ' + uuid_result + ' 到剪贴板\n可以Ctrl+V粘贴到任意地方啦~')
            #     else:
            #         pyperclip.copy(devices_uuid)
            #         # 从剪贴板那粘贴
            #         pyperclip.paste()
            #         s.root.wm_attributes('-topmost', 1)
            #         tkinter.messagebox.showinfo('粘贴提醒','已复制粘贴 ' + devices_uuid + ' 到剪贴板\n可以Ctrl+V粘贴到任意地方啦~')
            #     s.root.wm_attributes('-topmost', 0)
            s.uuid_paste_disable.place_forget()

        t_uuid_paste = threading.Thread(target=t_uuid_paste)
        t_uuid_paste.setDaemon(True)
        t_uuid_paste.start()

    def get_log_bind(s):
        def t_get_log():
            # 初始化一键获取日志页面的状态
            with open(get_log_page, 'w') as fp:
                fp.write('')
            linux_get_log = linux_main.Linux_Log()
            device_SN = s.more_devices_value.get()
            linux_get_log.log_form(s.init_str,s.get_log,s.get_log_disable,device_SN)

        def t_get_log_close():
            # 监听一键获取日志页面的关闭状态
            with open(get_log_page, 'w') as fp:
                fp.write('')
            while True:
                devices_connect = public.device_connect()
                get_log_page_state = open(get_log_page, 'r').read()
                if not devices_connect:
                    break
                else:
                    if get_log_page_state == '0':
                        s.get_log_disable.place_forget()
                        s.get_log.place(x=200, y=270)
                        break

        t_get_log = threading.Thread(target=t_get_log)
        t_get_log.setDaemon(True)
        t_get_log.start()

        t_get_log_close = threading.Thread(target=t_get_log_close)
        t_get_log_close.setDaemon(True)
        t_get_log_close.start()

    def open_apk_path_files(s,apk_path_install_flag):
        def t_open_apk_path():
            # 打开库文件代码
            s.apk_path_package_button_disable.place(x=320,y=160)
            s.apk_path_button_disable.place(x=320,y=285)
            s.apk_path_package_entry.config(state='disable')
            s.apk_path_entry.config(state='disable')
            apk_path_file = tkinter.filedialog.askopenfile(mode='r', filetypes=[('Apk Files', '*.apk')], title='选择apk安装文件')
            apk_path_file_string = str(apk_path_file)
            print('apk安装标识：' + str(apk_path_install_flag))
            if not apk_path_file:
                if apk_path_install_flag:
                    s.install_str.set('没有成功选择apk文件\n请重新选择apk文件')
                else:
                    s.uninstall_str.set('没有成功选择apk文件\n请重新选择apk文件')
            else:
                # replace('/','\\')替换路径符号，提高最准确无误的文件绝对路径
                print('apk路径获取源数据：' + apk_path_file_string)
                # apk_path_file_finally = eval(apk_path_file_string.split()[1].split('=')[1]).replace('/','\\')
                # 更换为 re正则表达式 判断
                apk_path_file_finally = ''.join(re.findall('name=\'(.*?)\'\s', apk_path_file_string)).replace('/', '\\')
                if apk_path_install_flag:
                    s.apk_path_str.set(apk_path_file_finally)
                    print('获取地址：' + str(apk_path_file_finally))
                    with open(apk_path_log, 'w') as fp:
                        fp.write(apk_path_file_finally)
                else:
                    s.apk_path_package_str.set(apk_path_file_finally)
                    print('获取地址：' + str(apk_path_file_finally))
                    with open(apk_path_package_log,'w') as fp:
                        fp.write(apk_path_file_finally)
            s.apk_path_package_entry.config(state='normal')
            s.apk_path_entry.config(state='normal')
            s.apk_path_button_disable.place_forget()
            s.apk_path_package_button_disable.place_forget()

        t_open_apk_path = threading.Thread(target=t_open_apk_path)
        t_open_apk_path.setDaemon(True)
        t_open_apk_path.start()

    def apk_package_bind(s):
        def t_apk_package():
            # 根据apk文件获取包名
            s.apk_package_button_disable.place(x=20,y=200)
            s.uninstall_str.set('正在获取apk文件包名中...')
            s.apk_path_package_get = s.apk_path_package_str.get()
            print(s.apk_path_package_get)
            apk_package_cmd = 'aapt dump badging ' + '"' + s.apk_path_package_get + '"' + ' > ' + apk_aapt_log
            apk_package_result = public.execute_cmd(apk_package_cmd)
            try:
                apk_package_result_error = apk_package_result.split(' ')[1].split('\n')[0].strip()
                if apk_package_result_error == '不是内部或外部命令，也不是可运行的程序':
                    s.uninstall_str.set('检测到ADB包中缺少aapt\n正在更新ADB本地包...')
                    s.adb_str.set('正在更新ADB...')
                    with open(adb_upgrade_flag,'w') as fp:
                        fp.write('ADB upgrade')
                    public.upgrade_adb()
                    with open(adb_upgrade_flag,'w') as fp:
                        fp.write('')
                    s.uninstall_str.set('ADB本地包更新成功！')
                    s.adb_str.set('本地ADB已开启！')
            except IndexError:
                pass
            apk_package_result_log = open(apk_aapt_log,'r',encoding='utf-8').read()
            apk_package_result_re = re.findall('package: name=\'(.*?)\'\s', apk_package_result_log)
            apk_package_result_finally = ''.join(apk_package_result_re)
            if apk_package_result_finally == '':
                s.uninstall_str.set('你选择的apk路径不存在或不是apk文件\n请重新选择正确无误的apk路径再试吧')
            else:
                with open(apk_aapt_log,'w') as fp:
                    fp.write(apk_package_result_finally)
                print('获取的包名为：' + apk_package_result_finally)
                s.uninstall_str.set('已获取到包名为：\n' + apk_package_result_finally)
            s.apk_package_button_disable.place_forget()

        t_apk_package = threading.Thread(target=t_apk_package)
        t_apk_package.setDaemon(True)
        t_apk_package.start()

    def apk_package_copy_bind(s):
        def t_apk_package_copy():
            s.apk_package_copy_button_disable.place(x=200,y=200)
            apk_package_name = open(apk_aapt_log,'r').read()
            if apk_package_name == '':
                tkinter.messagebox.showinfo('空包名','你还没有获取任何包名哦~\n现在暂时无法复制粘贴！')
            else:
                public.pyperclip_copy_paste(apk_package_name)
            s.apk_package_copy_button_disable.place_forget()

        t_apk_package_copy = threading.Thread(target=t_apk_package_copy)
        t_apk_package_copy.setDaemon(True)
        t_apk_package_copy.start()

    def apk_path_insatll_bind(s):
        # 选择apk文件逻辑
        global apk_path_install_flag
        apk_path_install_flag = True
        s.open_apk_path_files(apk_path_install_flag)
        apk_path_install_flag = False

    def apk_install_bind(s):
        def t_apk_install():
            # 安装apk逻辑
            global apk_install_flag
            s.apk_button_disable.place(x=20,y=325)
            apk_install_flag = True
            devices_state = public.device_connect()
            if not devices_state:
                s.install_str.set('检测到没有连接到设备\n请连接设备后再进行安装')
            else:
                devices = s.more_devices_value.get()
                device_type = public.device_type_android(devices)
                if device_type.strip() == 'Android':
                    s.install_str.set('正在安装apk中...')
                    apk_path = s.apk_path_str.get()
                    apk_install_options = s.apk_install_mode_value.get()
                    if apk_install_options == '默认':
                        apk_install_model = ''
                    elif apk_install_options == '-d选项 无视版本高低安装':
                        apk_install_model = '-d '
                    apk_install_cmd = 'adb -s ' + devices + ' install -r ' + apk_install_model + '"' + apk_path + '"'
                    print('安装命令显示：' + apk_install_cmd)
                    install_result = public.execute_cmd(apk_install_cmd)
                    print('安装结果：' + install_result)
                    try:
                        install_error = install_result.split(' ')[1]
                        if install_error.strip() == 'failed':
                            s.install_str.set('apk安装失败！\n请点击下方“查看安装信息”分析原因吧~')
                            with open(apk_install_log,'w') as fp:
                                fp.write(install_result)
                                apk_install_flag = False
                                s.apk_button_disable.place_forget()
                                # return 直接从此处跳出，不执行下方代码
                                return
                    except IndexError:
                        pass

                    with open(apk_install_log,'w') as fp:
                        fp.write(install_result)
                    print('安装结果：' + install_result)
                    s.install_str.set('apk安装成功！')
                else:
                    s.install_str.set('您所连接的设备为非Android设备\n无法使用安装apk功能')
            apk_install_flag = False
            s.apk_button_disable.place_forget()

        t_apk_install = threading.Thread(target=t_apk_install)
        t_apk_install.setDaemon(True)
        t_apk_install.start()

    def apk_install_info_bind(s):
        def t_apk_install_info():
            # 查看apk安装信息
            s.apk_install_info_button_disable.place(x=200,y=325)
            if not os.path.exists(apk_install_log):
                with open(apk_install_log,'w') as fp:
                    fp.write('')
            win32api.ShellExecute(0, 'open',apk_install_log, '', '', 1)
            s.apk_install_info_button_disable.place_forget()

        t_apk_install_info = threading.Thread(target=t_apk_install_info)
        t_apk_install_info.setDaemon(True)
        t_apk_install_info.start()

    def update_status(s):
        def public_mac_ip(devices):
            # 获取设备MAC（物理）地址
            mac_result = public.wifi_mac_result(devices)
            if mac_result.strip() == '':
                s.devices_mac_str.set('设备没有连接网络，暂无法查询')
                s.devices_mac.unbind('<Button-1>')
            else:
                s.devices_mac_str.set('设备MAC地址：' + mac_result.strip())
                s.devices_mac.bind('<Button-1>', lambda x: public.pyperclip_copy_paste(mac_result))
            # 获取设备ip地址
            ip_result = public.devices_ip_result(devices)
            if ip_result.strip() == '':
                s.devices_ip_str.set('设备没有连接网络，暂无法查询')
                s.devices_ip.unbind('<Button-1>')
            else:
                s.devices_ip_str.set('设备ip地址：' + ip_result.strip())
                s.devices_ip.bind('<Button-1>', lambda x: public.pyperclip_copy_paste(ip_result))

        def linux_sn_number(devices):
            # Linux SN号 获取方式
            devices_sn = public.execute_cmd('adb -s ' + devices + ' shell cat /data/linux_sn.ini')
            devices_sn_finally = ' '.join(devices_sn.strip().split()).split(':')[-1]
            if devices_sn_finally.strip() == 'No such file or directory':
                # 从设备系统日志中过滤出SN
                sn = public.execute_cmd('adb -s ' + devices + ' shell grep "sn" /data/syslog.log')
                if sn.strip() == '':
                    s.devices_sn_str.set('首次查询需要进入“设置-关于”')
                    s.devices_sn.unbind('<Button-1>')
                else:
                    sn_re = re.findall('"sn":(.*?)}', sn)
                    sn_result = eval(sn_re[0])
                    with open(linux_sn_path,'w') as fp:
                        fp.write(sn_result)
                    # 上传到设备里面方便保存读取
                    public.execute_cmd('adb -s ' + devices + ' push ' + linux_sn_path + ' /data/linux_sn.ini')
                    s.devices_sn_str.set('设备序列号：' + sn_result.strip())
                    s.devices_sn.bind('<Button-1>', lambda x: public.pyperclip_copy_paste(sn_result))
            else:
                sn_result = public.execute_cmd('adb -s ' + devices + ' shell cat /data/linux_sn.ini')
                s.devices_sn_str.set('设备序列号：' + sn_result.strip())
                s.devices_sn.bind('<Button-1>', lambda x: public.pyperclip_copy_paste(sn_result))

        def t_update_status():
            global software_version_flag
            # 实时检测设备所有信息
            devices = s.more_devices_value.get()

            if not public.device_connect():
                pass
            else:
                # 更新设备类型
                if s.devices_type_str.get() == 'Android（安卓）':
                    s.devices_mode_str.set('设备类型：Android（安卓）')
                    # 更新设备序列号（安卓）
                    # 更换更加准确查询序列号的命令
                    sn_result = public.execute_cmd('adb -s ' + devices + ' shell getprop gsm.serial')
                    if sn_result.strip() == '':
                        sn_result = public.execute_cmd('adb -s ' + devices + ' shell getprop ro.serialno')
                    if len(sn_result) > 19:
                        s.devices_sn_str.set('序列号:' + sn_result.strip())
                    else:
                        s.devices_sn_str.set('设备序列号:' + sn_result.strip())
                    s.devices_sn.bind('<Button-1>', lambda x: public.pyperclip_copy_paste(sn_result))
                    public_mac_ip(devices)
                    # 获取安卓版本号
                    try:
                        android_version = public.execute_cmd('adb -s ' + devices + ' shell getprop ro.build.version.release')
                        s.android_version_str.set('安卓版本号：Android ' + android_version.strip())
                    except TypeError:
                        pass
                    # 获取安卓的应用版本号和固件版本号
                    try:
                        software_version = public.android_software_version_result(devices)
                        s.software_version_str.set('应用版本号：' + software_version)
                    except TypeError:
                        pass
                    firmware_version = public.android_firmware_version_result(devices)
                    try:
                        s.firmware_version_str.set('固件版本号：' + firmware_version)
                    except TypeError:
                        pass
                elif s.devices_type_str.get() == 'Linux':
                    s.devices_mode_str.set('设备类型：Linux')
                    # 更换设备序列号提示
                    # s.devices_sn_str.set('设备序列号：' + device_SN.strip())
                    # s.devices_sn.bind('<Button-1>', lambda x: public.pyperclip_copy_paste(device_SN.strip()))
                    linux_sn_number(devices)
                    public_mac_ip(devices)
                    # 更换安卓系统版本 --》 Linux设备UUID
                    # uuid_get_result = public.execute_cmd('adb -s ' + device_SN + ' shell ls -lh /data/UUID.ini')
                    # uuid_get_result_finally = ' '.join(uuid_get_result.split()).split(':')[-1]
                    # agOsUUID_result = public.execute_cmd('adb -s ' + device_SN + ' shell ls -lh /data/agOsUUID.txt')
                    # agOsUUID_result_finally = ' '.join(agOsUUID_result.split()).split(':')[-1]
                    # 隐藏安卓的应用版本号label
                    s.software_version.place_forget()
                    # if uuid_get_result_finally.strip() == 'No such file or directory' and \
                    #         agOsUUID_result_finally.strip() == 'No such file or directory':
                    #     s.android_version_str.set('该设备需要重新获取UUID')
                    # else:
                    #     # 复制UUID到剪贴板
                    #     devices_uuid = public.execute_cmd('adb -s ' + device_SN + ' shell cat /data/UUID.ini')
                    #     devices_uuid_finally = ' '.join(devices_uuid.strip().split()).split(':')[-1]
                    #     if devices_uuid_finally.strip() == 'No such file or directory':
                    #         uuid_result = public.execute_cmd(
                    #             'adb -s ' + device_SN + ' shell cat /data/agOsUUID.txt').strip()
                    #         s.android_version.bind('<Button-1>', lambda x: public.pyperclip_copy_paste(uuid_result))
                    #         s.android_version_str.set('设备UUID：\n' + uuid_result)
                    #     else:
                    #         s.android_version.bind('<Button-1>', lambda x: public.pyperclip_copy_paste(devices_uuid))
                    #         s.android_version_str.set('设备UUID：\n' + devices_uuid)
                    uuid = public.execute_cmd('adb -s ' + devices + ' shell ag_os')
                    uuid_re = re.findall('uuid:(.*?)\\n', uuid)
                    uuid_result = ''.join(uuid_re).strip()
                    s.android_version_str.set('设备UUID：\n' + uuid_result)
                    s.android_version.bind('<Button-1>', lambda x: public.pyperclip_copy_paste(uuid_result))
                    # 显示安卓固件版本号 --》 固件版本号
                    # ota_version = public.execute_cmd('adb -s ' + device_SN + ' shell cat /data/ota_version')
                    # ota_version_finally = ' '.join(ota_version.split()).split(':')[-1]
                    # if ota_version_finally.strip() == 'No such file or directory':
                    #     s.firmware_version_str.set('该设备不支持查询固件版本')
                    # else:
                    #     s.firmware_version_str.set('固件版本：' + ota_version.strip())
                    version = public.execute_cmd('adb -s ' + devices + ' shell ag_os')
                    genie_re = re.findall('genie version:(.*?)\\n', version)
                    firmware_re = re.findall('firmware version:(.*?)\\n', version)
                    genie_version = ''.join(genie_re).strip()
                    firmware_version = ''.join(firmware_re).strip()
                    s.firmware_version_str.set('软件版本：' + genie_version.strip() + '\n'
                                               + '固件版本：' + firmware_version.strip())

        t_update_status = threading.Thread(target=t_update_status)
        t_update_status.setDaemon(True)
        t_update_status.start()

    def flow_bind(s):
        def t_flow():
            global first_button_flag,tkinter_messagebox_flag
            # 初始化查询应用流量值页面的状态
            with open(public.flow_page(), 'w') as fp:
                fp.write('')
            devices_state = public.device_connect()
            if not devices_state:
                pass
            else:
                flow = customize_main.Flow_Screen()
                device_SN = s.more_devices_value.get()
                tkinter_messagebox_flag = False
                flow.flow_form(s.flow_button, s.flow_button_disable, device_SN,devices_type_log)

        def t_flow_close():
            global first_button_flag,tkinter_messagebox_flag
            # 监听查询应用流量值页面的关闭状态
            with open(public.flow_page(), 'w') as fp:
                fp.write('')
            while True:
                flow_page_state = open(public.flow_page(), 'r').read()
                devices_state = public.device_connect()
                if not devices_state:
                    s.flow_button_disable.place(x=20, y=20)
                    if not tkinter_messagebox_flag:
                        content = '''
                        检测到使用本功能时没有连接设备
                        请连接设备后再使用本功能
                        '''
                        tkinter.messagebox.showerror(title='没有连接设备，启动功能失败',message=content)
                        tkinter_messagebox_flag = True
                else:
                    if not first_button_flag:
                        s.flow_button_disable.place_forget()
                        first_button_flag = True
                    if flow_page_state == '0':
                        s.flow_button_disable.place_forget()
                        s.flow_button.place(x=20, y=20)
                        break

        t_flow = threading.Thread(target=t_flow)
        t_flow.setDaemon(True)
        t_flow.start()

        t_flow_close = threading.Thread(target=t_flow_close)
        t_flow_close.setDaemon(True)
        t_flow_close.start()