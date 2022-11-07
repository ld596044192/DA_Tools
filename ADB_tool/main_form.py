import sys,os
import signal
import time
import tkinter,tkinter.ttk,tkinter.messagebox,tkinter.filedialog
import threading
import main_public,getpass
from adb_test import adb_test_main  # 调用ADB测试工具
from PIL import Image,ImageTk

#!/usr/bin/env python3+
# This program shows off a python decorator
# which implements tail call optimization. It
# does this by throwing an exception if it is
# it's own grandparent, and catching such
# exceptions to recall the stack.


class TailRecurseException(BaseException):
    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs


def tail_call_optimized(g):
    """
    This function decorates a function with tail call
    optimization. It does this by throwing an exception
    if it is it's own grandparent, and catching such
    exceptions to fake the tail call optimization.

    This function fails if the decorated
    function recurses in a non-tail context.
    """
    def func(*args, **kwargs):
        f = sys._getframe()
        if f.f_back and f.f_back.f_back \
            and f.f_back.f_back.f_code == f.f_code:
            # 抛出异常
            raise TailRecurseException(args, kwargs)
        else:
            while 1:
                try:
                    return g(*args, **kwargs)
                except TailRecurseException as e:
                    args = e.args
                    kwargs = e.kwargs
    func.__doc__ = g.__doc__
    return func

# @tail_call_optimized # 这是修饰器符号，使用后防止栈溢出，报RecursionError: maximum recursion depth exceeded的函数就放在上方即可

# ctrl + shift + - Pycharm一键关闭所有代码块
# ctrl + shift + + Pycharm一键展开所有代码块
# 折叠某一点：ctrl + -
# 展开某一层：ctrl + +


username = getpass.getuser()
main_version_path = main_public.resource_path(os.path.join('version','main_version_history.txt'))
# -----------------------------------
# 打包时需要调用的文件
main_public.resource_path(os.path.join('adb_test','adb_test'))  # ADB测试工具
# -----------------------------------
# 创建临时文件夹
make_dir = 'C:\\Users\\' + username + '\\Documents\\DA_Tools\\'
# 进入某功能需要实时监测功能是否已经启动
main = make_dir + 'main\\'
if not os.path.exists(main):
    os.makedirs(main)
function_status = main + 'function_status.log'
# 调用ADB服务开关（ADB测试工具专门调用ADB服务的）
adb_server_all_flag = True  # 默认True打开
# 统一修改版本号
version = 'V1.0.1'
version_code = 101
# 统一root窗口总宽高
main_width = 600
main_height = 450
# 引入日志
# logging.basicConfig(filename=make_dir + 'log.txt',
#                     level=logging.DEBUG,
#                     filemode='a+',
#                     format='[%(asctime)s] [%(levelname)s] >>> \n%(message)s',
#                     datefmt='%Y-%m-%d %I:%M:%S')


