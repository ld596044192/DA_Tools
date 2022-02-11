import public


def android_back():
    # 返回
    public.execute_cmd('adb shell input keyevent 4')


def android_settings():
    # 进入系统设置
    public.execute_cmd('adb shell am start com.android.settings/com.android.settings.Settings')


def android_reboot():
    # 重启设备
    public.execute_cmd('adb shell reboot')


def android_shutdown():
    # 关闭设备
    public.execute_cmd('adb shell reboot -p')


def clear_cache():
    # 清理缓存（初始化）
    package_name = public.found_packages()
    public.execute_cmd('adb shell pm clear ' + package_name)


def terminate_program():
    # 结束程序（不是初始化，不会清理缓存，单纯kill程序）
    package_name = public.found_packages()
    public.execute_cmd('adb shell am force-stop ' + package_name)


def android_desktop():
    # 返回Launcher桌面
    public.execute_cmd('adb shell am start -n com.android.launcher3/.Launcher')


def android_awake():
    # 唤醒屏幕
    public.execute_cmd('adb shell input keyevent 224')
