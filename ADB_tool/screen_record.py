import os.path
import signal
import sys
import time
import tkinter.messagebox
import public
import getpass,win32api
import datetime,shutil

adb_path = public.resource_path(os.path.join('adb-tools'))
record_state = public.resource_path(os.path.join('temp','record_state.txt'))
record_main = public.resource_path(os.path.join('background_program','record_main.exe'))
username = getpass.getuser()
make_dir = 'C:\\Users\\' + username + '\\Documents\\ADB_Tools(DA)\\'
count_path = make_dir + 'screenshots_count.txt'
record_count = make_dir + 'record_count.txt'
record_name = make_dir + 'record_name.txt'
record_model_log = make_dir + 'record_model.log'
# 录屏时间
record_time_txt = make_dir + 'record_time.txt'
# 获取录屏程序开始状态
record_began = make_dir + 'record_state.txt'
# 记录程序位置
exe_path = public.resource_path(os.path.join('temp','exe_path.log'))
# 录屏停止处理1
record_stop = make_dir + 'record_stop.ini'
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
    public.execute_cmd('adb shell rm -r /sdcard/da_screenshots/*.png')
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
    # 强制运行录屏程序
    while True:
        record_devices_state = open(record_began,'r').read()
        record_name = public.get_pid_name()
        if 'record_main.exe' in record_name:
            break
        elif record_devices_state == 'no devices':
            # 设备中断连接后强制结束录屏程序
            os.popen('taskkill /F /IM %s ' % 'record_main.exe /T', 'r')
            break
        else:
            win32api.ShellExecute(0, 'open',record_main , '', '', 1)


def record_time(record_str):
    # 录屏计时器（V1.0.0.6版开始取消计时功能，仅动态提示“正在录屏”，原因是计时无法与录屏文件时长进行同步）
    if not os.path.exists(record_began):
        with open(record_began,'w') as fp:
            fp.write('')
    # 检测后台程序是否运行，运行则继续，否则一直检测
    while True:
        devices_state = public.device_connect()
        record_name = public.get_pid_name()
        if 'record_main.exe' in record_name:
            break
        elif not devices_state:
            # # 有残留程序直接强制关闭（首先获取pid，再杀死程序）
            # record_pid = public.get_pid('record_main.exe')
            # print(record_pid)
            # try:
            #     for pid in record_pid:
            #         os.kill(pid, signal.SIGINT)
            #     break
            # except TypeError:
            #     print('该进程已退出，继续执行！')
            with open(record_began, 'w') as fp:
                fp.write('no devices')
            sys.exit()
    while True:
        try:
            record_time_began = open(record_began, 'r').read()
            if record_time_began == 'Began to record the screen':
                break
        except PermissionError:
            # sys.exit（）某种意义上也可以终止进程，不会继续向下执行代码，也不会结束主程序
            sys.exit()
    # 等待开始录屏后再计时
    time.sleep(4)
    # record_start = datetime.datetime.now()
    # try:
    while True:
        # 读取录屏状态
        record_action = open(record_began,'r').read()
    #     print(record_action)
        if record_action == 'Began to record the screen':
            # 动态显示录屏状态
            while True:
                record_stop = open(record_began, 'r').read()
                if record_stop == 'Stop recording screen':
                    break
                add_points = ['.','. .','. . .','. . . .']
                for point in add_points:
                    record_stop = open(record_began, 'r').read()
                    record_action = open(record_began, 'r').read()
                    if record_stop == 'Stop recording screen':
                        break
                    record_str.set('正在录屏中' + point)
                    time.sleep(1)
                    if record_action == 'continuous':
                        record_str.set('连续模式启动中，2秒后继续进行下一轮录屏...')
                        time.sleep(2)
        #         record_update = datetime.datetime.now()
        #         # 获取计时
        #         record_stop = record_update - record_start
        #         # 录屏时间格式处理
        #         record_end1 = str(record_stop).split(':')[-1].split('.')[0]
        #         record_end2 = str(record_stop).split(':')
        #         record_end2.pop()
        #         record_end3 = ':'.join(record_end2)
        #         record_end_finally = record_end3 + ':' + record_end1
        #         print(record_end_finally)
        #         record_str.set('正在录屏中，已录屏时间：' + record_end_finally)
        #         record_stop_flag = open(record_state, 'r').read()
        #
        #         print(record_stop_flag)
        #         # 停止录屏计时
        #         if record_stop_flag == 'Stop recording screen':
        #             record_str.set('录屏结束，总用时：' + record_end_finally)
        #             break
        else:
            # 录屏停止处理
            record_time_stop = open(record_began, 'r').read()
            if record_time_stop == 'Stop recording screen':
                break
            record_str.set('正在启动录屏，请稍候...')
            continue
        # return record_end_finally
    # except UnboundLocalError:
    #     with open(record_began, 'w') as fp:
    #         fp.write('no devices')


def record_pull(record_name):
    # 保存录屏视频

    # 重启ADB服务
    public.execute_cmd('adb start-server')

    # 等待ADB服务完全重启成功
    time.sleep(2)

    r = int(open(record_count,'r').read())
    r += 1

    download_cmd = 'adb pull /sdcard/da_screenrecord/' + record_name + '（' + str(r) + '）' + '.mp4 ' + record_save + record_name + '（' + str(r) + '）' + '.mp4'
    public.execute_cmd(download_cmd)
    with open(record_count, 'w') as fp:
        fp.write(str(r))

    # 删除录屏文件缓存（减少占用空间）
    public.execute_cmd('adb shell rm -r /sdcard/da_screenrecord/*.mp4')

    # 返回原始地址，防止与本地ADB服务发生冲突导致无法使用
    original_path = open(exe_path,'r').read()
    os.chdir(original_path)

    # 关闭ADB服务，以免影响本地ADB服务的开启
    public.execute_cmd('adb kill-server')


def open_screenrecords():
    # 打开录屏保存文件夹
    if not os.path.exists(record_save):
        os.makedirs(record_save)
    win32api.ShellExecute(0, 'open',record_save, '', '', 1)


def reset_delete(filename):
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
                public.execute_cmd('del /F /S /Q ' + filename)
            print(filename + ' 已删除！')


def reset_screenrecord():
    # 需要删除的文件或文件夹filename_list
    # 删除截图录屏保存文件夹 save_path，record_save 清空缓存 record_began，record_time_txt，record_name，record_model_log
    # 计数重置为零 count_path，record_count
    filename_list = [save_path,record_save,record_began,record_time_txt,record_name,record_model_log,count_path
        ,record_count,record_stop]
    for filename in filename_list:
        reset_delete(filename)