class MainForm(object):
    def root_form(self):
        self.root = tkinter.Tk()
        screenWidth = self.root.winfo_screenwidth()
        screenHeight = self.root.winfo_screenheight()
        w = main_width
        h = main_height
        x = (screenWidth - w) / 2
        y = (screenHeight - h) / 2
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.root.resizable(0, 0)
        # s.root.attributes("-toolwindow", 2)  # 去掉窗口最大化最小化按钮，只保留关闭
        # s.root.overrideredirect(1)  # 隐藏标题栏 最大化最小化按钮
        # s.root.config(bg=bg)
        # 软件始终置顶
        # s.root.wm_attributes('-topmost', 1)
        # s.root.protocol('WM_DELETE_WINDOW', s.exit)  # 点击Tk窗口关闭时直接调用s.exit，不使用默认关闭
        self.root.protocol('WM_DELETE_WINDOW', self.close)  # 退出程序需要处理或结束任务

        # 默认显示窗口页面
        self.all_function()

        self.root.mainloop()

    def function_status_listen(self):
        def t_function_status():
            # 监听功能模块进入情况
            with open(function_status,'w') as fp:
                fp.write('open')
            fp.close()
            while True:
                function_status_read = open(function_status,'r').read()
                if function_status_read.strip() == 'close':
                    self.all_function()  # 回到主界面
                    break

        t_function_status = threading.Thread(target=t_function_status)
        t_function_status.setDaemon(True)
        t_function_status.start()

    def all_function(self):
        # 所有应用返回主界面都要默认加载
        self.root.title('DA万能工具' + version + ' Windows版')
        main_logo = main_public.resource_path(os.path.join('icon', 'my-da.ico'))
        self.root.iconbitmap(main_logo)
        self.display_main_test()

        # 显示主界面菜单按钮
        self.root_label_frame = tkinter.Frame(self.root,width=600,height=50)

        # 测试工具列表
        self.test_list_label = tkinter.Label(self.root_label_frame,text='测试工具')
        self.test_list_label_disbale = tkinter.Label(self.root_label_frame,text='测试工具')
        self.test_list_label_disbale.config(state='disable')
        self.test_list_label_disbale.place(x=60,y=15)
        self.test_list_label.bind('<Button-1>',lambda x:self.display_test_frame())

        # 历史版本显示
        self.main_history_label = tkinter.Label(self.root_label_frame,text='历史版本')
        self.main_history_label_disbale = tkinter.Label(self.root_label_frame,text='历史版本')
        self.main_history_label_disbale.config(state='disable')
        self.main_history_label.place(x=120,y=15)
        self.main_history_label.bind('<Button-1>',lambda x: self.display_history_frame())

        self.root_label_frame.place(x=0,y=0)

    def display_test_frame(self):
        # 显示测试工具应用页面
        self.display_main_test()

        # 恢复按钮显示
        self.main_history_label_disbale.place_forget()

        self.test_list_label_disbale.place(x=60, y=15)
        try:
            self.main_history_frame.place_forget()
        except AttributeError:
            pass

    def display_main_test(self):
        # 显示测试工具应用页面
        self.test_button_frame = tkinter.Frame(self.root, width=600, height=400)

        # 显示ADB测试工具入口按钮
        ADB_Logo_path = main_public.resource_path(os.path.join('icon', 'adb.jpeg'))
        self.adb_test_button = tkinter.Button(self.test_button_frame, bg='green')
        img = Image.open(ADB_Logo_path)
        adb_test_photo = ImageTk.PhotoImage(img)
        self.adb_test_button.config(image=adb_test_photo)
        self.adb_test_button.image = adb_test_photo
        self.adb_test_button.bind('<Button-1>', lambda x: self.adb_test_function())
        self.adb_test_button.place(x=40, y=0)
        # ADB测试工具应用名称显示
        self.adb_test_name = tkinter.Label(self.test_button_frame, text='ADB测试工具')
        self.adb_test_name.place(x=45, y=80)

        self.test_button_frame.place(y=50)  # 默认显示的测试工具页面


    def display_history_frame(self):
        # 显示主界面历史版本页面
        self.display_main_history()

        # 默认第一个的两个都要换
        self.test_list_label.place(x=60, y=15)
        self.test_list_label_disbale.place_forget()

        self.main_history_label_disbale.place(x=120,y=15)
        try:
            self.test_button_frame.place_forget()
        except AttributeError:
            pass

    def display_main_history(self):
        # 历史版本页面逻辑
        self.main_history_frame = tkinter.Frame(self.root, width=600, height=400)
        self.main_history = tkinter.Frame(self.main_history_frame)
        self.scrollbar = tkinter.Scrollbar(self.main_history)
        self.version_listbox = tkinter.Listbox(self.main_history, width=55, height=20, yscrollcommand=(self.scrollbar.set))
        self.version_listbox.bindtags((self.version_listbox, 'all'))
        self.scrollbar.config(command=(self.version_listbox.yview))
        self.scrollbar.pack(side=(tkinter.RIGHT), fill=(tkinter.Y))
        self.version_listbox.pack()
        version_read = open(main_version_path, 'r', encoding='utf-8',errors='ignore')
        for readline in version_read.readlines():
            self.version_listbox.insert(tkinter.END, readline)
        version_read.close()
        self.main_history.place(x=5,y=10)
        self.main_history_frame.place(y=50)

    def adb_test_function(self):
        # 进入ADB测试工具
        def t_adb_test():
            global adb_server_all_flag
            # if tkinter.messagebox.askyesno('打开提醒','是否打开ADB测试工具'):
            self.function_status_listen()  # 开始监听开关状态
            self.adb_test_button.place_forget()
            self.root_label_frame.place_forget()
            self.test_button_frame.place_forget()
            # 每次进入需要打开ADB服务
            adb_server_all_flag = True
            adb_test = adb_test_main.ADB_Test()
            adb_test.adb_root_form(self.root)

        t_adb_test = threading.Thread(target=t_adb_test)
        t_adb_test.setDaemon(True)
        t_adb_test.start()

    def close(s):
        if tkinter.messagebox.askyesno(title='关闭提醒',message='确定要关闭本工具？'):
            # 结束主程序
            s.root.destroy()  # 关闭主窗口
            pid = os.getpid()  # 获取本工具的pid
            os.kill(pid,signal.SIGINT)  # 避免残留后台运行强制杀死
            sys.exit()  # 终止程序

    # def crawler_settings_bind(self):
    #     def t_crawler_settings():
    #         # 初始化通用爬虫参数设置页面的状态
    #         with open(main_public.crawler_setting_page(), 'w') as fp:
    #             fp.write('')
    #         fp.close()
    #         crawer_settings = public_crawler_setting.Crawler_Settings()
    #         crawer_settings.setting_form(self.general_params_button,self.general_params_button_disable)
    #
    #     def t_crawler_settings_close():
    #         # 监听通用爬虫参数设置页面的关闭状态
    #         with open(main_public.crawler_setting_page(), 'w') as fp:
    #             fp.write('')
    #         fp.close()
    #         while True:
    #             md5_size_page_state = open(main_public.crawler_setting_page(), 'r').read()
    #             if md5_size_page_state.strip() == '0':
    #                 print('获取通用爬虫参数设置页面已关闭！')
    #                 self.general_params_button_disable.place_forget()
    #                 self.general_params_button.place(x=500, y=0)
    #                 try:
    #                     main_public.stop_thread(t_crawler_settings)  # 关闭后终止线程
    #                 except ValueError:
    #                     pass
    #                 break
    #             else:
    #                 self.general_params_button.place_forget()
    #                 self.general_params_button_disable.place(x=500, y=0)
    #             time.sleep(1)
    #
    #     t_crawler_settings = threading.Thread(target=t_crawler_settings)
    #     t_crawler_settings.setDaemon(True)
    #     t_crawler_settings.start()
    #
    #     t_crawler_settings_close = threading.Thread(target=t_crawler_settings_close)
    #     t_crawler_settings_close.setDaemon(True)
    #     t_crawler_settings_close.start()