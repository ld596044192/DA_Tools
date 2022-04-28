from pywinauto import application
from pywinauto.keyboard import send_keys
import win32gui
import time


# 取图自动化脚本
class Carmera(object):
    def carmera_automation(self,yuvplayer_path,yuv_paths):
        # 打开软件
        # UserWarning: 32-bit application should be automated using 32-bit Python (you use 64-bit Python) UserWarning)
        # 出现上方提示为警告提示，可忽略
        application.Application(backend='win32').start(yuvplayer_path)
        # 连接软件以获得属性等信息
        app = application.Application().connect(path=yuvplayer_path)
        # 找到窗口
        yuv_app = app.window(title='YUV player - frame: 1/0')
        # 打开yuv文件
        yuv_app.menu_select(r'File->Open')
        yuv_select = app['打开']
        yuv_name = yuv_select.Edit
        yuv_path = yuv_select.Toolbar3
        yuv_name.set_text(yuv_paths)
        yuv_name.type_keys('^A')
        yuv_name.type_keys('^X')
        yuv_path.click()
        send_keys('^V')
        send_keys('~')
        yuv_name.set_text('origin_320X240.yuv')
        time.sleep(1)
        yuv_select['打开(&O)'].click()
        # 等待1S确保能正常获取当前窗口标题
        time.sleep(1)
        app_title = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        print(app_title)
        # 设置yuv图片的宽高
        yuv_app_uodate = app.window(title=app_title)
        yuv_app_uodate.menu_select(r'Size->Custom')
        custom_size = app['Custom Size']
        width_edit = custom_size.WidthEdit
        height_edit = custom_size.HeightEdit
        ok_button = custom_size.OKButton
        width_edit.set_text('320')
        height_edit.set_text('240')
        ok_button.click()



