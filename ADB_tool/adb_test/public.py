import ctypes,inspect
import sys,os
import subprocess,windnd
import tkinter,tkinter.messagebox
import psutil,shutil,getpass,pyperclip,hashlib
import re,time
from tkinter import *
import zipfile
from PIL import Image, ImageSequence
import random  # 随机模块

username = getpass.getuser()
# 创建临时文件夹
make_dir = 'C:\\Users\\' + username + '\\Documents\\ADB_Tools(DA)\\'
conflict_software_path = make_dir + 'conflict_software.txt'
# 记录设置环境变量日志
environ_log = make_dir + 'environ_log.log'
# 记录apk包路径（检测包名）
apk_path_package_log = make_dir + 'apk_path_package.log'
# 简易ADB - adb-tools检测标志
adb_tools_flag = make_dir + 'adb-tools'
# 创建页面文件，记录文件状态
make_dir_s = make_dir + 'make_dir\\'
# 修改gif图片产生的缓存
make_gif_temp = make_dir + 'gif_temp\\'
if not os.path.exists(make_dir_s):
    os.makedirs(make_dir_s)
gif_playerGif_path = make_dir + 'playerGif_temp\\'
# 首次启动需要删除存在的gif缓存
try:
    shutil.rmtree(gif_playerGif_path)
except (FileNotFoundError,OSError):
    pass


def resource_path(relative_path):
    """生成资源文件目录访问路径"""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)


# 获取包名所有信息
package_log_path = resource_path(os.path.join('temp','package_log.txt'))
packages_name = resource_path(os.path.join('temp','packages_name.log'))


def _async_raise(tid, exctype):
    """Raises an exception in the threads with id tid"""
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    # 终止进程
    _async_raise(thread.ident, SystemExit)


def execute_cmd(cmd):
    proc = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,stdin=subprocess.PIPE)
    proc.stdin.close()
    proc.wait()
    try:
        result = proc.stdout.read().decode('gbk')  # 注意你电脑cmd的输出编码（中文是gbk）
    except UnicodeDecodeError:
        result = proc.stdout.read().decode('utf-8')  # 适用于截图录屏功能，针对截图录屏文件名中文编码报错的异常处理
    proc.stdout.close()
    return result


def cmd_editor_disable():
    """
    定义一个禁止cmd的快速编辑模式，防止程序挂起不执行（仅限cmd控制台或后台程序使用）
    :return:
    """
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 128)


def get_pid(name):
    '''
     作用：根据进程名获取进程pid
    '''
    pids = psutil.process_iter()
    print("[" + name + "]'s pid is:")
    for pid in pids:
        if(pid.name() == name) and pid != None:
            print(pid.pid)


def device_connect():
    # 检查设备连接情况
    devices_fp = execute_cmd('adb devices')
    devices_re = re.findall('\\n(.*?)\\sdevice', devices_fp)
    # devices_split = ''.join(devices_re).split(' ')
    # devices_finally = [i for i in devices_split if i != '']  # 去空
    # print(devices_re)  # 调试设备连接状态以及设备序列号信息
    return devices_re


def adb_version():
    # 检测ADB调试桥版本
    adb_version_str = execute_cmd('adb version')
    print(adb_version_str)
    adb_version_re = re.findall('Android Debug Bridge version (.*?)\\r\\n',adb_version_str)
    adb_version_finally = ''.join(''.join(adb_version_re).split('.'))
    print('Android Debug Bridge version code: ' + adb_version_finally)
    return adb_version_finally


def found_packages(device):
    # 查找当前包名
    try:
        # 旧方法
        # package_cmd = execute_cmd('adb -s ' + device + ' shell dumpsys window | findstr mCurrentFocus')
        # package_name = package_cmd.split()[(-1)].split('/')[0]
        # 新方法，使用正则匹配更精确
        execute_cmd('adb -s ' + device + ' shell dumpsys window > ' + packages_name)
        package_log = open(packages_name,'r',errors='ignore').read()
        package_name = ''.join(re.findall('mCurrentFocus.*?(com.*?)/.*?}', package_log, re.S))
        # print(package_name)
        return package_name
    except IndexError:
        print('未连接设备，请连接设备后再尝试！！！')


