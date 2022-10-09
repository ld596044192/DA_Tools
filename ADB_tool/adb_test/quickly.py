import time

import public,pyperclip,tkinter.messagebox


def android_back(device):
    # 返回
    public.execute_cmd('adb -s ' + device + ' shell input keyevent 4')


def android_settings(device):
    # 进入系统设置
    public.execute_cmd('adb -s ' + device + ' shell am start com.android.settings/com.android.settings.Settings')


def current_reboot(device):
    # 重启设备（通用）
    public.execute_cmd('adb -s ' + device + ' shell reboot')


def android_shutdown(device):
    # 关闭设备
    public.execute_cmd('adb -s ' + device + ' shell reboot -p')


def clear_cache(device):
    # 清理缓存（初始化）
    try:
        package_name = public.found_packages(device)
        public.execute_cmd('adb -s ' + device + ' shell pm clear ' + package_name)
        # 息屏
        public.execute_cmd('adb -s ' + device + ' shell input keyevent 26')
        time.sleep(1)
        # 亮屏（不管息屏亮屏都点亮）
        public.execute_cmd('adb -s ' + device + ' shell input keyevent 224')
    except TypeError:
        print('未连接设备，请连接设备后再尝试！！！')


def terminate_program(device):
    # 结束应用（不是初始化，不会清理缓存，单纯kill程序）
    try:
        package_name = public.found_packages(device)
        public.execute_cmd('adb -s ' + device + ' shell am force-stop ' + package_name)
    except TypeError:
        print('未连接设备，请连接设备后再尝试！！！')


def android_desktop(device):
    # 返回Launcher桌面
    public.execute_cmd('adb -s ' + device + ' shell am start -n com.android.launcher3/.Launcher')


def android_awake(device):
    # 唤醒屏幕
    public.execute_cmd('adb -s ' + device + ' shell input keyevent 224')


def linux_shutdown(device):
    # 关闭设备（Linux）
    public.execute_cmd('adb -s ' + device + ' shell halt')


def current_copy_SN(device):
    # 一键复制SN序列号（通用）
    pyperclip.copy(device)
    # 从剪贴板那粘贴
    pyperclip.paste()
    tkinter.messagebox.showinfo('粘贴提醒','已复制粘贴 ' + device + ' 到剪贴板\n可以Ctrl+V粘贴到任意地方啦~')

