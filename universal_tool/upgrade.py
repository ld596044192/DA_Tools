# 该py程序需要单独打包成一个exe升级程序供主程序调用，放进upgrade文件夹即可
import shutil
import signal
import threading
import tkinter
import public,os,getpass,sys,ctypes,win32api
import requests,socket,urllib3
import time
from tqdm import tqdm
import tkinter.ttk
import zipfile

LOGO_path = public.resource_path(os.path.join('icon', 'my-da.ico'))
version_new_path = public.resource_path(os.path.join('version', 'version_new.txt'))
download_path = public.resource_path(os.path.join('temp', 'download_percent.log'))
upgrade_path = public.resource_path(os.path.join('upgrade_finally', 'upgrade_finally.exe'))
users = getpass.getuser()
dir_path = 'C:\\Users\\' + users + '\\Documents\\little_tools(DA)'
download_thread = dir_path + '\\download_thread.log'
install_path = dir_path + '\\install.log'
pid_path = dir_path + '\\pid.log'
# 查看github最新版本
response = requests.get("https://api.github.com/repos/ld596044192/DA_Tools/releases/latest")
version = response.json()["tag_name"]

install_read = open(install_path, 'r').read()
if not os.path.exists(download_thread):
    with open(download_thread,'w') as fp:
        fp.write('')


