#from pywinauto.application import Application
from pywinauto import application
from pywinauto.keyboard import send_keys
import win32gui
import time

'''（官方中文文档）
pywinauto是一组用于自动化Microsoft Windows GUI的python模块。 最简单的是，它允许您将鼠标和键盘操作发送到窗口对话框和控件。
安装
运行 pip install pywinauto
要检查是否已正确安装，请运行Python，中文环境可能不适用
>>> from pywinauto.application import Application
>>> app = Application(backend="uia").start("notepad.exe")
>>> app.UntitledNotepad.type_keys("%FX")
----------------------------------
一旦你安装了pywinauto - 你怎么样？ 第一个必要的事情是确定哪种可访问性技术（pywinauto的backend）可以用于您的应用程序。
Windows上受支持的辅助功能技术列表：
Win32 API (backend="win32") - 现在的默认backend
MFC, VB6, VCL, 简单的WinForms控件和大多数旧的遗留应用程序
MS UI Automation (backend="uia")
WinForms, WPF, Store apps, Qt5, 浏览器
注意: Chrome在启动之前需要--force-renderer-accessibility cmd标志。 由于comtypes Python库限制，不支持自定义属性和控件。
PS：到目前为止，Linux上的AT SPI和Apple Accessibility API都是长期计划。
-----------------------------------
GUI对象检查/Spy工具
如果您仍然不确定哪个backend最适合您，请尝试使用免费提供的对象检查/Spy工具：从GitHub repo gui-inspect-tool下载它们.
Spy++ 包含在MS Visual Studio发行版（甚至是Express或Community）中，可通过“开始”菜单访问。 它使用Win32 API。 这意味着如果Spy ++能够显示所有控件，那么“win32”`backend就是你需要的。 AutoIt Window Info工具是一种Spy ++克隆。
Inspect.exe 是Microsoft创建的另一个很棒的工具。 它包含在Windows SDK中，因此可以在x64 Windows上的以下位置找到它：
C:\Program Files (x86)\Windows Kits\<winver>\bin\x64     
将Inspect.exe切换到UIA mode（使用MS UI Automation）。 如果它可以显示比Spy ++更多的控件及其属性，那么可能是 "uia"backend是你的选择。
py_inspect 是基于pywinauto的多后端间谍工具的原型。 在可用后端之间切换可以通过“win32”和“uia”后端向您显示层次结构的差异。 py \ _inspect是SWAPY的未来替代品，仅在pywinauto == 0.5.4出现时支持“win32”后端。 由于现代pywinauto 0.6.0+架构，py \ _insins的初始实现仅包含大约150行代码。
如果所有检测工具都看不到某些或所有控件，则仍然可以通过使用基本模块鼠标和键盘生成鼠标和键盘事件来控制应用程序。
----------------------------------
'''
#注意，首先需要判断你要进行的程序是用什么语言写的，在实例化的时候会有区别，主要是判断backend是什么，你可以认为backend为位数（有32位，也有64位）。（下面将以记事本为例）
#官方文档中推荐使用spy++和inspect来检查。（本人推荐inspect更方便判断，但spy++虽不易看懂但更直观）
# 一：创建应用程序时可以指定应用程序的合适的backend，start方法中指定启动的应用程序
app = application.Application(backend='win32').start(r'C:\Users\lida\Desktop\yuvplayer.exe')

# 二：建立好入口后，我们需要连接到进程中。这里有四种方法:
#第1、2种方法通用性不强，每次运行ID和窗口句柄都可能不一样。第3种方法最直接简单，而第4种方法灵活性最强。（本人推荐使用第四种）
# 1.查看要打开的程序进程号，通过process指定进程号连接
#app = application.Application().connect(process=16352)

# 2.使用窗口句柄绑定（使用inspect查看更方便）
#app = application.Application().connect(handle=0x00450818)

# 3.使用程序路径绑定(路径前要使用r进行注释)
app = application.Application().connect(path=r'C:\Users\lida\Desktop\yuvplayer.exe')

# 4.使用标题、类型等匹配(强烈推荐使用Spy++查看更方便准确)
# app2 = application.Application().connect(title_re="YUV player - frame: 1/0", class_name="#32770 (对话框)")

# 三：选择窗口，下面有两种方法（其实在第五点会讲解的更详细）
# 1.不适用于窗口名为中文的
# wind_1 = app.窗口名

# 2.窗口名可以为中文（建议使用这种）
#wind_2 = app["无标题 - 记事本"]

# 3.可以按如下写法(但该写法有个限制，就是无法识别多个窗口，当有多个窗口时就会报错)
notepad = app.window(title='YUV player - frame: 1/0')

