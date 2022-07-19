import re
import shutil
import signal
import sys
from pathlib import Path
import time
import tkinter,tkinter.ttk,tkinter.messagebox
import threading
import os
import public,getpass,pyperclip
import quickly,screen_record,linux_main
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
# 冲突软件列表
conflict_software_list = ['PhoenixSuit.exe']
username = getpass.getuser()
LOGO_path = public.resource_path(os.path.join('icon', 'android.ico'))
version_path = public.resource_path(os.path.join('version','version_history.txt'))
adb_path = public.resource_path(os.path.join('resources','adb-tools.zip'))
adb_version_path = public.resource_path(os.path.join('resources','Android Debug Bridge version.txt'))
uuid_path = public.resource_path(os.path.join('resources','UUID.ini'))
record_state = public.resource_path(os.path.join('temp','record_state.txt'))
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
# 临时保存UUID日志
syslog_log = make_dir + 'uuid.log'
# 实时保存设备序列号
devices_log = make_dir + 'devices.log'
# 启动前初始化
with open(adb_upgrade_flag,'w') as fp:
    fp.write('ADB is the latest version')
with open(conflict_software_path,'w') as fp:
    fp.write('')
# 统一修改版本号
version = 'V1.0.0.20'
version_code = 1002.0
# 统一修改frame的宽高
width = 367
height = 405
# 统一按钮宽度
width_button = 20
# 统一root窗口总宽高
main_width = 600
main_height = 450
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

        s.verion_menu = tkinter.Menubutton(s.root,text='版本历史')
        s.verion_menu1 = tkinter.Menubutton(s.root, text='版本历史')
        s.verion_menu1.config(state='disable')

        s.main_menu.bind('<Button-1>',lambda x:s.display_main_frame())
        s.verion_menu.bind('<Button-1>',lambda x:s.display_version_frame())
        s.screen_menu.bind('<Button-1>',lambda x:s.display_screenshot_frame())
        s.linux_menu.bind('<Button-1>',lambda x:s.display_linux_frame())
        s.install_menu.bind('<Button-1>',lambda x:s.display_install_frame())

        s.main_menu.place(x=0,y=0)
        s.screen_menu.place(x=60, y=0)
        s.install_menu.place(x=120,y=0)
        s.linux_menu.place(x=180,y=0)
        s.verion_menu.place(x=240,y=0)

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
        s.main_menu1.place(x=0, y=0)
        try:
            s.screen_frame1.place_forget()
            s.linux_frame1.place_forget()
            s.verion_frame_full.place_forget()
            s.install_frame1.place_forget()
        except AttributeError:
            print('所选窗口未启动 -警告信息Logs（可忽略）')
            pass

    def display_screenshot_frame(s):
        # 显示截图录屏窗口
        s.screen_frame()
        s.main_menu1.place_forget()
        s.linux_menu1.place_forget()
        s.install_menu1.place_forget()
        s.screen_menu1.place(x=60, y=0)
        s.verion_menu1.place_forget()
        try:
            s.quickly_frame1.place_forget()
            s.linux_frame1.place_forget()
            s.verion_frame_full.place_forget()
            s.install_frame1.place_forget()
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
        try:
            s.quickly_frame1.place_forget()
            s.screen_frame1.place_forget()
            s.verion_frame_full.place_forget()
            s.linux_frame1.place_forget()
        except AttributeError:
            print('所选窗口未启动 -警告信息Logs（可忽略）')
            pass

    def display_linux_frame(s):
        # 显示Linux模式窗口
        s.linux_menu1.place(x=180, y=0)
        s.linux_frame()
        s.screen_menu1.place_forget()
        s.main_menu1.place_forget()
        s.verion_menu1.place_forget()
        s.install_menu1.place_forget()
        try:
            s.quickly_frame1.place_forget()
            s.screen_frame1.place_forget()
            s.verion_frame_full.place_forget()
            s.install_frame1.place_forget()
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
        s.verion_menu1.place(x=240, y=0)
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
        content = '''* 说明：此处可以修改录屏后生成的文件名称(默认demo)\n生成的文件保存在桌面上的“ADB工具-录屏（DA）”里面\n录屏时请勿使用本地ADB服务，否则会中断录屏
                        '''
        s.record_readme_label = tkinter.Label(s.screen_frame1, text=content, fg='red', font=('宋体', 10))
        s.record_readme_label.place(x=20, y=250)

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

        # 检测包名按钮
        s.uninstall_button = tkinter.Button(s.install_frame1, text='一键卸载APK', width=width_button)
        s.uninstall_button.bind('<Button-1>', lambda x: s.uninstall_bind())
        s.uninstall_button_disable = tkinter.Button(s.install_frame1, text='正在卸载中...', width=width_button)
        s.uninstall_button_disable.config(state='disable')
        s.uninstall_button.place(x=200, y=80)

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
        uuid_remind_content1 = '点击“重新获取”会获取设备的UUID\n' \
                              '温馨提示：由于设备机制导致获取UUID时会存在失败的可能性\n' \
                              '因此获取设备UUID失败后请再重新获取（直到成功后就无需再获取了）'
        public.CreateToolTip(s.uuid_get,uuid_remind_content1)

        # UUID复制粘贴功能
        s.uuid_paste = tkinter.Button(s.linux_frame1, text='一键复制UUID', width=width_button)
        s.uuid_paste_disable = tkinter.Button(s.linux_frame1, text='正在复制中...', width=width_button)
        s.uuid_paste.bind('<Button-1>', lambda x: s.uuid_paste_bind())
        s.uuid_paste_disable.config(state='disable')
        s.uuid_paste.place(x=200, y=360)
        uuid_remind_content2 = '温馨提示：由于设备机制导致获取UUID时会存在失败的可能性\n' \
                               '因此获取设备UUID失败后请再重新获取（直到成功后就无需再获取了）'
        public.CreateToolTip(s.uuid_paste,uuid_remind_content2)

        # 开始默认禁用，根据情况开启
        s.linux_all_button_close()

        s.linux_frame1.place(y=20)

    # def conflict_frame_main(s,conflict_software_name):
    #     # 防冲突窗口
    #     s.conflict_frame1 = tkinter.Frame(s.root,width=main_width,height=250)
    #
    #     # 显示防冲突软件名称
    #     s.conflict_software_label = tkinter.Label(s.conflict_frame1,text='冲突软件名称：')
    #     s.conflict_software_label.place(x=20,y=20)
    #     print('冲突软件名称：' + conflict_software_name)
    #     s.conflict_software_name_label = tkinter.Label(s.conflict_frame1,text=conflict_software_name,fg='red')
    #     s.conflict_software_name_label.place(x=100,y=20)
    #
    #     # 防冲突字体显示
    #     s.conflict_software_title_label = tkinter.Label(s.conflict_frame1,text='防冲突功能',fg='red',font=('华文行楷',50))
    #     s.conflict_software_title_label.place(x=145,y=50)
    #
    #     # 防冲突注意事项显示
    #     s.conflict_software_content = '注意事项:\n' \
    #                                   '①检测到冲突软件 ' + conflict_software_name + ' 正在运行中...\n' \
    #                                   '②该冲突软件会和本工具产生严重冲突导致出现闪退问题\n' \
    #                                   '③当前解决方案为：\n' \
    #                                   '（1）关闭冲突软件或本工具，只运行其中之一\n' \
    #                                   '（2）进行冲突兼容，使用冲突软件的ADB服务，避免使用ADB服务冲突问题（推荐）\n' \
    #                                   '④本工具默认使用推荐方案，当然也提供强制关闭该冲突软件的按钮，但强烈推荐使用默认方案！'
    #     s.conflict_warnning_label = tkinter.Label(s.conflict_frame1,text=s.conflict_software_content)
    #     s.conflict_warnning_label.place(x=30,y=130)
    #
    #     s.conflict_frame1.place(x=0, y=0)
    #
    # def conflict_frame_main2(s,conflict_software_name):
    #     s.conflict_frame2 = tkinter.Frame(s.root, width=main_width,height=200)
        # # 某些软件是绿色免安装的，需要自行手动输入绝对路径
        # conflict_software_path_content = '请手动输入 ' + conflict_software_name + ' 的安装或存放路径：'
        # s.conflict_software_path_label = tkinter.Label(s.conflict_frame2,text=conflict_software_path_content,fg='red')
        # s.conflict_software_path_label.place(x=20,y=20)

        # # 提醒需要点击冲突兼容
        # remind_content = '输入路径后，请点击下方“冲突兼容”开始进行兼容；点击“取消”将会关闭本工具！'
        # s.conflict_remind_label = tkinter.Label(s.conflict_frame2, text=remind_content, fg='red')
        # s.conflict_remind_label.place(x=20, y=80)

        # # 冲突兼容按钮
        # s.conflict_software_button = tkinter.Button(s.conflict_frame2,text='冲突兼容',width=width_button)
        # s.conflict_software_button_disable = tkinter.Button(s.conflict_frame2,text='冲突兼容',width=width_button)
        # s.conflict_software_button_disable.config(state='disable')
        # s.conflict_software_button.bind('<Button-1>',lambda x:s.confict_software_bind())
        # s.conflict_software_button.place(x=20,y=110)
        #
        # # 冲突兼容取消按钮
        # s.conflict_software_cancel_button = tkinter.Button(s.conflict_frame2, text='取消', width=width_button)
        # s.conflict_software_cancel_button_disable = tkinter.Button(s.conflict_frame2, text='取消', width=width_button)
        # s.conflict_software_cancel_button_disable.config(state='disable')
        # s.conflict_software_cancel_button.place(x=400, y=110)

        # s.conflict_frame2.place(x=0,y=250)

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
        def t_devices():
            global adb_server_flag
            global conflict_model_flag
            s.devices_str.set('正在检测设备连接状态...')
            while True:
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
                                                    my_pid = os.getpid()
                                                    os.kill(my_pid,signal.SIGINT)
                    # 取消置顶
                    s.root.wm_attributes('-topmost', 0)

                    # # 首次检测冲突软件后ADB服务断开
                    # if not adb_server_flag:
                    #     print('发现冲突软件，ADB正在断开中...')
                    #     public.execute_cmd('adb kill-server')
                    #     adb_server_flag = True
                    # if not conflict_model_flag:
                    #     print('只显示一次防冲突窗口，不循环操作')
                    #     # 冲突软件锁定（显示防冲突处理窗口）
                    #     # 禁用当前所有模块入口
                    #     s.verion_menu.place_forget()
                    #     s.verion_menu1.place_forget()
                    #     s.screen_menu1.place_forget()
                    #     s.screen_menu.place_forget()
                    #     s.install_menu1.place_forget()
                    #     s.install_menu.place_forget()
                    #     s.linux_menu1.place_forget()
                    #     s.linux_menu.place_forget()
                    #     s.main_menu1.place_forget()
                    #     s.main_menu.place_forget()
                    #     # 禁用所有root控件
                    #     s.devices_state_label.place_forget()
                    #     s.devices_success.place_forget()
                    #     s.devices_fail.place_forget()
                    #
                    #     s.adb_state_label.place_forget()
                    #     s.adb_success.place_forget()
                    #
                    #     s.devices_type_label.place_forget()
                    #     s.devices_type_fail.place_forget()
                    #     s.devices_type_success.place_forget()
                    #
                    #     s.more_devices_label.place_forget()
                    #     s.more_devices_combobox.place_forget()
                    #
                    #     # 禁用当前所有窗口
                    #     try:
                    #         s.quickly_frame1.place_forget()
                    #         s.screen_frame1.place_forget()
                    #         s.linux_frame1.place_forget()
                    #         s.verion_frame_full.place_forget()
                    #         s.install_frame1.place_forget()
                    #     except AttributeError:
                    #         print('当前所有窗口已锁定 -警告信息Logs（可忽略）')
                    #         pass
                    #     # 显示防冲突窗口
                    #     s.conflict_frame_main(conflict_software_name)
                    #     s.conflict_frame_main2(conflict_software_name)
                    #
                    #     conflict_model_flag = True
                    # else:
                    #     pass
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
                        # print(adb_install_state)
                        # print(conflict_software_flag)
                        # print(conflict_model_flag)
                        # if not conflict_software_flag:
                            # if conflict_model_flag:
                            #     # 关闭防冲突窗口
                            #     s.conflict_frame1.place_forget()
                            #     s.conflict_frame2.place_forget()
                            #     print('只恢复一次窗口，不循环操作')
                            #     # 冲突软件关闭后防冲突功能解除，恢复当前所有控件和窗口
                            #     s.main_menu.place(x=0,y=0)
                            #     s.main_menu1.place(x=0,y=0)
                            #     s.screen_menu.place(x=60, y=0)
                            #     s.install_menu.place(x=120, y=0)
                            #     s.linux_menu.place(x=180, y=0)
                            #     s.verion_menu.place(x=240, y=0)
                            #
                            #     s.devices_type_label.place(x=270, y=425)
                            #     s.devices_state_label.place(x=370, y=0)
                            #
                            #     s.adb_success.place(x=110, y=425)
                            #     s.adb_state_label.place(x=0, y=425)
                            #
                            #     s.devices_type_label.place(x=270, y=425)
                            #
                            #     s.more_devices_label.place(x=310, y=20)
                            #     s.more_devices_combobox.place(x=380, y=80)
                            #     # 默认显示窗口
                            #     s.display_main_frame()
                            #
                            #     conflict_model_flag = False
                            # else:
                            #     if not conflict_model_flag:
                        devices_finally = public.device_connect()
                        # print('检测设备连接状态 === ' + str(devices_finally))
                        if not devices_finally:
                            s.devices_fail.place(x=470, y=0)
                            s.devices_type_fail.place(x=325,y=425)
                            s.devices_success.place_forget()
                            s.devices_type_success.place_forget()
                            # 为确保防冲突时关闭所有控件和提示，增加判断
                            # print('未连接到设备的提示判断 === ' + str(conflict_model_flag))
                            # if conflict_model_flag:
                            #     # 提示置为空
                            #     s.devices_null.set('')
                            #     s.devices_type_error.set('')
                            # elif not conflict_model_flag:
                            s.devices_null.set('未连接任何设备！')
                            s.devices_type_error.set('未连接任何设备！')
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
                                    s.devices_str.set(devices + ' 已连接')
                                    continue
                                elif len(devices_finally) > 1:
                                    s.devices_str.set('多部设备已连接')
                                    continue
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
        s.screen_str.set('正在截图中...')
        devices_SN = s.more_devices_value.get()
        screenshot_success = screen_record.main_screenshots(touch_name,devices_SN)
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
            if not devices_state:
                s.record_str.set('请连接设备后再录屏！')
                # 按钮复原
                s.record_button_disable.place_forget()
                s.record_stop_button_disable.place(x=200, y=330)
                s.reset_button_disable.place_forget()
            else:
                # s.record_str.set('正在启动录屏（自动获取权限）...')
                s.record_str.set('正在启动录屏（请稍候）...')

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
                if s.init_text == '该设备没有初始化\n请点击下方按钮进行设备初始化' or s.init_text == '此处显示初始化状态'\
                        or not devices_linux_flag or not devices_finally or only_read.strip() == 'No such file or directory':
                    s.linux_all_button_close()
                elif s.init_text == '该设备已初始化\n无需初始化，可正常使用下方功能' and devices_linux_flag and devices_finally\
                          and only_read.strip() != 'No such file or directory':
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
                # 初始化UUID
                with open(uuid_path, 'w') as fp:
                    fp.write('')
                with open(syslog_log, 'w') as fp:
                    fp.write('')
                device_SN = s.more_devices_value.get()
                # 获取UUID文件
                uuid_get_result = public.execute_cmd('adb -s ' + device_SN + ' shell ls -lh /data/UUID.ini')
                uuid_get_result_finally = ' '.join(uuid_get_result.split()).split(':')[-1]
                print(uuid_get_result_finally)
                if uuid_get_result_finally.strip() == 'No such file or directory':
                    if not uuid_run_flag:
                        s.uuid_str.set('该设备UUID没有获取过\n请点击下方“重新获取”进行UUID获取吧！')
                    else:
                        # 初始化内部数据
                        public.execute_cmd('adb -s ' + device_SN + ' shell rm -rf /data/UUID.ini')
                        public.execute_cmd('adb -s ' + device_SN + ' shell rm -rf /data/uuid.log')
                        # 每次循环都要先删除uuid.log内容，避免之前记录混淆导致获取的UUID是错误的
                        try:
                            os.remove(syslog_log)
                        except FileNotFoundError:
                            pass

                        s.uuid_str.set('还没有获取过UUID，正在重启设备中...')
                        # 为了避免设备进入首页后日志被冲掉，因此先清除设备缓存数据
                        # public.execute_cmd('adb -s ' + device_SN + ' shell rm -rf /data/miniapp/data')
                        # 首次必须要进行重启后才能获取
                        public.execute_cmd('adb -s ' + device_SN + ' shell reboot')
                        uuid_reboot_flag = True
                        time.sleep(18)
                        uuid_count = 0
                        while True:
                            uuid_count += 1
                            if uuid_count > 20:
                                break
                            print('uuid_count:' + str(uuid_count))
                            s.uuid_str.set('正在获取UUID中，请耐心等待 ' + str(uuid_count))
                            # s.uuid_str.set('正在获取UUID中，请耐心等待...')
                            # 新方法 - 查询系统底层返回的UUID，成功率极高，成功率高达99%
                            # 临时储存过滤UUID结果
                            # os.system('adb -s ' + device_SN + ' shell grep "UUID" /data/syslog.log > ' + syslog_log)
                            public.execute_cmd('adb -s ' + device_SN + ' shell grep "UUID" /data/syslog.log > ' + syslog_log)
                            uuid_result = open(syslog_log,'r',encoding='utf-8').read()
                            print('查询设备UUID：\n' + uuid_result)
                            uuid_result_local = public.execute_cmd('adb -s ' + device_SN + ' shell cat /data/agOsUUID.txt')
                            uuid_result_local_finally = ' '.join(uuid_result_local.split()).split(':')[-1]
                            # print(uuid_result_local_finally)
                            uuid_re1 = ''.join(re.findall('\(dict\) UUID = (.*?)\n', uuid_result))
                            print('uuid_re1 获取方法1：' + str(uuid_re1))
                            uuid_re2 = ''.join(list(set(re.findall('ota: OtaParameters:mUUID:(.*?)!\n', uuid_result))))
                            print('uuid_re2 获取方法2：' + str(uuid_re2))
                            if uuid_re1 == '' and uuid_re2 == '' and uuid_result_local_finally.strip() == 'No such file or directory':
                                print('没有获取到设备UUID，继续获取中...')
                                continue
                            else:
                                s.uuid_str.set('成功获取到设备UUID...')
                                # 按数据优先级
                                if uuid_result_local_finally.strip() != 'No such file or directory'\
                                    and uuid_result_local_finally.strip() != "device '" + device_SN + "' not found"\
                                    and uuid_result_local_finally.strip() != 'closed':
                                    print('成功获取到设备UUID...')
                                    with open(uuid_path, 'w') as fp:
                                        fp.write(uuid_result_local.strip())
                                    break
                                else:
                                    if uuid_re1 != '':
                                        print('成功获取到设备UUID...')
                                        with open(uuid_path, 'w') as fp:
                                            fp.write(uuid_re1.strip())
                                        break
                                    else:
                                        if uuid_re2 != '':
                                            print('成功获取到设备UUID...')
                                            with open(uuid_path, 'w') as fp:
                                                fp.write(uuid_re2.strip())
                                            break
                                        else:
                                            continue

                            # 旧方法 - 失败率极高
                            # 设备开机后先临时保存日志
                            # public.execute_cmd('adb -s ' + device_SN + ' pull /data/syslog.log ' + syslog_log)
                            # 再上传到设备里面进行过滤读取
                            # public.execute_cmd('adb -s ' + device_SN + ' push ' + syslog_log + ' /data/uuid.log')
                            # try:
                            #     uuid_result = public.execute_cmd('adb -s ' + device_SN + ' shell grep "set_deviceId" /data/uuid.log')
                            #     print('查询设备UUID：\n' + uuid_result)
                            #     uuid_re = re.findall('1=====(.*?)\s/home', uuid_result)
                            #     print(uuid_re)
                            #     uuid_finally = eval(''.join(uuid_re))
                            #     print('成功获取到设备UUID dict...')
                            #     s.uuid_str.set('成功获取到设备UUID...')
                            #     # 注意：python3中dict没有has_key(key)方法,使用自带函数实现 __contains__('key')
                            #     uuid_state = uuid_finally.__contains__('deviceId')
                            #     print('uuid_state: ' + str(uuid_state))
                            #     if not uuid_state:
                            #         continue
                            #     for key, value in uuid_finally.items():
                            #         if key == 'deviceId':
                            #             print(value)
                            #             with open(uuid_path, 'w') as fp:
                            #                 fp.write(value)
                            #             break
                            #     break
                            # except (ValueError,IndexError,SyntaxError):
                            #     print('没有获取到设备UUID，继续获取中...')
                        uuid_reboot_flag = False
                        # 写入UUID后上传到设备中进行读取
                        public.execute_cmd('adb -s ' + device_SN + ' push ' + uuid_path + ' /data/UUID.ini')
                        # 再次读取UUID即可
                        devices_uuid = public.execute_cmd('adb -s ' + device_SN + ' shell cat /data/UUID.ini')
                        if devices_uuid == '':
                            public.execute_cmd('adb -s ' + device_SN + ' shell rm -rf /data/UUID.ini')
                            public.execute_cmd('adb -s ' + device_SN + ' shell rm -rf /data/uuid.log')
                            s.uuid_str.set('该设备UUID获取失败\n请点击下方“重新获取”进行UUID获取吧！')
                        else:
                            s.uuid_str.set('已获取到该设备的UUID为\n' + devices_uuid)
                else:
                    devices_uuid = public.execute_cmd('adb -s ' + device_SN + ' shell cat /data/UUID.ini')
                    if devices_uuid == '':
                        public.execute_cmd('adb -s ' + device_SN + ' shell rm -rf /data/UUID.ini')
                        public.execute_cmd('adb -s ' + device_SN + ' shell rm -rf /data/uuid.log')
                        s.uuid_str.set('该设备UUID获取失败\n请点击下方“重新获取”进行UUID获取吧！')
                    else:
                        s.uuid_str.set('已获取到该设备的UUID为\n' + devices_uuid)
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
            if uuid_get_result_finally.strip() == 'No such file or directory':
                s.uuid_str.set('无法复制粘贴UUID\n请点击下方“重新获取UUID”开始获取UUID吧！')
            else:
                # 复制UUID到剪贴板
                devices_uuid = public.execute_cmd('adb -s ' + device_SN + ' shell cat /data/UUID.ini')
                pyperclip.copy(devices_uuid)
                # 从剪贴板那粘贴
                pyperclip.paste()
                s.root.wm_attributes('-topmost', 1)
                tkinter.messagebox.showinfo('粘贴提醒','已复制粘贴 ' + devices_uuid + ' 到剪贴板\n可以Ctrl+V粘贴到任意地方啦~')
                s.root.wm_attributes('-topmost', 0)
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
