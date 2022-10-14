# 这是爬虫程序通用设置
import getpass,os.path,re
import threading,shutil
import tkinter
import public
from pathlib2 import Path

username = getpass.getuser()
# 创建临时文件夹
make_dir = 'C:\\Users\\' + username + '\\Documents\\DA_Tools\\'
# 进入某功能需要实时监测功能是否已经启动
crawler_settings = make_dir + 'crawler_settings\\'
crawler_settings_log = crawler_settings + 'crawler_settings_null.ini'
crawler_page = crawler_settings + 'crawler_page'
# 默认参数设置文件（需要开发者手动配置可用的参数）
default_settings = public.resource_path(os.path.join('settings', 'crawler_default_settings.ini'))
# 自定义参数设置文件（默认为空）
customize_settings = public.resource_path(os.path.join('settings', 'crawler_settings_null.ini'))
# 初始化文件
if not os.path.exists(crawler_settings):
    os.makedirs(crawler_settings)
setting_logo = public.resource_path(os.path.join('icon', 'crawler_settings.ico'))
# 每次进入页面首次需要处理一次
crawler_first_flag = False
# 首次不执行
crawler_not_first_flag = False


def replace_content(search_text,replace_text,file_name):
    # 替换文件中的字符串
    # 使用Path函数打开文件
    file = Path(file_name)
    # 读取文件内容并将其存储在数据变量中
    data = file.read_text()
    # 使用替换功能替换文本
    data = data.replace(search_text,replace_text)
    # 在文本文件中写入替换的数据
    file.write_text(data)


