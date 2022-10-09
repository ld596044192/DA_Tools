# 这是爬虫程序通用设置
import getpass,os.path
import tkinter
import public

username = getpass.getuser()
# 创建临时文件夹
make_dir = 'C:\\Users\\' + username + '\\Documents\\ADB_Tools(DA)\\'
# 进入某功能需要实时监测功能是否已经启动
crawler_settings = make_dir + 'crawler_settings\\'
crawler_settings_log = crawler_settings + 'crawler_settings.ini'
crawler_page = crawler_settings + 'crawler_page'
# 初始化文件
if not os.path.exists(crawler_settings):
    os.makedirs(crawler_settings)
if not os.path.exists(crawler_settings_log):
    with open(crawler_settings_log,'w') as fp:
        fp.write('')
    fp.close()
setting_logo = public.resource_path(os.path.join('icon', 'crawler_settings.ico'))


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

    def setting_startup(self,general_params_button,general_params_button_disable):
        # 监听截图页面的打开状态
        crawler_exists = self.crawler_setting_root.winfo_exists()
        print(crawler_exists)
        if crawler_exists == 1:
            general_params_button.place_forget()
            general_params_button_disable.place(x=500, y=0)

    def close_handle(self):
        # 监听页面消失
        with open(crawler_page,'w') as fp:
            fp.write('0')
        fp.close()
        self.crawler_setting_root.destroy()

    def main_frame(self):
        pass



