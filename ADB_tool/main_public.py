import sys,os,inspect,ctypes,getpass,re

username = getpass.getuser()
# 创建临时文件夹
make_dir = 'C:\\Users\\' + username + '\\Documents\\DA_Tools\\'
crawler_settings = make_dir + 'crawler_settings\\'
# 初始化文件
if not os.path.exists(crawler_settings):
    os.makedirs(crawler_settings)


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


def crawler_setting_page():
    # 创建爬虫通用设置页面
    crawler_page = crawler_settings + 'crawler_page'
    if not os.path.exists(crawler_page):
        with open(crawler_page,'w') as fp:
            fp.write('')
        fp.close()
    return crawler_page