def adb_connect():
    # 检测本地是否有adb服务
    adb_service = execute_cmd('adb version')
    adb_list = adb_service.split()
    return adb_list


def get_pid_name():
    # 获取进程名
    Processes = []
    pids = psutil.pids()
    try:
        for pid in pids:
            pid_names = psutil.Process(pid).name()
            # 获取所有进程名称并添加到列表中
            Processes.append(pid_names)
    except psutil.NoSuchProcess:
        # print('不存在该进程，继续执行！')
        pass
    return Processes


def device_type_android(device):
    # 检测安卓方法
    device_type = execute_cmd('adb -s ' + device + ' shell getprop net.bt.name').strip()
    # print(device_type)  # 调试
    return device_type


# 当鼠标移动到指定控件时，进行文字提醒的控件
class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    # 当光标移动指定控件是显示消息
    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx()+15
        y = y + cy + self.widget.winfo_rooty()+25
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text,justify=LEFT,
                      background="Yellow", relief=SOLID, borderwidth=1,
                      font=("微软雅黑", "10"))
        label.pack(side=BOTTOM)

    # 当光标移开时提示消息隐藏
    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

# 气泡提示的函数（可调用）
"""
第一个参数：是定义的控件的名称
第二个参数，是要显示的文字信息
"""
def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)

    def enter(event):
        toolTip.showtip(text)

    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


def reset_delete(filename):
    # 通用重置删除文件
    if os.path.exists(filename):
        # 判断文件是否为文件夹或文件
        if os.path.isdir(filename):
            # shutil.rmtree只删除文件夹
            shutil.rmtree(filename)
            print(filename + ' 已删除！')
        else:
            try:
                # os.remove只删除文件
                os.remove(filename)
            except PermissionError:
                # 遇到 另一个程序正在使用此文件，进程无法访问 导致无法删除文件的权限问题，下面利用cmd强制删除文件命令进行删除
                execute_cmd('del /F /S /Q ' + filename)
            print(filename + ' 已删除！')


def reset_method(filename_list):
    # 重置功能需要调用的方法
    # filename_list 需要删除的文件名称列表
    for filename in filename_list:
        reset_delete(filename)


# 右键菜单绑定事件
# 剪切功能的实现
def cut(editor_list, event=None):
    for editor in editor_list:
        editor.event_generate("<<Cut>>")


# 复制功能的实现
def copy(editor_list, event=None):
    for editor in editor_list:
        editor.event_generate("<<Copy>>")


# 获取当前路径中的所有文件夹
def get_dirs(path):  # 获取所有文件
    all_file = []
    for f in os.listdir(path):  # listdir返回文件中所有目录
        f_name = os.path.join(path, f)
        all_file.append(f_name)
    return all_file


# 获取当前路径中的所有文件
def get_files(file_dir):
    for root, dirs, files in os.walk(file_dir):
        if files:
            # print(root)  # 当前目录路径
            # print(dirs)  # 当前路径下所有子目录
            print(files)   # 当前路径下所有非目录子文件

            return files


def linux_only_read(device):
    # 检测只读权限 - 适用于Linux系统
    check_only_read = execute_cmd('adb -s ' + device + ' shell ls -lh /data/.overlay')
    only_read = ' '.join(check_only_read.split()).split(':')[-1]
    print(only_read)
    return only_read


def temporary_environ(path_value):
    # 临时配置环境变量
    os.environ["PATH"] += ";" + path_value
    # 查看已配置的环境变量
    print(os.environ["PATH"])


def permanent_environ(path_value):
    # 永久配置环境变量（添加到Path中）
    environ_list = os.environ["PATH"].split(';')
    # 过滤，模糊匹配
    try:
        grep_list = ''.join([x for x in environ_list if x.find('/m') != -1])
        environ_list.remove(grep_list)
    except ValueError:
        print('无需过滤环境变量')
    environ_list_finally = environ_list
    print('已过滤的环境变量列表：\n' + str(environ_list_finally))
    with open(environ_log, 'a+') as fp:
        fp.write('已过滤的环境变量列表：\n' + str(environ_list_finally))
    fp.close()
    new_environ = ';'.join(environ_list_finally)

    # /m代表系统变量。 不加 /m为用户变量
    command = r'setx "Path" ' + '"' + path_value + ';' + new_environ + '"' + ' /m'
    print(command)
    result = execute_cmd(command)
    print(result)
    with open(environ_log,'a+') as fp:
        fp.write('最终设置的环境变量列表：\n' + command + '\n' + result)
    fp.close()


