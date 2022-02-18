import os.path
import signal
import time
import public
import getpass,win32api
import datetime

adb_path = public.resource_path(os.path.join('adb-tools'))
record_state = public.resource_path(os.path.join('temp','record_state.txt'))
record_main = public.resource_path(os.path.join('background_program','record_main.exe'))
username = getpass.getuser()
make_dir = 'C:\\Users\\' + username + '\\Documents\\ADB_Tools(DA)\\'
count_path = make_dir + 'screenshots_count.txt'
record_count = make_dir + 'record_count.txt'
# 获取录屏程序开始状态
record_began = make_dir + 'record_state.txt'
# 自定义截图保存文件夹名
dirname = 'ADB工具-截图（DA）'
save_path = 'C:\\Users\\' + username + '\\Desktop\\' + dirname + '\\'
# 自定义录屏保存文件名
record_dirname = 'ADB工具-录屏（DA）'
record_save = 'C:\\Users\\' + username + '\\Desktop\\' + record_dirname + '\\'


def cd_screenshots():
    # 进入截图临时保存文件夹
    command = 'adb shell cd /sdcard/da_screenshots'
    screenshot = public.execute_cmd(command)
    print(screenshot)
    mkdir_state = screenshot.split(':')[-1]
    # 创建截图临时保存文件夹
    if mkdir_state == ' No such file or directory\r\n':
        make_state = public.execute_cmd('adb shell mkdir /sdcard/da_screenshots')
        return make_state


def main_screenshots(touch_name):
    # 初始化截图缓存
    if not os.path.exists(make_dir):
        os.makedirs(make_dir)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    if not os.path.exists(count_path):
        with open(count_path, 'w') as fp:
            fp.write('0')

    # 截图
    f = int(open(count_path, 'r').read())
    f += 1
    public.execute_cmd('adb shell screencap -p /sdcard/da_screenshots/' + touch_name + '（' + str(f) + '）' + '.png')
    # 默认等待2S，防止截图不完整
    time.sleep(2)
    # 后面pull目的文件夹中的目的文件，添加一样的文件后缀名，避免pull后的文件乱码且不是截图文件，确保是png格式的高清截图文件
    pull_cmd = 'adb pull /sdcard/da_screenshots/' + touch_name + '（' + str(f) + '）' + '.png ' + save_path + touch_name + '（' + str(f) + '）' + '.png'
    public.execute_cmd(pull_cmd)
    with open(count_path, 'w') as fp:
        fp.write(str(f))
    fp.close()
    # 删除截图缓存（减少占用空间）
    public.execute_cmd('adb shell rm -r /sdcard/da_screenshots/' + touch_name + '（' + str(f) + '）' + '.png')
    screenshot_success = '截图成功！文件保存在:\n ' + save_path + dirname + '\\' + touch_name + '（' + str(f) + '）' + '.png'
    # 超出显示范围状态提示处理
    if len(screenshot_success) > 58:
        screenshot_success = '截图成功！文件保存在:\n 桌面\\' + dirname + '\\' + touch_name + '（' + str(f) + '）' + '.png'
    return screenshot_success


def open_screenshots():
    # 打开截图文件夹
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    win32api.ShellExecute(0, 'open',save_path, '', '', 1)


def open_record_main():
    # 运行录屏程序
    win32api.ShellExecute(0, 'open',record_main , '', '', 1)


def record_time(record_str):
    # 录屏计时器
    # # 等待录屏程序响应，根据机器性能有所不同
    # time.sleep(4)
    # 等待录屏后台程序响应后才开始计时
    while True:
        record_time_began = open(record_began, 'r').read()
        record_start = datetime.datetime.now()
        if record_time_began == 'Began to record the screen':
            break
    while True:
        # 读取录屏状态
        record_action = open(record_began,'r').read()
        print(record_action)
        if record_action == 'Began to record the screen':
            record_update = datetime.datetime.now()
            # 获取计时
            record_stop = record_update - record_start
            # 录屏时间格式处理
            record_end1 = str(record_stop).split(':')[-1].split('.')[0]
            record_end2 = str(record_stop).split(':')
            record_end2.pop()
            record_end3 = ':'.join(record_end2)
            record_end_finally = record_end3 + ':' + record_end1
            print(record_end_finally)
            record_str.set('正在录屏中，已录屏时间：' + record_end_finally)
            time.sleep(1)
            record_stop_flag = open(record_state, 'r').read()
            print(record_stop_flag)
            # 停止录屏计时
            if record_stop_flag == 'Stop recording screen':
                record_str.set('录屏结束，总用时：' + record_end_finally)
                break
        else:
            record_str.set('正在启动录屏，请稍候...')
    return record_end_finally


def record_pull(record_name):
    # 保存录屏视频

    r = int(open(record_count,'r').read())
    r += 1

    download_cmd = 'adb pull /sdcard/da_screenrecord/' + record_name + '（' + str(r) + '）' + '.mp4 ' + record_save + record_name + '（' + str(r) + '）' + '.mp4'
    pull_state = public.execute_cmd(download_cmd)
    print(pull_state)
    with open(record_count, 'w') as fp:
        fp.write(str(r))

    # # 删除录屏文件缓存（减少占用空间）
    # public.execute_cmd('adb shell rm -r /sdcard/da_screenrecord/' + record_name + '（' + str(r) + '）' + '.mp4')