class Crawler_Settings(object):
    def setting_form(self,general_params_button,general_params_button_disable):
        self.crawler_setting_root = tkinter.Toplevel()
        self.crawler_setting_root.title('爬虫参数通用设置')
        # screenWidth = self.screen_root.winfo_screenwidth()
        # screenHeight = self.screen_root.winfo_screenheight()
        w = 400
        h = 500
        # x = (screenWidth - w) / 2
        # y = (screenHeight - h) / 2
        self.crawler_setting_root.geometry('%dx%d' % (w, h))
        self.crawler_setting_root.iconbitmap(setting_logo)
        self.crawler_setting_root.resizable(0, 0)
        # self.screen_root.wm_attributes('-topmost', 1)

        self.setting_startup(general_params_button, general_params_button_disable)

        self.crawler_setting_root.protocol('WM_DELETE_WINDOW', self.close_handle)

        self.main_frame()

    def setting_startup(self,general_params_button,general_params_button_disable):
        # 监听截图页面的打开状态
        crawler_exists = self.crawler_setting_root.winfo_exists()
        print(crawler_exists)
        if crawler_exists == 1:
            general_params_button.place_forget()
            general_params_button_disable.place(x=500, y=0)

    def close_handle(self):
        global crawler_first_flag,check_button_flag,crawler_not_first_flag
        # 监听页面消失
        with open(crawler_page,'w') as fp:
            fp.write('0')
        fp.close()
        crawler_first_flag = False
        check_button_flag = False
        crawler_not_first_flag = False
        self.crawler_setting_root.destroy()

    def main_frame(self):
        # User-Agent
        self.user_agent_label = tkinter.Label(self.crawler_setting_root,text='User-Agent设置:')
        self.user_agent_label.place(x=20,y=10)

        self.user_agent_set = tkinter.IntVar()

        self.user_agent_text = tkinter.Text(self.crawler_setting_root,width=50, height=5,font=('宋体', 10))
        self.user_agent_text.config(command=self.user_agent_bind())
        self.user_agent_text.place(x=20,y=40)

        self.user_agent_set_checkbutton = tkinter.Checkbutton(self.crawler_setting_root, text='勾选采用自定义参数',
                                                              onvalue=1, offvalue=0, variable=self.user_agent_set)
        self.user_agent_set_checkbutton.bind('<Button-1>', lambda x: self.user_agent_bind())
        self.user_agent_set.set(0)
        self.user_agent_set_checkbutton.place(x=20, y=110)
        user_agent_warnning = '点击勾选采取自定义的User-Agent参数，不再使用默认\n' \
                              '使用自定义参数有风险，请确保参数是正确的，不正确将导致爬虫出现问题\n' \
                              '如何获取正确的User-Agent参数，方法如下：\n' \
                              '1.先打开浏览器，如无默认导航页请手动进入www.baidu.com\n' \
                              '2.打开任意网页，按F12进入检查页面，选择Network\n' \
                              '3.点击下方任一请求数据，查看Headers项 - Request Headers中的user-agent\n' \
                              '4.后面一大串就是user-agent的值，复制到文本框，然后点击勾选自定义即可成功设置完毕！\n' \
                              '温馨提示：新手建议使用默认参数设置或网上直接查找可用的，避免自定义出现问题'
        public.CreateToolTip(self.user_agent_set_checkbutton, user_agent_warnning)

        # 检查是否默认勾选自定义按钮，每次进入首页根据之前设置进行设定
        user_agent_read = ''.join(open(crawler_settings_log, 'r').readlines())
        user_agent_value = ''.join(re.findall('User-Agent_Button=(.*?)\n', user_agent_read, re.S))
        if user_agent_value == 'False':
            self.user_agent_set.set(0)  # 默认不勾选
        elif user_agent_value == 'True':
            self.user_agent_set.set(1)  # 默认勾选
        else:  # 如果变量为空
            self.user_agent_set.set(0)

    def user_agent_bind(self):
        def t_user_agent():
            global crawler_first_flag,check_button_flag,crawler_not_first_flag
            # User-Agent逻辑
            if not os.path.exists(crawler_settings_log):
                shutil.copy(customize_settings,crawler_settings)

            # print(self.user_agent_set.get())

            # 根据Bool类型状态判断是否被勾选
            user_agent_read = ''.join(open(crawler_settings_log, 'r').readlines())
            user_agent_value = ''.join(re.findall('User-Agent_Button=(.*?)\n', user_agent_read, re.S))
            # print(user_agent_value)

            # crawler_first_flag主要针对checkbutton第一次和第二次的值会相同导致错误，特地进行区分（首次执行和首次不执行）
            if not crawler_first_flag and self.user_agent_set.get() == 0 and user_agent_value == 'True':  # 首次执行
                user_agent_read = ''.join(open(crawler_settings_log, 'r').readlines())
                user_agent_customize = ''.join(re.findall('User-Agent=(.*?)\n', user_agent_read, re.S))
                self.user_agent_text.delete(0.0, tkinter.END)  # 先清空内容
                self.user_agent_text.insert(tkinter.END, user_agent_customize)
                crawler_first_flag = True
                crawler_not_first_flag = True

            # 默认读取参数设置
            if crawler_first_flag and self.user_agent_set.get() == 0:  # 首次不执行
                user_agent_read = ''.join(open(crawler_settings_log,'r').readlines())
                user_agent_customize = ''.join(re.findall('User-Agent=(.*?)\n',user_agent_read,re.S))
                user_agent_search = 'User-Agent=' + user_agent_customize.strip()
                user_agent_content = self.user_agent_text.get(0.0, tkinter.END)
                user_agent_replace_content = 'User-Agent=' + user_agent_content.strip()  # 要替换的文本
                replace_content(user_agent_search,user_agent_replace_content,crawler_settings_log)
                print('自定义参数已设置完毕！')

                if crawler_not_first_flag:  # 首次不执行
                    # 设置自定义按钮bool值(True)
                    user_agent_customize = ''.join(re.findall('User-Agent_Button=(.*?)\n', user_agent_read, re.S))
                    user_agent_search = 'User-Agent_Button=' + user_agent_customize.strip()
                    user_agent_replace_content = 'User-Agent_Button=True'  # 要替换的文本
                    replace_content(user_agent_search, user_agent_replace_content, crawler_settings_log)
            else:
                if not crawler_first_flag and self.user_agent_set.get() == 0 and user_agent_value == 'False' or \
                    user_agent_value.strip() == '':  # 首次执行
                    user_agent_default_read = ''.join(open(default_settings,'r').readlines())
                    user_agent_default = ''.join(re.findall('User-Agent=(.*?)\n',user_agent_default_read,re.S))
                    self.user_agent_text.delete(0.0,tkinter.END)  # 先清空内容
                    self.user_agent_text.insert(tkinter.END,user_agent_default)
                    crawler_first_flag = True
                    crawler_not_first_flag = True

                if crawler_not_first_flag and self.user_agent_set.get() == 1:  # 首次不执行
                    user_agent_default_read = ''.join(open(default_settings, 'r').readlines())
                    user_agent_default = ''.join(re.findall('User-Agent=(.*?)\n', user_agent_default_read, re.S))
                    self.user_agent_text.delete(0.0, tkinter.END)  # 先清空内容
                    self.user_agent_text.insert(tkinter.END, user_agent_default)

                    # 设置自定义按钮bool值(False)
                    user_agent_read = ''.join(open(crawler_settings_log, 'r').readlines())
                    user_agent_customize = ''.join(re.findall('User-Agent_Button=(.*?)\n', user_agent_read, re.S))
                    user_agent_search = 'User-Agent_Button=' + user_agent_customize.strip()
                    user_agent_replace_content = 'User-Agent_Button=False'  # 要替换的文本
                    replace_content(user_agent_search, user_agent_replace_content, crawler_settings_log)

        t_user_agent = threading.Thread(target=t_user_agent)
        t_user_agent.setDaemon(True)
        t_user_agent.start()