def remove_environ(path_value):
    # 删除指定的环境变量
    environ_list = os.environ["PATH"].split(';')
    print('旧环境变量列表:\n' + str(environ_list))
    while True:
        if path_value in environ_list:
            environ_list.remove(path_value)
        else:
            break

    # 过滤，模糊匹配
    try:
        grep_list = ''.join([x for x in environ_list if x.find('/m') != -1])
        environ_list.remove(grep_list)
    except ValueError:
        print('无需过滤环境变量')
    environ_list_finally = environ_list
    print('已过滤的环境变量列表：\n' + str(environ_list_finally))
    with open(environ_log,'a+') as fp:
        fp.write('已过滤的环境变量列表：\n' + str(environ_list_finally))
    fp.close()
    new_environ = ';'.join(environ_list_finally)

    print('新环境变量内容:\n' + str(new_environ))
    return new_environ


def zip_extract(zip_path,zip_target_path):
    # 解压zip文件
    zip_f = zipfile.ZipFile(zip_path)
    list_zip_f = zip_f.namelist()  # zip文件中的文件列表名
    for zip_fn in list_zip_f:
        zip_f.extract(zip_fn, zip_target_path)  # 第二个参数指定输出目录
        print("%s done" % zip_fn)
    zip_f.close()


# 检验字符串是否含有中文字符
def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False


def wifi_mac_result(device):
    # 获取WIFI MAC地址
    wifi_mac_result = os.popen('adb -s ' + device + ' shell ip addr show wlan0', 'r').read().replace('\n\n', '\n')
    wifi_mac = ''.join(re.findall('link/ether(.*?)brd', wifi_mac_result)).strip()
    # print(wifi_mac)
    return wifi_mac


def devices_ip_result(device):
    # 获取设备ip地址
    devices_ip_result = os.popen('adb -s ' + device + ' shell ifconfig wlan0', 'r').read().replace('\n\n', '\n')
    devices_ip = ''.join(re.findall('inet addr:(.*?)Bcast', devices_ip_result)).strip()
    return devices_ip


def android_software_version_result(device):
    # 获取设备应用版本
    # 管道符命令获取方式（虽一步到位，但会弹出命令行窗口）
    # package_name = found_packages(device)
    # software_version_result = subprocess.Popen(('adb -s ' + device + ' shell dumpsys package ' + package_name),stdout=subprocess.PIPE)
    # output = subprocess.check_output(('findstr version'),stdin=software_version_result.stdout).decode('utf-8')
    # software_version_result.wait()
    # # print(output)
    # software_version = re.findall('versionName=(.*?)\s',output)[0]
    # software_version_result.stdout.close()
    # # print(devices_version)
    # 正则表达式获取（不会弹出命令行窗口）
    package_name = found_packages(device)
    # print(package_name)
    execute_cmd('adb -s ' + device + ' shell dumpsys package ' + package_name + '> ' + package_log_path)
    package_result_content = open(package_log_path,'r',encoding='utf-8').read()
    software_version_re = re.findall('Packages.*?versionName=(.*?)\n',package_result_content, re.S)
    software_version = ''.join(software_version_re)
    # print(software_version)
    return software_version


def android_firmware_version_result(device):
    # 获取设备固件版本
    firmware_version = execute_cmd('adb -s ' + device + ' shell getprop ro.build.display.id').strip()
    return firmware_version


def find_pid_name(software_name_list):
    # 查找软件是否已打开
    software_name_flag = False
    Processes = get_pid_name()
    # print(Processes)
    for software_name in software_name_list:
        if software_name in Processes:
            # print('已发现目标软件 ' + software_name)
            with open(conflict_software_path,'w') as fp:
                fp.write(software_name)
            fp.close()
            software_name_flag = True
            break
        else:
            software_name_flag = False
    return software_name_flag


