# 软件启动前的Logo加载界面
import signal
import sys
import time
import tkinter.messagebox
import public
import os,getpass
from PIL import ImageTk,Image
import threading


loading_logo_path = public.resource_path(os.path.join('loading', 'loading_logo.gif'))
username = getpass.getuser()

# 创建临时文件夹
make_dir = 'C:\\Users\\' + username + '\\Documents\\ADB_Tools(DA)\\'
if not os.path.exists(make_dir):
    os.makedirs(make_dir)
# 主程序启动标志
root_state = make_dir + 'root_state.txt'


class MainForm_Logo(object):
    def root_form(self):
        self.root_logo = tkinter.Tk()

        screenWidth = self.root_logo.winfo_screenwidth()
        screenHeight = self.root_logo.winfo_screenheight()
        w = 600
        h = 450
        x = (screenWidth - w) / 2
        y = (screenHeight - h) / 2
        self.root_logo.geometry('%dx%d+%d+%d' % (w, h, x, y))
        # 隐藏标题栏和最大、最小关闭按钮
        self.root_logo.overrideredirect(True)

        self.root_logo.wm_attributes('-topmost', 1)
        self.background_logo()

        self.root_logo.mainloop()

    def background_logo(self):
        # 设置背景图片
        bg_logo_canvas = tkinter.Canvas(self.root_logo,width=600,height=450,bd=0,highlightthickness=0)
        # 打开图片（变量命名前要加self，否则背景图片无法显示）
        self.logo_img = Image.open(loading_logo_path)
        # 读取图片
        self.logo_photo = ImageTk.PhotoImage(self.logo_img)

        # 创建背景（前面 0，0 是偏移量，anchor始置于画布左上角，这样就铺满全图）
        bg_logo_canvas.create_image(0,0,image=self.logo_photo,anchor='nw')

        # 新建 加载进度提示标签
        self.loading_str = tkinter.StringVar()
        loading_label = tkinter.Label(self.root_logo,textvariable=self.loading_str,bg='black',fg='#FFFFFF',font=('华文行楷',15))

        # 在画布上插入loading_label
        self.text_canvas_x = 300
        bg_logo_canvas.create_window(self.text_canvas_x,400,width=1200,height=30,window=loading_label)

        bg_logo_canvas.place(x=0,y=0)

        # 加载界面逻辑处理
        self.check_safety_software()

    def check_safety_software(self):
        def t_check_safety():
            pid = os.getpid()
            self.loading_str.set('正在检测运行中的杀毒软件...')
            # 需要检测的杀毒软件
            target_names_dict = {'QQPCTray.exe': '电脑管家'}

            # 获取正在运行的杀毒软件名称
            pid_names = public.get_pid_name()
            for key, value in target_names_dict.items():
                if key in pid_names:
                    safety_name = target_names_dict[key]
                    check_safety_message = '''
                                       已检测到杀毒软件正在运行中，如下：\n
                                       ''' + safety_name + '''\n
                                       是否已经手动关闭 ''' + safety_name + '''？\n
                                       点击“确定”则默认您已经手动关闭杀毒软件
                                       点击“取消”则结束本程序\n
                                       PS:如遇杀软误杀文件影响功能使用请重启本软件\n
                                       温馨提醒：
                                       本软件属于开源免费软件，绿色安全无毒
                                       被报毒均为杀软误报！！！
                                       '''
                    if tkinter.messagebox.askokcancel(title='检测结果', message=check_safety_message):
                        with open(root_state, 'w') as fp:
                            fp.write('0-1')
                        break
                    else:
                        with open(root_state, 'w') as fp:
                            fp.write('main_stop')
                        # 杀死进程
                        os.kill(int(pid), signal.SIGINT)
                else:
                    with open(root_state, 'w') as fp:
                        fp.write('0-1')
                    break

            self.loading_str.set('正在获取系统权限...')
            time.sleep(2)
            self.loading_str.set('正在加载软件...')
            while True:
                root_state_finally = open(root_state, 'r').read()
                if root_state_finally == '1':
                    # self.root_logo.destroy()
                    # 杀死进程
                    os.kill(int(pid),signal.SIGINT)

        t_check_safety = threading.Thread(target=t_check_safety)
        t_check_safety.setDaemon = True
        t_check_safety.start()


if __name__ == '__main__':
    logo = MainForm_Logo()
    logo.root_form()
