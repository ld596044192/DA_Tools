import drink_water
import ctypes,sys


def run_program():
    main_form = drink_water.MainForm()

    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    if is_admin():
        root = main_form.root_form()
        main_form.minimize()
        root.mainloop()
    else:
        ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, __file__, None, 1)


run_program()