class Upgrade(object):
    def upgrade_form(s):
        s.upgrade_root = tkinter.Tk()
        s.upgrade_root.title('达之领域通用更新程序V1.0.0 tktiner版')
        screenWidth = s.upgrade_root.winfo_screenwidth()
        screenHeight = s.upgrade_root.winfo_screenheight()
        w = 400
        h = 300
        x = (screenWidth - w) / 2
        y = (screenHeight - h) / 2
        s.upgrade_root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        s.upgrade_root.iconbitmap(LOGO_path)
        s.upgrade_root.resizable(0, 0)
        s.upgrade_root.wm_attributes('-topmost', 1)
        # s.root.protocol('WM_DELETE_WINDOW', s.close_handle)
        s.author_frame()
        s.version_upgrade_frame()
        s.version_main()
        s.upgrade_root.mainloop()

    def version_upgrade_frame(s):
        # 历史版本信息窗口
        s.upgrade_frame = tkinter.Frame(s.upgrade_root)
        s.scrollbar = tkinter.Scrollbar(s.upgrade_frame)
        s.upgrade_listbox = tkinter.Listbox(s.upgrade_frame, width=54, height=9,yscrollcommand=(s.scrollbar.set))
        s.upgrade_listbox.bindtags((s.upgrade_listbox,'all'))
        s.scrollbar.config(command=(s.upgrade_listbox.yview))
        s.scrollbar.pack(side=(tkinter.RIGHT),fill=(tkinter.Y))
        s.upgrade_listbox.pack()
        s.upgrade_frame.place(y=80)

    def author_frame(s):
        s.upgrade_button = tkinter.Button(s.upgrade_root,text='立即更新',width=10)
        s.upgrade_button.place(x=165,y=10)
        s.upgrade_button.bind('<Button-1>',lambda x:s.upgrade_main())
        s.upgrade_button_disable = tkinter.Button(s.upgrade_root, text='正在更新中...', width=10)
        s.upgrade_button_disable.config(state='disable')

        s.upgrade_i = tkinter.StringVar()
        s.upgrade_number = tkinter.Label(s.upgrade_root,textvariable=s.upgrade_i,bg='white',width=5,height=1,font=("华文楷体",20))
        s.upgrade_i.set('0%')

        s.upgrade_k = tkinter.StringVar()
        s.upgrade_speed = tkinter.Label(s.upgrade_root, textvariable=s.upgrade_k, bg='white', width=8, height=1,
                                         font=("华文楷体", 20))
        s.upgrade_k.set('0k/s')

        s.progressbarOne = tkinter.ttk.Progressbar(s.upgrade_root, length=350)
        s.progressbarOne['maximum'] = 100
        s.progressbarOne['value'] = 0
        s.progressbarOne.place(x=25,y=48)

        s.author_label = tkinter.Label(s.upgrade_root, text='达之领域', font=("华文行楷", 40), fg='red')
        s.author_label.place(x=90,y=245)

    def requests_response(s):
        # 设置备用下载线路，下载失败后切换备用线路继续下载
        download_id = open(download_thread, 'r').read()
        if download_id == '':
            codex_website = 'https://hub.fastgit.org/'
            download_url = codex_website + "ld596044192/DA_Tools/releases/download/" + version + "/main.zip"
            return download_url
        elif download_id == '1':
            codex_website = 'https://github.com.cnpmjs.org/'
            download_url = codex_website + "ld596044192/DA_Tools/releases/download/" + version + "/main.zip"
            return download_url
        elif download_id == '2':
            codex_website = 'https://github.com/'
            download_url = codex_website + "ld596044192/DA_Tools/releases/download/" + version + "/main.zip"
            return download_url

    def version_main(s):
        def version_request():
            try:
                s.upgrade_listbox.insert(tkinter.END,version + '新版本特性及更新内容:')

                version_info = response.json()["body"]
                # 保存更新内容
                with open(version_new_path,'w') as fp:
                    fp.write(version_info)
                version_size = int(response.json()["assets"][0]["size"]) / 1024 / 1024
                # 处理版本更新内容格式
                version_new = open(version_new_path,'r').readlines()
                for version_info in version_new:
                    if version_info == '\n':
                        # 去掉空行
                        version_info.strip('\n')
                    else:
                        s.upgrade_listbox.insert(tkinter.END,version_info)

                s.upgrade_listbox.insert(tkinter.END,'更新文件大小为' + str("%.2f " % version_size) + 'MB')
                s.upgrade_listbox.see(tkinter.END)
            except ValueError:
                s.upgrade_listbox.insert(tkinter.END,'检测到你启动了代理或翻墙工具，请关闭后再继续更新！')
                s.upgrade_listbox.see(tkinter.END)
            except (socket.gaierror, urllib3.exceptions.NewConnectionError, urllib3.exceptions.MaxRetryError,
                    requests.exceptions.ConnectionError):
                s.upgrade_listbox.insert(tkinter.END,'检测更新失败，网络连接正常后再试！')
                s.upgrade_listbox.see(tkinter.END)
                sys.exit()

        t = threading.Thread(target=version_request)
        t.setDaemon(True)
        t.start()

    def upgrade_main(s):
        def upgrade():
            s.upgrade_button_disable.place(x=165,y=10)
            s.upgrade_number.place(x=30, y=5)
            s.upgrade_speed.place(x=260, y=5)
            s.upgrade_i.set('0%')
            s.upgrade_listbox.insert(tkinter.END,'软件正在更新中...')
            s.upgrade_listbox.see(tkinter.END)
            i = 1
            while True:
                try:
                    install_path = os.getcwd()
                    install_path_split = install_path.split(':')[0]
                    if install_path_split == 'C':
                        os.chdir('C:\\Users\\' + users + '\\Desktop')
                    else:
                        os.chdir(install_read)
                    download_url = s.requests_response()
                    # print('手动更新:如果自动更新速度很慢，可以复制下面的下载地址到浏览器打开即可！')
                    # print(download_url + '\n')
                    response3 = requests.get(url=download_url, timeout=10, stream=True)

                    content_size = int(response3.headers['Content-Length']) / 1024
                    with open("喝水提醒小工具" + version + ".zip", "wb") as f:
                        s.upgrade_listbox.insert(tkinter.END,"文件大小为: " + str(content_size) + 'k,正在开始下载...')
                        s.upgrade_listbox.see(tkinter.END)
                        upgrade_files = tqdm(iterable=response3.iter_content(1024), total=content_size, unit='k',
                                         desc="喝水提醒小工具" + version + ".zip")
                        for data in upgrade_files:
                            percent = open(download_path,'w')
                            print(upgrade_files,file=percent)
                            percent_read = open(download_path,'r').read()
                            # s.upgrade_listbox.insert(tkinter.END,upgrade_files)
                            # s.upgrade_listbox.see(tkinter.END)
                            # 获取进度百分比
                            d = percent_read.split('|')[0].split(':')[-1].split(' ')[-1].split('%')[0]
                            # 获取每秒下载速度
                            k = percent_read.split('[')[-1].split(']')[0].split(',')[-1].split(' ')[-1]
                            # 防止数值为空需要加判断
                            if d != '':
                                s.progressbarOne['value'] = int(d)
                                s.upgrade_i.set(d + '%')
                                s.upgrade_k.set(k)
                            f.write(data)

                        s.progressbarOne['value'] = 100
                        s.upgrade_button_disable.place_forget()
                        s.upgrade_listbox.insert(tkinter.END,"喝水提醒小工具" + version + ".zip" + " 下载成功!")
                        s.upgrade_listbox.see(tkinter.END)
                        # s.upgrade_listbox.insert(tkinter.END,'安装包下载保存位置:')
                        # s.upgrade_listbox.see(tkinter.END)
                        # s.upgrade_listbox.insert(tkinter.END, install_path + '\\喝水提醒小工具' + version + ".zip")
                        # s.upgrade_listbox.see(tkinter.END)
                        break
                except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError,
                        requests.exceptions.ReadTimeout):
                    s.upgrade_listbox.insert(tkinter.END,'第' + str(i) + '次正在重连，请耐心等待...')
                    s.upgrade_listbox.see(tkinter.END)
                    if i == 1:
                        with open(download_thread, 'w') as fp:
                            fp.write('1')
                    elif i == 2:
                        with open(download_thread, 'w') as fp:
                            fp.write('2')
                    s.upgrade_listbox.insert(tkinter.END,'正在启用备用下载线路...')
                    s.progressbarOne['value'] = 0
                    s.upgrade_listbox.see(tkinter.END)
                    i += 1
                    time.sleep(1)
                # except ValueError:
                #     s.upgrade_listbox.insert(tkinter.END,'检测到你启动了代理或翻墙工具，请关闭后再继续更新！')
                #     continue
                if i > 10:
                    s.upgrade_listbox.insert(tkinter.END,'下载更新失败，网络连接成功后再试！')
                    s.upgrade_listbox.see(tkinter.END)
                    s.upgrade_button_disable.place_forget()
                    sys.exit()
            s.install_file()

        t_upgrade = threading.Thread(target=upgrade)
        t_upgrade.setDaemon(True)
        t_upgrade.start()

    def install_file(s):
        # 解压安装
        try:
            pid_read = open(pid_path,'r').read()
            s.upgrade_listbox.insert(tkinter.END,'正在强制关闭程序...')
            s.upgrade_listbox.see(tkinter.END)
            os.kill(int(pid_read),signal.SIGINT)
            # public.execute_cmd('taskkill.exe /pid:' + pid_read)
            time.sleep(1)
            s.upgrade_listbox.insert(tkinter.END, '程序已关闭!')
        except OSError:
            print('程序没有启动或已关闭，无需关闭！')
            pass
        s.upgrade_listbox.insert(tkinter.END, '正在解压安装（静默安装）...')
        s.upgrade_listbox.see(tkinter.END)

        try:
            # 删除旧文件
            shutil.rmtree(install_read + '/version')
            shutil.rmtree(install_read + '/icon')
            shutil.rmtree(install_read + '/background_program')
            os.remove(install_read + '/main.exe')
        except FileNotFoundError:
            pass

        # 解压新版文件
        time.sleep(1)
        install_zip = zipfile.ZipFile(install_read + "/喝水提醒小工具" + version + ".zip", 'r')
        for file in install_zip.namelist():
            if file == 'upgrade/' or file == 'upgrade/upgrade.exe':
                s.upgrade_listbox.insert(tkinter.END, '检测到更新程序升级，正式转为后台运行...')
                s.upgrade_listbox.see(tkinter.END)
                time.sleep(1)
                # public.execute_cmd(upgrade_path)
                win32api.ShellExecute(0, 'open', upgrade_path, '', '', 1)
                time.sleep(1)
                pid = os.getpid()
                os.kill(pid,signal.SIGINT)
                sys.exit()
            else:
                install_zip.extract(file, install_read)
        install_zip.close()

        os.remove(install_read + "/喝水提醒小工具" + version + ".zip")
        s.upgrade_listbox.insert(tkinter.END, '安装完毕，自行重启程序即是最新版本！')
        s.upgrade_listbox.see(tkinter.END)


if __name__ == '__main__':
    upgrade_form = Upgrade()
    upgrade_form.upgrade_form()

# def run_program():
#     upgrade_form = Upgrade()
#
#     def is_admin():
#         try:
#             return ctypes.windll.shell32.IsUserAnAdmin()
#         except:
#             return False
#
#     if is_admin():
#         upgrade_form.upgrade_form()
#     else:
#         ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, __file__, None, 1)
#
#
# if __name__ == '__main__':
#     run_program()