def windnd_hook_files(widget,widget_str):
    # 拖拽文件到entry文本框获取文件路径功能（windnd） widget是控件 widget_str是显示文件路径
    def dragged_files(files):
        # 获取文件路径
        widget_str.set('')
        path_msg = '\n'.join((item.decode('gbk') for item in files))
        print('获取的文件路径：' + path_msg)
        with open(apk_path_package_log,'w') as fp:
            fp.write(path_msg)
        fp.close()
        widget.insert(tkinter.END,path_msg)

    # 使用windnd方法
    windnd.hook_dropfiles(widget,func=dragged_files)


def upgrade_adb():
    # 直接更换本工具最新的adb
    # 需要时间停掉所有ADB的行为
    time.sleep(5)
    execute_cmd('adb kill-server')  # 关闭ADB服务
    try:
        shutil.rmtree(adb_tools_flag)  # 删除旧版本ADB文件
    except FileNotFoundError:
        print('没有该文件无需删除！！！')
    adb_path = resource_path(os.path.join('resources', 'adb-tools.zip'))
    shutil.copy(adb_path, make_dir)
    # 解压
    zip_path = make_dir + 'adb-tools.zip'
    zip_extract(zip_path, make_dir)
    # 清理压缩包
    os.remove(zip_path)
    # 打印测试
    print('更新完成！！！')


def pyperclip_copy_paste(content):
    # 通用复制粘贴
    pyperclip.copy(content)
    # 从剪贴板那粘贴
    pyperclip.paste()
    tkinter.messagebox.showinfo('粘贴提醒','已复制粘贴\n' + content + '\n到剪贴板\n温馨提示：可以Ctrl+V粘贴到任意地方啦~')


def flow_page():
    # 创建查询应用流量值页面
    flow_page = make_dir_s + 'flow_page.txt'
    return flow_page


def file_md5(file_path):
    # 获取文件MD5
    with open(file_path, 'rb') as fp:
        data = fp.read()
    file_md5 = hashlib.md5(data).hexdigest().upper()  # 32位大写
    fp.close()
    print('已获取当前文件md5值：' + file_md5)
    return file_md5


def bigger_file_md5(file_path):
    # 计算大文件md5，防止整个大文件读入内存导致爆内存
    # 将文件分成 8192 字节的块（或其他一些 128 字节的倍数）并使用update().
    # 这利用了 MD5 具有 128 字节摘要块（8192 是 128×64）的事实。由于您没有将整个文件读入内存，因此这不会使用超过 8192 字节的内存。
    # 如果目录下有文件过大，则会消耗很久时间
    with open(file_path, "rb") as f:
        file_hash = hashlib.md5()
        while chunk := f.read(8192):  # := 为海象运算符，类似于“=”等于，python 3.8+ 才会有，代码缩短运算速度更快
            file_hash.update(chunk)
    file_md5 = file_hash.hexdigest().upper()
    f.close()
    print('已获取当前文件md5值：' + file_md5)
    return file_md5


def gif_size_revise(photo_path,gif_width,gif_height,photo_path_new):
    # 修改gif图片的尺寸大小
    oriGif = Image.open(photo_path)
    lifeTime = oriGif.info['duration']
    imgList = []
    imgNew = []
    if not os.path.exists(make_gif_temp):
        os.makedirs(make_gif_temp)
    for i in ImageSequence.Iterator(oriGif):
        # print(i.copy())
        imgList.append(i.copy())
    for index, f in enumerate(imgList):
        f.save(make_gif_temp + "%d.png" % index)  # 将gif的每一帧取出，保存成一张张图片，这里用png格式(也可以用jpg但是jpg需要转换一次)
        img = Image.open(make_gif_temp + "%d.png" % index)
        img.thumbnail((gif_width, gif_height), Image.ANTIALIAS)  # 修改每帧图片的尺寸大小
        imgNew.append(img)
    # 将每帧图片修改尺寸后，再次合成gif
    imgNew[0].save(photo_path_new, 'gif', save_all=True, append_images=imgNew[1:], loop=0,
                   duration=lifeTime)
    # 删除缓存文件
    shutil.rmtree(make_gif_temp)


