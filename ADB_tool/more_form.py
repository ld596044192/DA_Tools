import tkinter,os,threading,tkinter.messagebox,getpass,sys,time
import public
from pathlib import Path

username = getpass.getuser()
LOGO_path = public.resource_path(os.path.join('icon', 'android.ico'))
# 创建临时文件夹
make_dir = 'C:\\Users\\' + username + '\\Documents\\ADB_Tools(DA)\\'
conflict_software_state = public.resource_path(os.path.join('temp','conflict_software_state.txt'))
# 简易ADB - adb-tools检测标志
adb_tools_flag = make_dir + 'adb-tools'


class ConflictSoftware(object):
    # def conflict_software_form(self,conflict_software):
    def conflict_software_form(self):
        self.conflict_software_root = tkinter.Tk()
        # self.conflict_software_root.title('正在兼容冲突软件 ' + conflict_software)
        self.conflict_software_root.title('正在兼容冲突软件 ')
        screenWidth = self.conflict_software_root.winfo_screenwidth()
        screenHeight = self.conflict_software_root.winfo_screenheight()
        w = 400
        h = 300
        x = (screenWidth - w) / 2
        y = (screenHeight - h) / 2
        self.conflict_software_root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.conflict_software_root.geometry('%dx%d' % (w, h))
        self.conflict_software_root.iconbitmap(LOGO_path)
        self.conflict_software_root.resizable(0, 0)
        self.conflict_software_root.wm_attributes('-topmost', 1)  # 置顶窗口
        self.conflict_software_root.attributes("-toolwindow", 2)  # 去掉窗口最大化最小化按钮，只保留关闭

        self.conflict_software_root.protocol('WM_DELETE_WINDOW', self.close_handle)
        self.main_frame()
        self.conflict_software_root.mainloop()
        return self.conflict_software_root

    def close_handle(self):
        # 关闭无效
        pass

    def main_frame(self):
        self.conflict_software_frame = tkinter.Frame(self.conflict_software_root, width=400, height=300)
        # 冲突说明
        conflict_content = '检测到 XXX 冲突软件正在启动中...\n' \
                           '因ADB环境不同该软件会与ADB测试工具发生严重冲突\n' \
                           '会导致ADB测试工具闪退或该冲突软件无法识别设备等\n' \
                           '下面将会使用兼容模式 - 兼容使用冲突软件ADB环境\n'
        self.conflict_software_label= tkinter.Label(self.conflict_software_frame, text=conflict_content, fg='red', width=40,
                                                      font=('微软雅黑', 10))
        self.conflict_software_label.place(x=20, y=10)

        # 冲突软件地址说明
        conflict_path_content = '下面请输入冲突软件 XXX 的文件路径（不要输错哦！）：'
        self.conflict_software_path_label = tkinter.Label(self.conflict_software_frame, text= conflict_path_content, fg='red',
                                                     width=40,
                                                     font=('微软雅黑', 10))
        self.conflict_software_path_label.place(x=20, y=100)

        # 冲突软件地址输入框
        self.conflict_software_entry_str = tkinter.StringVar()
        self.conflict_software_entry = tkinter.Entry(self.conflict_software_frame, textvariable=self.conflict_software_entry_str,
                                             width=40, highlightcolor='pink', validate="focusin"
                                             , highlightthickness=5)
        self.conflict_software_entry.place(x=20, y=130)
        # self.conflict_software_entry.config(command=self.conflict_software_entry_bind())

        # 同意兼容或拒绝说明
        conflict_okandcancel_content = '点击“同意并兼容”则开始重新配置ADB环境变量；\n点击“取消”则会关闭ADB测试工具！！！'
        self.conflict_software_okandcancel_label = tkinter.Label(self.conflict_software_frame, text=conflict_okandcancel_content,
                                                          fg='red',
                                                          width=40,
                                                          font=('微软雅黑', 10))
        self.conflict_software_okandcancel_label.place(x=20, y=210)

        # 同意按钮
        self.conflict_ok_button = tkinter.Button(self.conflict_software_frame, text='同意并兼容', width=20)
        self.conflict_ok_button.bind('<Button-1>', lambda x: self.conflict_ok_bind())
        self.conflict_ok_button_disable = tkinter.Button(self.conflict_software_frame, text='同意并兼容', width=20)
        self.conflict_ok_button_disable.config(state='disable')
        self.conflict_ok_button.place(x=20, y=250)

        # 取消按钮
        self.conflict_cancel_button = tkinter.Button(self.conflict_software_frame, text='取消并退出', width=20)
        self.conflict_cancel_button.bind('<Button-1>', lambda x: self.conflict_cancel_bind())
        self.conflict_cancel_button_disable = tkinter.Button(self.conflict_software_frame, text='取消并退出', width=20)
        self.conflict_cancel_button_disable.config(state='disable')
        self.conflict_cancel_button.place(x=200, y=250)
        self.conflict_software_frame.pack()

    def conflict_software_list_frame(self):
        # 兼容进度记录ListBox
        self.conflict_software_listbox_frame = tkinter.Frame(self.conflict_software_root, width=200, height=198)
        # 创建滚动条
        self.conflict_software_scrollbar = tkinter.Scrollbar(self.conflict_software_listbox_frame)
        # listbox控件创建并与滚动条绑定
        self.conflict_software_listbox = tkinter.Listbox(self.conflict_software_listbox_frame, width=53, height=16,
                                                         bg='black',
                                                         fg='#FFFFFF',font=('微软雅黑',10),
                                                         yscrollcommand=(self.conflict_software_scrollbar.set))
        # listbox内容数据联动滚动条
        self.conflict_software_scrollbar.config(command=(self.conflict_software_listbox.yview))
        # 显示滚动条
        self.conflict_software_scrollbar.pack(side=(tkinter.RIGHT), fill=(tkinter.Y))
        self.conflict_software_listbox.bindtags((self.conflict_software_listbox, 'all'))
        self.conflict_software_listbox.pack()
        self.conflict_software_listbox_frame.place(x=5, y=5)

    def conflict_ok_bind(self):
        def t_conflict_ok():
            conflict_software_path = self.conflict_software_entry_str.get()
            print(conflict_software_path)
            if not os.path.exists(conflict_software_path):
                self.conflict_ok_button_disable.place(x=20, y=250)
                tkinter.messagebox.showwarning(title='路径不存在', message='该路径不存在，请重新输入正确的文件路径！！！')
                self.conflict_ok_button_disable.place_forget()
            else:
                my_file = Path(conflict_software_path)
                if my_file.is_dir():
                    self.conflict_software_frame.place_forget()
                    self.conflict_software_list_frame()
                    self.conflict_software_listbox.config(command=self.conflict_software_listbox_bind(conflict_software_path))
                    self.conflict_software_listbox.insert(0, '此处显示冲突兼容输出信息-------')
                else:
                    self.conflict_ok_button_disable.place(x=20, y=250)
                    tkinter.messagebox.showwarning(title='路径不是目录', message='该路径不是文件夹或目录，无法进行冲突兼容！！！')
                    self.conflict_ok_button_disable.place_forget()

        t_conflict_ok = threading.Thread(target=t_conflict_ok)
        t_conflict_ok.setDaemon(True)
        t_conflict_ok.start()

    def conflict_cancel_bind(self):
        def t_conflict_cancel():
            self.conflict_cancel_button_disable.place(x=200, y=250)
            cancel_content = '提示：点击确定则关闭ADB测试工具，取消则返回兼容窗口继续进行冲突兼容！！！'
            if tkinter.messagebox.askokcancel(title='是否确定关闭？',message=cancel_content):
                self.conflict_software_root.destroy()
                sys.exit()
            self.conflict_cancel_button_disable.place_forget()

        t_conflict_cancel = threading.Thread(target=t_conflict_cancel)
        t_conflict_cancel.setDaemon(True)
        t_conflict_cancel.start()

    def conflict_software_listbox_bind(self,conflict_software_path):
        # 冲突兼容主逻辑
        self.conflict_software_listbox.insert(tkinter.END, '正在开始冲突兼容...')
        # 删除ADB测试工具默认锁定的环境变量
        self.conflict_software_listbox.insert(tkinter.END, '正在删除旧的ADB环境变量...')
        new_environ = public.remove_environ(adb_tools_flag)
        # 重新配置ADB环境变量
        self.conflict_software_listbox.insert(tkinter.END,'正在重新配置ADB环境变量...')
        # 先设置移除旧的新环境变量
        command = r'setx "Path" ' + '"' + new_environ + '" /m'
        print(command)
        result = public.execute_cmd(command)
        print(result)
        # 配置新的环境变量
        # public.temporary_environ(conflict_software_path)
        public.permanent_environ(conflict_software_path)
        self.conflict_software_listbox.insert(tkinter.END, '环境变量设置完成！！！')
        # 测试ADB版本
        # self.conflict_software_listbox.insert(tkinter.END, '正在测试ADB版本是否正常...')
        # time.sleep(5)
        # adb_version_result = public.execute_cmd('adb version')
        # self.conflict_software_listbox.insert(tkinter.END, adb_version_result)
        # self.conflict_software_listbox.see(tkinter.END)
        # 10S后自动关闭该程序
        self.conflict_software_listbox.insert(tkinter.END, '10S后自动关闭该程序...')
        self.conflict_software_listbox.see(tkinter.END)
        # 状态变更
        with open(conflict_software_state, 'w') as fp:
            fp.write('Conflicting software is already compatible')
        time.sleep(10)
        self.conflict_software_root.destroy()
        sys.exit()

# # -*- coding:utf-8 -*-
# import ctypes,sys
#
#
# def run_program():
#
#     def is_admin():
#         try:
#             return ctypes.windll.shell32.IsUserAnAdmin()
#         except:
#             return False
#
#     if is_admin():
#         conflict_software_main = ConflictSoftware()
#         conflict_software_main.conflict_software_form()
#     else:
#         ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, __file__, None, 1)
#
#
# run_program()