# # 四：选择操作菜单项，下面有两种方法（直接输入函数即可，别想着能够自动出来）
# #使用menu_select()函数进行选择，注意箭头和横杆都是英文格式
#
notepad.menu_select(r'File->Open')
#
# #使用快捷键进行选择
# #可以看到，菜单的每个选项都对应着快捷键，可以使用组合的快捷键直接访问我们需要的选项。
# '''对于一些特殊符号的快捷键，对应的码表如下:
# SHIFT                            +
# CTRL                             ^
# ALT                               %
# 空格键                            {SPACE}
#
# BACKSPACE                        {BACKSPACE}、{BS}   or   {BKSP}
# BREAK                            {BREAK}
# CAPS   LOCK                      {CAPSLOCK}
# DEL   or   DELETE                {DELETE}   or   {DEL}
# DOWN   ARROW                     {DOWN}
# END                              {END}
# ENTER                            {ENTER}   or   ~
# ESC                              {ESC}
# HELP                             {HELP}
# HOME                             {HOME}
# INS   or   INSERT                {INSERT}   or   {INS}
# LEFT   ARROW                     {LEFT}
# NUM   LOCK                       {NUMLOCK}
# PAGE   DOWN                      {PGDN}
# PAGE   UP                        {PGUP}
# PRINT   SCREEN                   {PRTSC}
# RIGHT   ARROW                    {RIGHT}
# SCROLL   LOCK                    {SCROLLLOCK}
# TAB                              {TAB}
# UP   ARROW                       {UP}
# +                                {ADD}
# -                                {SUBTRACT}
# *                                {MULTIPLY}
# /                                {DIVIDE}
# '''
# #notepad.type_keys('^+S')
#
# # 五：各控件的操作（匹配控件）
# #对于常见的窗口程序，需要点点填填的控件有输入框(Edit)、按钮(Button)、复选框(CheckBox)、单选框(RadioButton)、下拉列表(ComboBox).
# # 1.最简单的方法就是通过空间特征进行匹配。窗体也可以看成是一个大控件。匹配窗口的方法除了前面提到的window()方法，还可以通过中括号加窗口名。
# #yemian = app.window(title='页面设置')
#
# #除了title，还可以使用class或者title+class或者相近的text和类来匹配控件,如下：
# #yemian = app.window(title='页面设置',class_name='#32770(对话框)')
#
# #推荐使用以下，简单(但由于获取控件时发现该窗口的所有控件其实都在notepad这个窗口里，所以切换到这个窗口也是无意义的，这里只是演示效果)
yemian = app['打开']
#
# #另外一种方法就是我们知道了这个程序的层次结构，然后类似寻到DOM元素一样一层一层的匹配。
# #那么如何找到这个层次结构呢。pywinauto提供了print_control_identifiers()函数来显示该窗体下所有控件的结构。
# #获取控件信息后建议复制到文本文档，然后把该代码注释，因为获取后需要时间，为了不用每次都要重复获取，节省时间，建议这么做，这里只是测试，所以并不注释。
# notepad.print_control_identifiers()
# yemian.print_control_identifiers()
#
# #获取到控件信息，例如在页面设置->页眉去编辑内容，我们可以通过控件的text或者title来查找控件
# #注意，对于输入控件Edit，一般不建议使用text内容绑定，因为Edit的text内容会发生变化。另外，绑定的控件也可能不唯一,所以建议使用title查找控件。
# #以下两种方法都可用，按照自己习惯选择
# edit1 = notepad['Edit5']
# edit2 = notepad['Edit6']
edit1 = yemian.Edit
edit2 = yemian.Toolbar3
# #控件选择的方法有好几种，最简单的方法如下：(其实跟上面的两个一样的，只是写法稍微有些不同，更直接一点而已)
# '''
# edit1 = app['无标题 - 记事本']['Edit5']
# edit2 = app['无标题 - 记事本']['Edit6']
# '''
#
# #对于Edit控件，要么就是向里面写内容，要么就是读里面的内容。
# #下面方法是直接设置edit的text(注意函数是不会自动出来，需要手动输入)
# edit2.set_text('Hello,正在使用pywinauto进行记事本自动化呢')
edit1.set_text('D:\\my_git\\DA_Tools\\ADB_tool\\')
edit1.type_keys('^A')
edit1.type_keys('^X')
edit2.click()
send_keys('^V')
send_keys('~')
edit1.set_text('origin_320X240.yuv')
send_keys('~')
yemian['打开(&O)'].click()
time.sleep(1)
title = win32gui.GetWindowText(win32gui.GetForegroundWindow())
print(title)
notepad = app.window(title=title)
notepad.menu_select(r'Size->Custom')
custom_size = app['Custom Size']
width_edit = custom_size.WidthEdit
height_edit = custom_size.HeightEdit
ok_button = custom_size.OKButton
width_edit.set_text('320')
height_edit.set_text('240')
ok_button.click()
# time.sleep(1)
# #下面是使用type_keys来进行全选删除
# edit1.type_keys('^A')
# edit1.type_keys('{BS}')
# #第二种是在里面模拟键盘输入(如果字符串中没有空格，可以省略后面的参数)，殊途同归。
# edit2.type_keys('正在测试第二种方法   加了三个空格',with_spaces=True)
# time.sleep(1)
# #下面是使用send_keys来进行全选删除，但需要插入相关库，这是键盘事件
# send_keys('^A')
# send_keys('{BS}')
#
# #直接模拟点击（下面是通过控件名进行测试）
# #notepad.Button3.click()
# #也可以直接通过索引来进行操作
# notepad['确定'].click()