def not_gif_revise(photo_path,gif_width,gif_height,photo_path_new):
    # 修改非gif图片的尺寸大小
    '''
    photo_path: 输入图片
    photo_path_new: 输出图片
    gif_width: 输出图片宽度
    gif_height:输出图片高度
    type:输出图片类型（png, gif, jpeg...）
    '''

    def ResizeImage(filein, fileout, width, height, file_type):
        img = Image.open(filein)
        out = img.resize((width, height), Image.ANTIALIAS)  # resize image with high-quality
        out.save(fileout, file_type)

    file_type = 'png'  # 默认输出png图片
    ResizeImage(photo_path, photo_path_new,gif_width,gif_height, file_type)


STR_FRAME_FILENAME = "frame{}.png"  # 每帧图片的文件名格式


class playGif():
    # 实现gif动态图的动态播放
    def __init__(self, file, temporary=gif_playerGif_path):  # temporary 指临时目录路径，为空时则随机生成
        self.__strPath = file
        self.__index = 1  # 当前显示图片的帧数

        if len(temporary) == 0:
            self.strTemporaryFolder = self.crearteTemporaryFolder()  # 随机得到临时目录
        else:
            self.strTemporaryFolder = temporary  # 指定的临时目录

        self.__intCount = 0  # gif 文件的帧数

        try:
            self.decomposePics()  # 开始分解
        except (FileNotFoundError,FileExistsError):
            pass

    def crearteTemporaryFolder(self):  # 生成临时目录名返回
        # 获取当前调用模块主程序的运行目录
        strSelfPath = str(os.path.dirname(os.path.realpath(sys.argv[0])))
        if len(strSelfPath) == 0:
            strSelfPath = os.path.join(os.getcwd())

        def createRandomFolder(strSelfPath):  # 内嵌方法，生成随机目录用
            length = random.randint(5, 10)  # 随机长度
            path = ""
            for i in range(length):
                path = path + chr(random.randint(97, 122))  # 随机生成a-z字母

            return os.path.join(strSelfPath, path)

        # 获取当前软件目录
        folder = createRandomFolder(strSelfPath)
        while os.path.isdir(folder):  # 已存在
            folder = createRandomFolder(strSelfPath)
        return folder

    def decomposePics(self):  # 分解 gif 文件的每一帧到独立的图片文件，存在临时目录中
        i = 0
        img = Image.open(self.__strPath)
        self.__width, self.__height = img.size  # 得到图片的尺寸

        os.mkdir(self.strTemporaryFolder)  # 创建临时目录
        for frame in ImageSequence.Iterator(img):  # 遍历每帧图片
            frame.save(os.path.join(self.strTemporaryFolder, STR_FRAME_FILENAME.format(i + 1)))  # 保存独立图片
            i += 1

        self.__intCount = i  # 得到 gif 的帧数

    def getPicture(self, frame=0):  # 返回第 frame 帧的图片(width=0,height=0)
        if frame == 0:
            frame = self.__index
        elif frame >= self.__intCount:
            frame = self.__intCount  # 最后一张

        img = tkinter.PhotoImage(file=os.path.join(self.strTemporaryFolder, STR_FRAME_FILENAME.format(frame)))
        self.__index = self.getNextFrameIndex()

        return img  # 返回图片

    def getNextFrameIndex(self, frame=0):  # 返回下一张的帧数序号
        if frame == 0:
            frame = self.__index  # 按当前插入帧数

        if frame == self.__intCount:
            return 1  # 返回第1张，即从新开始播放
        else:
            return frame + 1  # 下一张

    def playGif(self, tk, widget, time=100):  # 开始调用自身实现播放，time 单位为毫秒
        try:
            img = self.getPicture()
            widget.config(image=img)
            widget.image = img
            gif_files = len(os.listdir(gif_playerGif_path))  # 获取临时文件数量
            if gif_files < 100:
                time = 100
            else:
                time = 30
            tk.after(time, self.playGif, tk, widget, time)  # 在 time 时间后调用自身
        except tkinter.TclError:
            self.close()
            pass

    def close(self):  # 关闭动画文件，删除临时文件及目录
        try:
            files = os.listdir(self.strTemporaryFolder)
            for file in files:
                os.remove(os.path.join(self.strTemporaryFolder, file))
            os.rmdir(self.strTemporaryFolder)
        except FileNotFoundError:
            pass

    def stop(self,widget):
        widget.place_forget()


def md5_size_page():
    # 创建获取文件MD5和大小页面
    md5_size_page = make_dir_s + 'md5_size_page.txt'
    return md5_size_page