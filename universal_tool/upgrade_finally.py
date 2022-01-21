import threading
import time
import zipfile,requests,getpass,shutil,os
import tkinter
import public


response = requests.get("https://api.github.com/repos/ld596044192/DA_Tools/releases/latest")
version = response.json()["tag_name"]
users = getpass.getuser()
dir_path = 'C:\\Users\\' + users + '\\Documents\\little_tools(DA)'
install_path = dir_path + '\\install.log'
install_read = open(install_path, 'r').read()
LOGO_path = public.resource_path(os.path.join('icon', 'my-da.ico'))


class Upgrade(object):
    def upgrade_form(s):
        s.upgrade_root = tkinter.Tk()
        s.upgrade_root.title('更新程序后台V1.0.0 tktiner版')
        screenWidth = s.upgrade_root.winfo_screenwidth()
        screenHeight = s.upgrade_root.winfo_screenheight()
        w = 350
        h = 50
        x = (screenWidth - w) / 2
        y = (screenHeight - h) / 2
        s.upgrade_root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        s.upgrade_root.resizable(0, 0)
        s.upgrade_root.iconbitmap(LOGO_path)
        s.upgrade_root.wm_attributes('-topmost', 1)
        s.main_form()
        s.upgrade_root.mainloop()

    def main_form(s):
        s.label_str = tkinter.StringVar()
        s.text_label = tkinter.Label(s.upgrade_root,textvariable=s.label_str,bg='black',fg='#ffffff',width=40,height=2)
        s.text_label.config(command=s.main())
        s.text_label.place(x=35,y=5)

    def main(s):
        def download():
            s.label_str.set('正在启动 更新程序后台安装..')
            time.sleep(1)
            s.label_str.set('本次安装涉及更新程序更新，所以采取后台进行更新')
            time.sleep(1)
            s.label_str.set('等待3s后开始解压安装...')
            time.sleep(3)

            try:
                # 删除更新文件夹
                shutil.rmtree(install_read + '/upgrade')
                shutil.rmtree(install_read + '/version')
                shutil.rmtree(install_read + '/icon')
                shutil.rmtree(install_read + '/background_program')
                os.remove(install_read + '/main.exe')
            except FileNotFoundError:
                pass

            s.label_str.set('正在解压安装...')

            install_zip = zipfile.ZipFile(install_read + "/喝水提醒小工具" + version + ".zip", 'r')
            for file in install_zip.namelist():
                install_zip.extract(file, install_read)
            install_zip.close()

            os.remove(install_read + "/喝水提醒小工具" + version + ".zip")

            time.sleep(1)
            s.label_str.set('安装完毕，自行重启程序即是最新版本！')

        t = threading.Thread(target=download)
        t.setDaemon(True)
        t.start()


if __name__ == '__main__':
    upgrade_form = Upgrade()
    upgrade_form.upgrade_form()