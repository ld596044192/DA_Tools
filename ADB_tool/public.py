import ctypes,inspect
import sys,os
import subprocess
import psutil
import re


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

