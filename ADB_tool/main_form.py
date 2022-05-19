import re
import shutil
import time
import tkinter,tkinter.ttk,tkinter.messagebox
import threading
import os,psutil,zipfile
import public,getpass
import quickly,screen_record,linux_main

# 全局变量标记-设备类型
devices_linux_flag = False
# 全局变量标记-设备检测
adb_service_flag = True

username = getpass.getuser()
LOGO_path = public.resource_path(os.path.join('icon', 'android.ico'))
version_path = public.resource_path(os.path.join('version','version_history.txt'))
adb_path = public.resource_path(os.path.join('resources','adb-tools.zip'))
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
# 统一修改版本号
version = 'V1.0.0.12'
version_code = 1001.2
# 统一修改frame的宽高
width = 600
height = 405
# 统一按钮宽度
width_button = 20


class MainForm(object):
    def root_form(s):
        s.root = tkinter.Tk()
        s.root.title('ADB测试工具' + version + ' tktiner版')
        screenWidth = s.root.winfo_screenwidth()
        screenHeight = s.root.winfo_screenheight()
        w = 600
        h = 450
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
            s.verion_frame.place_forget()
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
            s.verion_frame.place_forget()
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
            s.verion_frame.place_forget()
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
            s.verion_frame.place_forget()
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
                                                                                 ,s.linux_init_Button_disable))
        s.linux_init_Button_disable.place(x=200, y=110)

        # 重新检测按钮
        s.init_again_Button = tkinter.Button(s.linux_frame1, text='点击重新检测', width=width_button)
        s.init_again_Button.bind('<Button-1>',lambda x:linux_main.check_init(s.init_str,s.linux_init_Button
                                    ,s.linux_init_Button_disable,devices_linux_flag,s.linux_all_button_close))
        s.init_again_Button.place(x=20,y=110)

        # 初始化状态栏
        s.init_label = tkinter.Label(s.linux_frame1, textvariable=s.init_str, bg='black', fg='#FFFFFF',
                                       width=46, height=2)
        s.init_label.config(command=linux_main.check_init(s.init_str,s.linux_init_Button,s.linux_init_Button_disable,
                                                          devices_linux_flag,s.linux_all_button_close))
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
        s.linux_developer_mode_content = """访问设备本地盘需要关闭ADB命令，届时本工具不能连接该设备\n恢复ADB命令需要手动在设备上的“设置-关于-固件版本”，连续点击5下后重启
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

        # 开始默认禁用，根据情况开启
        s.linux_all_button_close()

        s.linux_frame1.place(y=20)

    def linux_all_button_close(s):
        def linux_all_button_place_forget():
            # 特殊情况下禁用linux模式所有功能（包含已disable状态的按钮）
            s.linux_screen_Button.place_forget()
            s.linux_screen_Button_disable.place_forget()
            s.linux_developer_mode_Button_close.place_forget()
            s.linux_developer_mode_Button_close_disable.place_forget()
            s.linux_install.place_forget()
            s.linux_install_disable.place_forget()
            s.linux_camera.place_forget()
            s.linux_camera_disable.place_forget()

            s.linux_button_label.place(x=20, y=220)

        devices = public.device_connect()
        if not devices:
            s.linux_init_Button.place_forget()
            s.linux_init_Button_disable.place(x=200, y=110)

            linux_all_button_place_forget()
        else:
            linux_all_button_place_forget()

    def linux_all_button_open(s):
        # 先禁用初始化按钮
        s.linux_init_Button.place_forget()
        s.linux_init_Button_disable.place(x=200,y=110)

        # 正常情况下开启linux模式所有功能
        s.linux_button_label.place_forget()
        s.linux_screen_Button.place(x=20, y=190)
        s.linux_developer_mode_Button_close.place(x=200,y=190)
        s.linux_install.place(x=20,y=230)
        s.linux_camera.place(x=20,y=270)

    def version_history_frame(s):
        # 历史版本信息窗口
        s.verion_frame = tkinter.Frame(s.root,width=width,height=height)
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
            s.devices_str.set('正在检测设备连接状态...')
            while True:
                # 获取设备序列号
                devices_finally = public.device_connect()
                # print(devices_finally)
                if not devices_finally:
                    s.devices_fail.place(x=470, y=0)
                    s.devices_type_fail.place(x=325,y=425)
                    s.devices_success.place_forget()
                    s.devices_type_success.place_forget()
                    s.devices_null.set('未连接任何设备！')
                    s.devices_type_error.set('未连接任何设备！')
                    # 确保切换设备类型时Linux相关功能按钮不会主动显示出来
                    try:
                        s.linux_all_button_close()
                    except AttributeError:
                        pass
                # elif devices_finally == 'error: device not found':
                #     s.devices_null.set('获取设备失败，正在重新获取...')
                #     continue
                else:
                    s.devices_fail.place_forget()
                    s.devices_type_fail.place_forget()
                    s.devices_success.place(x=450,y=0)
                    s.devices_type_success.place(x=325,y=425)
                    for devices in devices_finally:
                        if len(devices_finally) == 1:
                            s.devices_str.set(devices + ' 已连接')
                        elif len(devices_finally) > 1:
                            s.devices_str.set('多部设备已连接')
                    time.sleep(1)

        def devices_type():
            try:
                s.devices_type_str.set('正在检测设备类型...')
            except AttributeError:
                pass
            while True:
                global devices_linux_flag
                # 检测设备类型
                device_type = public.device_type_android()
                # print(device_type.strip())  # 调试Logs
                # 增加strip方法，去掉结果的两边空格以便进行识别
                if device_type.strip() == 'Android':
                    s.devices_type_str.set('Android（安卓）')
                    devices_linux_flag = False
                elif device_type.strip() == '/bin/sh: getprop: not found':
                    # Linux无法使用adb shell getprop命令
                    device_type_linux = public.execute_cmd('adb shell cat /proc/version')
                    device_type_linux_finally = device_type_linux.split(' ')[0]
                    # print(device_type_linux_finally)  # 调试Logs
                    if device_type_linux_finally == 'Linux':
                        s.devices_type_str.set('Linux')
                        devices_linux_flag = True
                    else:
                        s.devices_type_str.set('未知设备')
                time.sleep(1)

        t_devices = threading.Thread(target=t_devices)
        t_devices.setDaemon(True)
        t_devices.start()

        devices_type = threading.Thread(target=devices_type)
        devices_type.setDaemon(True)
        devices_type.start()

    def adb_bind(s):
        # 检测ADB服务状态
        def adb_install():
            # 一键配置ADB核心步骤
            if not os.path.exists(adb_tools_flag):
                shutil.copy(adb_path,make_dir)
                # 解压
                zip_path = make_dir + 'adb-tools.zip'
                public.zip_extract(zip_path,make_dir)
                # 清理压缩包
                os.remove(zip_path)
                # 配置环境变量
                public.temporary_environ(adb_tools_flag)
                public.permanent_environ(adb_tools_flag)
                # 打印测试
                print(public.execute_cmd('adb version'))

        def t_adb():
            # time.sleep(5)  # 等待ADB服务启动完毕
            while True:
                time.sleep(1)
                # 中文状态下
                adb_finally = public.adb_connect()[1]
                try:
                    # 英文状态下
                    adb_english = ' '.join(public.adb_connect()).split(',')[1]
                    if adb_finally == '不是内部或外部命令，也不是可运行的程序' or adb_english == ' operable program or batch file.':
                        # os.chdir(adb_path)
                        # s.adb_str.set('内置ADB已开启！')
                        s.adb_str.set('正在配置ADB...')
                        adb_install()
                        s.adb_str.set('ADB已配置成功！')
                        time.sleep(3)
                        s.adb_str.set('本地ADB已开启！')
                        break
                    else:
                        s.adb_str.set('本地ADB已开启！')
                        print(public.execute_cmd('adb version'))
                        break
                except IndexError:
                    print('IndexError异常，无影响！')
                    if adb_finally == '不是内部或外部命令，也不是可运行的程序':
                        # os.chdir(adb_path)
                        # s.adb_str.set('内置ADB已开启！')
                        s.adb_str.set('正在配置ADB...')
                        adb_install()
                        s.adb_str.set('ADB已配置成功！')
                        time.sleep(3)
                        s.adb_str.set('本地ADB已开启！')
                        break
                    else:
                        s.adb_str.set('本地ADB已开启！')
                        print(public.execute_cmd('adb version'))
                        break

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
                    make_state = screen_record.cd_screenshots(s.screen_str)
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
                screen_record.record(s.record_name,s.record_time_selected,str(s.record_model_selected))

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
                if record_model_get == '0':
                    s.record_str.set('正在保存录屏文件，请稍等...')
                    # s.record_name = open(record_name,'r').read()
                    s.record_name = s.record_entry.get()
                    screen_record.record_pull(s.record_name, record_model_get)
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

                    # 连续模式计数
                    r = int(open(record_count, 'r').read())
                    r += 1
                    with open(record_count, 'w') as fp:
                        fp.write(str(r))
                    s.record_str.set('正在保存连续模式录屏文件，请稍等...')
                    s.record_name = s.record_entry.get()
                    screen_record.record_pull(s.record_name,record_model_get)
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
                    # 关闭ADB服务
                    public.execute_cmd('adb kill-server')
                    # 重启ADB服务
                    public.execute_cmd('adb start-server')
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
                check_only_read = public.execute_cmd('adb shell ls -lh /data/.overlay')
                only_read = ' '.join(check_only_read.split()).split(':')[-1]
                return only_read

            while True:
                # linux_frame_exists = s.linux_frame1.winfo_exists()
                devices_finally = public.device_connect()
                s.init_text = s.init_str.get()
                only_read = check_only_read()
                if s.init_text == '该设备没有初始化\n请点击下方按钮进行设备初始化' or s.init_text == '此处显示初始化状态'\
                        or not devices_linux_flag or not devices_finally or only_read == ' No such file or directory':
                    s.linux_all_button_close()
                elif s.init_text == '该设备已初始化\n无需初始化，可正常使用下方功能' and devices_linux_flag and devices_finally\
                          and only_read != ' No such file or directory':
                    s.linux_all_button_open()
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
            linux_screen.screen_form(s.init_str,s.linux_screen_Button,s.linux_screen_Button_disable)

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
                public.execute_cmd('adb shell rm -rf /data/.adb_config')
                public.execute_cmd('adb shell reboot')
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
            linux_install.install_form(s.init_str,s.linux_install,s.linux_install_disable)

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
            linux_camera.camera_form(s.init_str,s.linux_camera,s.linux_camera_disable)

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
                    package_name = public.found_packages()
                    print(package_name)
                    s.uninstall_str.set('已检测到当前包名\n' + package_name)

                    if not uninstall_flag:
                        s.uninstall_str.set('检测到' + package_name + '\n正在卸载中...')
                        public.execute_cmd('adb uninstall ' + package_name)
                        uninstall_flag = True
                        s.uninstall_str.set('APK已卸载成功！')
                    else:
                        pass
                except IndexError:
                    s.uninstall_str.set('检测到非安卓设备\n请使用安卓设备进行操作')

            s.check_package_name_button_disable.place_forget()

        t_check_package_name = threading.Thread(target=t_check_package_name)
        t_check_package_name.setDaemon(True)
        t_check_package_name.start()
