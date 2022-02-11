import main_form
import ctypes,sys


def run_program():
    adb_form = main_form.MainForm()
    # adb_form.root_form()

    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    if is_admin():
        adb_form.root_form()
    else:
        ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, __file__, None, 1)


run_program()
