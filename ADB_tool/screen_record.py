import os.path
import time
import public
import getpass,win32api

username = getpass.getuser()
make_dir = 'C:\\Users\\' + username + '\\Documents\\ADB_Tools(DA)\\'
count_path = make_dir + 'screenshots_count.txt'
# 自定义截图保存文件夹名
dirname = 'ADB工具-截图（DA）'
save_path = 'C:\\Users\\' + username + '\\Desktop\\' + dirname + '\\'


def cd_screenshots():
    # 进入截图临时保存文件夹
    command = 'adb shell cd /sdcard/da_screenshots'
    screenshot = public.execute_cmd(command)
    # 创建截图临时保存文件夹
    if screenshot.split(':')[-1] == 'No such file or directory':
        public.execute_cmd('adb shell mkdir /sdcard/da_screenshots')


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
