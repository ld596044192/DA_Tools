import public


def android_back(device):
    # 返回
    public.execute_cmd('adb -s ' + device + ' shell input keyevent 4')


def android_settings(device):
    # 进入系统设置
    public.execute_cmd('adb -s ' + device + ' shell am start com.android.settings/com.android.settings.Settings')


def android_reboot(device):
    # 重启设备
    public.execute_cmd('adb -s ' + device + ' shell reboot')


def android_shutdown(device):
    # 关闭设备
    public.execute_cmd('adb -s ' + device + ' shell reboot -p')


def clear_cache(device):
    # 清理缓存（初始化）
    package_name = public.found_packages(device)
    public.execute_cmd('adb -s ' + device + ' shell pm clear ' + package_name)


def terminate_program(device):
    # 结束应用（不是初始化，不会清理缓存，单纯kill程序）
    package_name = public.found_packages(device)
    public.execute_cmd('adb -s ' + device + ' shell am force-stop ' + package_name)


def android_desktop(device):
    # 返回Launcher桌面
    public.execute_cmd('adb -s ' + device + ' shell am start -n com.android.launcher3/.Launcher')


def android_awake(device):
    # 唤醒屏幕
    public.execute_cmd('adb -s ' + device + ' shell input keyevent 224')
