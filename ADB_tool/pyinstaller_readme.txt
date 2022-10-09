使用前请先升级pyinstaller
pip install -U pyinstaller

main_da.py

pyinstaller -Fw .\main_da.py .\main_form.py -p .adb_test\.__init__.py,.\adb_test\customize_main.py,.\adb_test\pywinauto_adb.py,.\adb_test\public.py,.\adb_test\quickly.py,.\adb_test\screen_record.py -i .\my-da.ico --key dazhilingyu596044192

pyinstaller  .\main_da.spec