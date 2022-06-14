import ctypes,inspect
import sys,os
import subprocess
import time

import psutil,shutil,getpass
import re
from tkinter import *
import zipfile

username = getpass.getuser()
# 创建临时文件夹
make_dir = 'C:\\Users\\' + username + '\\Documents\\ADB_Tools(DA)\\'
conflict_software_path = make_dir + 'conflict_software.txt'


def resource_path(relative_path):
    """生成资源文件目录访问路径"""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)


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
        if(pid.name() == name):
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
    adb_version_re = re.findall('Android Debug Bridge version (.*?)\\r\\n',adb_version_str)
    adb_version_finally = ''.join(''.join(adb_version_re).split('.'))
    print('Android Debug Bridge version code: ' + adb_version_finally)
    return adb_version_finally


def found_packages(device):
    # 查找当前包名
    package_cmd = execute_cmd('adb -s ' + device + ' shell dumpsys window | findstr mCurrentFocus')
    package_name = package_cmd.split()[(-1)].split('/')[0]
    return package_name


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
    device_type = execute_cmd('adb -s ' + device + ' shell getprop net.bt.name')
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
    # /m代表系统变量。 不加 /m为用户变量
    command = r'setx "Path" ' + '"' + path_value + ';%path%" /m'
    print(command)
    result = execute_cmd(command)
    print(result)


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
    print(wifi_mac)
    return wifi_mac


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
            software_name_flag = True
            break
        else:
            software_name_flag = False
    return software_name_flag
