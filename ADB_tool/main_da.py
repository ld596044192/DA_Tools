# -*- coding:utf-8 -*-
import ctypes,sys
import main_form
# 打包失败提示没有找到这个模块名称，请在spec文件中hiddenimports项添加即可，pyinstaller默认打包时不会打包第三方库，缺失的请添加！


def run_program():
    main = main_form.MainForm()
    # adb_form.root_form()

    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    if is_admin():
        main.root_form()
    else:
        ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, __file__, None, 1)


run_program()


