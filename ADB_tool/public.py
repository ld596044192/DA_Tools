import ctypes,inspect
import sys,os
import subprocess
import psutil,shutil
import re
from tkinter import *


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
    devices_split = ''.join(devices_re).split(' ')
    devices_finally = [i for i in devices_split if i != '']  # 去空
    return devices_finally


def found_packages():
    # 查找当前包名
    package_cmd = execute_cmd('adb shell dumpsys window | findstr mCurrentFocus')
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
        print('不存在该进程，继续执行！')
    return Processes


def device_type_android():
    # 检测安卓方法
    device_type = execute_cmd('adb shell getprop net.bt.name')
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




