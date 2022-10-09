import os,getpass
import sys
import time,re,win32api,shutil,subprocess,win32ui
import public,windnd
import tkinter,tkinter.ttk,tkinter.messagebox,tkinter.filedialog
import threading,ctypes

LOGO_path = public.resource_path(os.path.join('icon', 'android.ico'))
flow_package = public.resource_path(os.path.join('temp','flow_package.txt'))
flow_package_log = public.resource_path(os.path.join('temp','flow_package_log.txt'))
devices_type_log = public.resource_path(os.path.join('temp','devices_type_log.txt'))  # 记录设备类型
username = getpass.getuser()
make_dir = 'C:\\Users\\' + username + '\\Documents\\ADB_Tools(DA)\\'
path_page = make_dir + 'path_page\\'
# 实时保存设备序列号
devices_log = make_dir + 'devices.log'
# md5和大小路径保存
md5_size_path = path_page + 'md5_size_path.log'
# 判断当前包名是否一致标记
package_flag = False
# 判断当前设备类型是否更换标记
devices_type_flag = False
if not os.path.exists(path_page):
    os.makedirs(path_page)


# 查询应用流量值工具界面
class Flow_Screen(object):
    def flow_form(self,flow_Button,flow_Button_disable):
        self.flow_root = tkinter.Toplevel()
        self.flow_root.title('查询应用流量值工具')
        # screenWidth = self.screen_root.winfo_screenwidth()
        # screenHeight = self.screen_root.winfo_screenheight()
        w = 400
        h = 300
        # x = (screenWidth - w) / 2
        # y = (screenHeight - h) / 2
        self.flow_root.geometry('%dx%d' % (w, h))
        self.flow_root.iconbitmap(LOGO_path)
        self.flow_root.resizable(0, 0)
        # self.screen_root.wm_attributes('-topmost', 1)

        self.flow_startup(flow_Button,flow_Button_disable)

        self.flow_root.protocol('WM_DELETE_WINDOW',self.close_handle)
        self.main_frame()
        # self.device_monitor(init_str)

        return self.flow_root

    def flow_startup(self,flow_Button,flow_Button_disable):
        # 监听截图页面的打开状态
        flow_exists = self.flow_root.winfo_exists()
        print(flow_exists)
        if flow_exists == 1:
            flow_Button.place_forget()
            flow_Button_disable.place(x=20, y=20)

    def close_handle(self):
        # 监听页面消失
        with open(public.flow_page(),'w') as fp:
            fp.write('0')
        fp.close()
        self.flow_root.destroy()

    def main_frame(self):
        # 上行流量与下行流量Label
        self.up_flow_label = tkinter.Label(self.flow_root,text='上行（上传）流量')
        self.up_flow_label.place(x=20,y=20)

        self.down_flow_label = tkinter.Label(self.flow_root, text='下行（下载）流量')
        self.down_flow_label.place(x=250, y=20)

        # 上行流量与下行流量显示框
        self.up_flow_str = tkinter.StringVar()
        self.up_flow = tkinter.Label(self.flow_root,textvariable=self.up_flow_str,bg='#FFFFFF',height=2,width=10,
                                     font=('宋体',15))
        self.up_flow.place(x=20,y=50)
        self.up_flow_str.set('0')

        self.down_flow_str = tkinter.StringVar()
        self.down_flow = tkinter.Label(self.flow_root, textvariable=self.down_flow_str, bg='#FFFFFF', height=2, width=10,
                                     font=('宋体',15))
        self.down_flow.place(x=250, y=50)
        self.down_flow_str.set('0')

        # 上行总流量与下行总流量label
        self.up_flow_total_label = tkinter.Label(self.flow_root, text='上行已使用总流量')
        self.up_flow_total_label.place(x=130, y=0)

        self.down_flow_total_label = tkinter.Label(self.flow_root, text='下行已使用总流量')
        self.down_flow_total_label.place(x=130, y=50)

        # 上行总流量与下行总流量显示框
        self.up_flow_total_str = tkinter.StringVar()
        self.up_flow_total = tkinter.Label(self.flow_root, textvariable=self.up_flow_total_str, bg='#FFFFFF', height=2, width=15,
                                     font=('宋体', 10))
        self.up_flow_total.place(x=130, y=20)
        self.up_flow_total_str.set('0')

        self.down_flow_total_str = tkinter.StringVar()
        self.down_flow_total = tkinter.Label(self.flow_root, textvariable=self.down_flow_total_str, bg='#FFFFFF', height=2,
                                       width=15,
                                       font=('宋体', 10))
        self.down_flow_total.place(x=130, y=70)
        self.down_flow_total_str.set('0')

        # 启动流量检测按钮
        self.start_button = tkinter.Button(self.flow_root,width=12,text='开始检测流量')
        self.start_button_disbale = tkinter.Button(self.flow_root,width=12,text='正在检测中...')
        self.start_button_disbale.config(state='disable')
        self.start_button.bind('<Button-1>',lambda x:self.flow_main())
        self.start_button.place(x=30,y=102)

        # 暂停流量检测按钮
        self.stop_button = tkinter.Button(self.flow_root, width=12, text='停止检测')
        self.stop_button_disbale = tkinter.Button(self.flow_root, width=12, text='停止检测')
        self.stopping_button_disbale = tkinter.Button(self.flow_root, width=12, text='正在停止...')
        self.stop_button_disbale.config(state='disable')
        self.stopping_button_disbale.config(state='disable')
        self.stop_button.bind('<Button-1>', lambda x: self.flow_stop_bind())
        self.stop_button_disbale.place(x=240, y=102)

        # 日志记录显示
        self.flow_frame = tkinter.Frame(self.flow_root,width=400,height=150)
        self.flow_scrollbar = tkinter.Scrollbar(self.flow_frame)
        self.flow_text = tkinter.Text(self.flow_frame,yscrollcommand=(self.flow_scrollbar.set),width=50,height=12,
                                      font=('宋体',10))
        self.flow_scrollbar.config(command=self.flow_text.yview)
        self.flow_scrollbar.pack(side=(tkinter.RIGHT),fill=(tkinter.Y))
        self.flow_text.config(state='disable')  # 设为disable防止Text多行文本框能被点击
        self.flow_text.pack()
        self.flow_frame.place(x=20,y=135)

    def flow_stop_bind(self):
        def t_flow_stop():
            # 停止检测流量
            global flow_stop_flag
            self.stopping_button_disbale.place(x=240,y=102)
            self.flow_text.config(state='normal')
            self.flow_text.insert(tkinter.END, '已手动中断线程，结束检测流量！\n')
            self.flow_text.see(tkinter.END)
            self.flow_text.config(state='disable')
            flow_stop_flag = True
            time.sleep(2)  # 延时设置避免未重置数值
            self.up_flow_str.set('0KB/s')
            self.down_flow_str.set('0KB/s')
            self.up_flow_total_str.set('0')
            self.down_flow_total_str.set('0')
            return flow_stop_flag

        t_flow_stop = threading.Thread(target=t_flow_stop)
        t_flow_stop.setDaemon = True
        t_flow_stop.start()

    def flow_main(self):
        def flow_text_normal():
            self.flow_text.config(state='normal')

        def flow_text_disable():
            self.flow_text.config(state='disable')

        def get_pid():
            global package_flag
            # 获取包名及Uid
            # 获取当前应用的包名
            time.sleep(1)
            flow_text_normal()
            device = open(devices_log,'r').read()
            package_name = public.found_packages(device)
            # print(package_name)
            if not package_name:
                self.flow_text.insert(tkinter.END, '包名获取失败，正在重新获取...\n')
                self.flow_text.see(tkinter.END)
                flow_text_disable()
                package_flag = False
            else:
                with open(flow_package, 'w') as fp:
                    fp.write(package_name.strip())
                fp.close()
                self.flow_text.insert(tkinter.END, '已检测到正在使用的应用包名：' + package_name + '\n')
                self.flow_text.see(tkinter.END)
                flow_text_disable()
                # 获取对应的包名的pid
                public.execute_cmd('adb -s ' + device + ' shell ps > ' + flow_package_log)
                ps_result_finally = open(flow_package_log, 'r').read()
                pid_result_re = re.findall('\n\w+.*?(\d+).*?' + package_name + '\n', ps_result_finally)
                pid_result = ''.join(pid_result_re)
                if pid_result == '':
                    flow_text_normal()
                    self.flow_text.insert(tkinter.END, '获取当前应用pid失败，正在重新获取当前包名...\n')
                    self.flow_text.see(tkinter.END)
                    flow_text_disable()
                    package_flag = False
                else:
                    flow_text_normal()
                    self.flow_text.insert(tkinter.END, package_name + '获取的pid：' + pid_result + '\n')
                    self.flow_text.see(tkinter.END)
                    # flow_text_disable()
                    # # 获取包名的uid
                    # uid_result_status = public.execute_cmd('adb -s ' + device + ' shell cat /proc/' + pid_result + '/status')
                    # uid_result_re = re.findall('Uid.*?(\d+).*?', uid_result_status)
                    # uid_result = ''.join(uid_result_re)
                    # flow_text_normal()
                    # self.flow_text.insert(tkinter.END, package_name + '获取的Uid：' + uid_result + '\n')
                    # self.flow_text.see(tkinter.END)
                    self.flow_text.insert(tkinter.END, '正在计算当前应用流量值中...\n')
                    self.flow_text.see(tkinter.END)
                    flow_text_disable()
                    return pid_result

        def t_flow_main():
            global package_flag,devices_type_flag,flow_stop_flag
            flow_stop_flag = False  # 暂停标识
            # 查询流量主要逻辑
            self.start_button_disbale.place(x=30,y=102)
            self.stop_button_disbale.place_forget()
            self.stop_button.place(x=240,y=102)
            with open(flow_package,'w') as fp:
                fp.write('')
            fp.close()
            # 开始输入内容前需要编辑
            flow_text_normal()
            self.flow_text.insert(tkinter.END,'正在开始查询应用流量...\n')
            self.flow_text.see(tkinter.END)
            flow_text_disable()
            device_state = public.device_connect()
            if not device_state:
                flow_text_normal()
                self.flow_text.insert(tkinter.END,'设备没有连接，无法获取应用使用流量情况！\n')
                self.flow_text.see(tkinter.END)
                # 显示内容后立即禁用
                flow_text_disable()
            else:
                while True:
                    devices_type = open(devices_type_log, 'r').read()
                    if devices_type != 'Android':
                        print('进入Linux模式')
                        # 初始化计算总和的变量
                        rcv_total = 0
                        snd_total = 0
                        # flow_text_normal()
                        # self.flow_text.insert(tkinter.END, '检测到非安卓设备，请使用安卓设备进行操作！\n')
                        # self.flow_text.see(tkinter.END)
                        # flow_text_disable()
                        flow_text_normal()
                        self.flow_text.insert(tkinter.END, '已检测到设备类型为Linux！\n')
                        self.flow_text.see(tkinter.END)
                        self.flow_text.insert(tkinter.END, '正在计算当前Linux设备流量值中...\n')
                        self.flow_text.see(tkinter.END)
                        flow_text_disable()
                        try:
                            while True:
                                # print('----------------------------')
                                device_state = public.device_connect()
                                device = open(devices_log, 'r').read()
                                if not device_state:
                                    flow_text_normal()
                                    self.flow_text.insert(tkinter.END, '设备突然断开连接，线程终止！\n')
                                    self.flow_text.see(tkinter.END)
                                    flow_text_disable()
                                    break
                                if devices_type_flag or flow_stop_flag:
                                    break
                                flow_exists = self.flow_root.winfo_exists()
                                try:
                                    # 获取Linux设备的上行和下行
                                    rcv_snd1 = public.execute_cmd('adb -s ' + device + ' shell grep "wlan0" /proc/net/dev')
                                    rcv_snd_list1 = [i for i in rcv_snd1.strip().split(' ') if i != '']
                                    # print(rcv_snd_list1) # 调试查看流量值获取结果
                                    # 获取第一次的上行速度
                                    snd1 = rcv_snd_list1[9]
                                    # 获取第一次的下行速度
                                    rcv1 = rcv_snd_list1[1]
                                    time.sleep(1)
                                    rcv_snd2 = public.execute_cmd('adb -s ' + device + ' shell grep "wlan0" /proc/net/dev')
                                    rcv_snd_list2 = [i for i in rcv_snd2.strip().split(' ') if i != '']
                                    # 获取第二次的上行速度
                                    snd2 = rcv_snd_list2[9]
                                    # 获取第二次的下行速度
                                    rcv2 = rcv_snd_list2[1]
                                    snd_finally = (int(snd2) - int(snd1)) / 1024
                                    snd_finally_update = round(snd_finally, 2)
                                    rcv_finally = (int(rcv2) - int(rcv1)) / 1024
                                    rcv_finally_update = round(rcv_finally, 2)
                                    if snd_finally_update >= 1024:
                                        snd_finally_mb = snd_finally / 1024
                                        snd_finally_update_mb = round(snd_finally_mb,2)
                                        self.up_flow_str.set(str(snd_finally_update_mb) + 'MB/s')
                                    else:
                                        self.up_flow_str.set(str(snd_finally_update) + 'KB/s')
                                    if rcv_finally_update >= 1024:
                                        rcv_finally_mb = rcv_finally / 1024
                                        rcv_finally_update_mb = round(rcv_finally_mb, 2)
                                        self.down_flow_str.set(str(rcv_finally_update_mb) + 'MB/s')
                                    else:
                                        self.down_flow_str.set(str(rcv_finally_update) + 'KB/s')
                                    # 计算上行行流量值总和
                                    snd_total += snd_finally_update
                                    # print('上行流量总和：' + str(snd_total))
                                    if 1024 <= snd_total < 1048576:  # 该表达式同等 snd_total >= 1024 and snd_total < 1048576
                                        snd_total_mb = snd_total / 1024
                                        snd_finally_update_mb = round(snd_total_mb, 2)
                                        self.up_flow_total_str.set(str(round(snd_finally_update_mb, 2)) + 'MB')
                                    elif rcv_total > 1048576:
                                        snd_total_gb = snd_total / 1024 / 1024
                                        snd_finally_update_gb = round(snd_total_gb, 2)
                                        self.up_flow_total_str.set(str(round(snd_finally_update_gb, 2)) + 'GB')
                                    else:
                                        self.up_flow_total_str.set(str(round(snd_total, 2)) + 'KB')
                                    # 计算下行行流量值总和
                                    rcv_total += rcv_finally_update
                                    # print('下行流量总和：' + str(rcv_total))
                                    if 1024 <= rcv_total < 1048576:  # 该表达式同等 rcv_total >= 1024 and rcv_total < 1048576
                                        rcv_total_mb = rcv_total / 1024
                                        rcv_finally_update_mb = round(rcv_total_mb, 2)
                                        self.down_flow_total_str.set(str(round(rcv_finally_update_mb,2)) + 'MB')
                                    elif rcv_total > 1048576:
                                        rcv_total_gb = rcv_total / 1024 / 1024
                                        rcv_finally_update_gb = round(rcv_total_gb, 2)
                                        self.down_flow_total_str.set(str(round(rcv_finally_update_gb,2)) + 'GB')
                                    else:
                                        self.down_flow_total_str.set(str(round(rcv_total,2)) + 'KB')
                                    if flow_exists == 0:
                                        package_flag = False
                                        print('flow_up_down检测线程已结束！')
                                        break
                                except (UnboundLocalError,ValueError,TypeError,IndexError):
                                    pass
                        except tkinter.TclError:
                            pass
                    else:
                        print('进入安卓模式')
                        # 初始化计算总和的变量
                        rcv_total = 0
                        snd_total = 0
                        flow_text_normal()
                        self.flow_text.insert(tkinter.END, '已检测到设备类型为Android（安卓）！\n')
                        self.flow_text.see(tkinter.END)
                        flow_text_disable()
                        flow_text_normal()
                        self.flow_text.insert(tkinter.END, '开始获取当前的应用包名...\n')
                        self.flow_text.see(tkinter.END)
                        flow_text_disable()
                        try:
                            while True:
                                # print('+++++++++++++++++++++++')
                                device_state = public.device_connect()
                                device = open(devices_log, 'r').read()
                                if not device_state:
                                    flow_text_normal()
                                    self.flow_text.insert(tkinter.END, '设备突然断开连接，线程终止！\n')
                                    self.flow_text.see(tkinter.END)
                                    flow_text_disable()
                                    break
                                if not devices_type_flag or flow_stop_flag:
                                    break
                                if not package_flag:
                                    try:
                                        # 默认第一次必须执行
                                        pid_result = get_pid()
                                        if not pid_result:
                                            continue
                                        package_flag = True
                                    except AttributeError:
                                        continue
                                flow_exists = self.flow_root.winfo_exists()
                                try:
                                    # 获取Linux设备的上行和下行
                                    rcv_snd1 = public.execute_cmd(
                                        'adb -s ' + device + ' shell grep "wlan0" /proc/' + pid_result + '/net/dev')
                                    rcv_snd_list1 = [i for i in rcv_snd1.strip().split(' ') if i != '']
                                    # print(rcv_snd_list1) # 调试查看流量值获取结果
                                    # 获取第一次的上行速度
                                    snd1 = rcv_snd_list1[9]
                                    # 获取第一次的下行速度
                                    rcv1 = rcv_snd_list1[1]
                                    time.sleep(1)
                                    rcv_snd2 = public.execute_cmd(
                                        'adb -s ' + device + ' shell grep "wlan0" /proc/' + pid_result + '/net/dev')
                                    rcv_snd_list2 = [i for i in rcv_snd2.strip().split(' ') if i != '']
                                    # 获取第二次的上行速度
                                    snd2 = rcv_snd_list2[9]
                                    # 获取第二次的下行速度
                                    rcv2 = rcv_snd_list2[1]
                                    snd_finally = (int(snd2) - int(snd1)) / 1024
                                    snd_finally_update = round(snd_finally, 2)
                                    rcv_finally = (int(rcv2) - int(rcv1)) / 1024
                                    rcv_finally_update = round(rcv_finally, 2)
                                    if snd_finally_update >= 1024:
                                        snd_finally_mb = snd_finally / 1024
                                        snd_finally_update_mb = round(snd_finally_mb, 2)
                                        self.up_flow_str.set(str(snd_finally_update_mb) + 'MB/s')
                                    else:
                                        self.up_flow_str.set(str(snd_finally_update) + 'KB/s')
                                    if rcv_finally_update >= 1024:
                                        rcv_finally_mb = rcv_finally / 1024
                                        rcv_finally_update_mb = round(rcv_finally_mb, 2)
                                        self.down_flow_str.set(str(rcv_finally_update_mb) + 'MB/s')
                                    else:
                                        self.down_flow_str.set(str(rcv_finally_update) + 'KB/s')
                                    # 计算上行行流量值总和
                                    snd_total += snd_finally_update
                                    # print('上行流量总和：' + str(snd_total))
                                    if 1024 <= snd_total < 1048576:  # 该表达式同等 snd_total >= 1024 and snd_total < 1048576
                                        snd_total_mb = snd_total / 1024
                                        snd_finally_update_mb = round(snd_total_mb, 2)
                                        self.up_flow_total_str.set(str(round(snd_finally_update_mb, 2)) + 'MB')
                                    elif rcv_total > 1048576:
                                        snd_total_gb = snd_total / 1024 / 1024
                                        snd_finally_update_gb = round(snd_total_gb, 2)
                                        self.up_flow_total_str.set(str(round(snd_finally_update_gb, 2)) + 'GB')
                                    else:
                                        self.up_flow_total_str.set(str(round(snd_total, 2)) + 'KB')
                                    # 计算下行行流量值总和
                                    rcv_total += rcv_finally_update
                                    # print('下行流量总和：' + str(rcv_total))
                                    if 1024 <= rcv_total < 1048576:  # 该表达式同等 rcv_total >= 1024 and rcv_total < 1048576
                                        rcv_total_mb = rcv_total / 1024
                                        rcv_finally_update_mb = round(rcv_total_mb, 2)
                                        self.down_flow_total_str.set(str(round(rcv_finally_update_mb, 2)) + 'MB')
                                    elif rcv_total > 1048576:
                                        rcv_total_gb = rcv_total / 1024 / 1024
                                        rcv_finally_update_gb = round(rcv_total_gb, 2)
                                        self.down_flow_total_str.set(str(round(rcv_finally_update_gb, 2)) + 'GB')
                                    else:
                                        self.down_flow_total_str.set(str(round(rcv_total, 2)) + 'KB')
                                    if flow_exists == 0:
                                        package_flag = False
                                        print('flow_up_down检测线程已结束！')
                                        break
                                except (UnboundLocalError, ValueError, TypeError, IndexError):
                                    pass
                        except tkinter.TclError:
                            break
                    if not device_state or flow_stop_flag:
                        print('主循环结束！')
                        break
            try:
                self.start_button_disbale.place_forget()
                self.stop_button.place_forget()
                self.stopping_button_disbale.place_forget()
                self.stop_button_disbale.place(x=240,y=102)
            except tkinter.TclError:
                pass

        def t_package():
            global package_flag,devices_type_flag
            # 实时检测当前包名
            with open(flow_package,'w') as fp:
                fp.write('')
            fp.close()
            try:
                while True:
                    device_state = public.device_connect()
                    if not device_state:
                        print('设备突然断开连接，线程终止！')
                        self.up_flow_str.set('0KB/s')
                        self.down_flow_str.set('0KB/s')
                        self.up_flow_total_str.set('0')
                        self.down_flow_total_str.set('0')
                        package_flag = False
                        break
                    device = open(devices_log, 'r').read()
                    package_name = public.found_packages(device)
                    package_name_orgin = open(flow_package,'r').read()
                    device_type = open(devices_type_log,'r').read()
                    flow_exists = self.flow_root.winfo_exists()
                    if package_name != package_name_orgin and package_flag and package_name_orgin != '' and package_name != ''\
                            and package_name:
                        # 多判断防止不断重新获取包名和Uid
                        flow_text_normal()
                        self.flow_text.insert(tkinter.END, '检测到当前包名已发生变化，正在重新获取Uid...\n')
                        self.flow_text.see(tkinter.END)
                        flow_text_disable()
                        package_flag = False
                    elif flow_exists == 0:
                        print('flow_package检测线程已结束！')
                        package_flag = False
                        try:
                            public.stop_thread(t_flow_main)
                        except ValueError:
                            pass
                        break
                    elif device_type != 'Android' and device_type != '' and devices_type_flag:
                        devices_type_flag = False
                    elif device_type == 'Android' and device_type != '' and not devices_type_flag:
                        devices_type_flag = True
                        package_flag = False
                    time.sleep(2)
            except tkinter.TclError:
                pass

        t_flow_main = threading.Thread(target=t_flow_main)
        t_flow_main.setDaemon(True)
        t_flow_main.start()

        t_package = threading.Thread(target=t_package)
        t_package.setDaemon(True)
        t_package.start()


# 获取文件MD5和大小页面
class MD5_Screen(object):
    def md5_size_form(self,md5_size_Button,md5_size_Button_disable):
        self.md5_size_root = tkinter.Toplevel()
        self.md5_size_root.title('文件MD5大小计算工具')
        screenWidth = self.md5_size_root.winfo_screenwidth()
        screenHeight = self.md5_size_root.winfo_screenheight()
        w = 500
        h = 400
        x = (screenWidth - w) / 2
        y = (screenHeight - h) / 2
        self.md5_size_root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        # self.md5_size_root.geometry('%dx%d' % (w, h))
        self.md5_size_root.iconbitmap(LOGO_path)
        self.md5_size_root.resizable(0, 0)
        self.md5_size_root.wm_attributes('-topmost', 1)

        self.md5_size_startup(md5_size_Button,md5_size_Button_disable)

        self.md5_size_root.protocol('WM_DELETE_WINDOW',self.close_handle)
        self.main_frame()
        # self.device_monitor(init_str)

        return self.md5_size_root

    def md5_size_startup(self,md5_size_Button,md5_size_Button_disable):
        # 监听截图页面的打开状态
        md5_size_exists = self.md5_size_root.winfo_exists()
        print(md5_size_exists)
        if md5_size_exists == 1:
            md5_size_Button.place_forget()
            md5_size_Button_disable.place(x=200, y=20)

    def close_handle(self):
        # 监听页面消失
        with open(public.md5_size_page(),'w') as fp:
            fp.write('0')
        fp.close()
        self.md5_size_root.destroy()

    def count_md5_size(self,file_path):
        def t_count_md5():
            # 计算文件MD5和大小
            # self.md5_size_entry.config(state='disable')
            self.md5_size_button_disable.place(x=20, y=20)
            self.md5_clear_button_disbale.place(x=120,y=20)
            file_size_result = os.stat(file_path).st_size
            if file_size_result >= 524288000:  # 文件大于500MB的采取大文件md5获取
                self.md5_size_text.insert(tkinter.END,'\n-----------------------------')
                self.md5_size_text.insert(tkinter.END,'\n该文件大于500MB，采取分块计算，将会消耗一些时间，请耐心等待...')
                self.md5_size_text.insert(tkinter.END,'\n（计算MD5值期间不能复制粘贴修改等操作）')
                self.md5_size_text.insert(tkinter.END,'\n-----------------------------')
                self.md5_size_text.see(tkinter.END)
                self.md5_size_text.config(state='disable')
                file_md5 = public.bigger_file_md5(file_path)
                try:
                    self.md5_size_text.see(tkinter.END)
                except tkinter.TclError:
                    pass
                self.md5_size_text.config(state='normal')
                self.md5_size_text.see(tkinter.END)  # 确保能正常移动到最下方
            else:
                file_md5 = public.file_md5(file_path)
            file_size = round(file_size_result / 1024 / 1024, 2)
            self.md5_size_text.insert(tkinter.END,'\n' + file_path + '\nmd5值：' + file_md5 + '\n文件大小：' +
                                      str(file_size_result) + ' 字节 (' + str(file_size) + 'MB)')
            self.md5_size_text.insert(tkinter.END, '\n-----------------------------')
            # self.md5_size_entry.config(state='normal')
            self.md5_size_text.see(tkinter.END)
            self.md5_size_button_disable.place_forget()
            self.md5_clear_button_disbale.place_forget()

        t_count_md5 = threading.Thread(target=t_count_md5)
        t_count_md5.setDaemon(True)
        t_count_md5.start()

    def windnd_hook_files(self,widget):
        # 拖拽文件到text文本框获取文件路径功能（windnd） widget是控件
        def dragged_files(files):
            path_msg = '\n'.join((item.decode('gbk') for item in files))
            print('获取的文件路径：' + path_msg)
            # 拖拽到框即可获取md5和大小
            self.count_md5_size(path_msg)

        # 使用windnd方法
        windnd.hook_dropfiles(widget,func=dragged_files)

    def main_frame(self):
        # 上传文件获取路径
        self.md5_size_str = tkinter.StringVar()
        # self.md5_size_entry = tkinter.Entry(self.md5_size_root,width=50, highlightcolor='#87CEFA',
        #                                     textvariable=self.md5_size_str, highlightthickness=5)
        # self.md5_size_entry.place(x=20,y=20)
        # if not os.path.exists(md5_size_path):
        #     with open(md5_size_path, 'w') as fp:
        #         fp.write('')
        # path_msg = open(md5_size_path, 'r').read()
        # self.md5_size_str.set(path_msg)

        # 浏览文件
        self.md5_size_button = tkinter.Button(self.md5_size_root,text='浏览',width=10)
        self.md5_size_button.bind('<Button-1>',lambda x:self.md5_size_button_bind())
        self.md5_size_button_disable = tkinter.Button(self.md5_size_root,text='浏览',width=10)
        self.md5_size_button_disable.config(state='disable')
        self.md5_size_button.place(x=20,y=20)

        # 清空记录
        self.md5_clear_button = tkinter.Button(self.md5_size_root, text='清空', width=10)
        self.md5_clear_button_disbale = tkinter.Button(self.md5_size_root, text='清空', width=10)
        self.md5_clear_button.bind('<Button-1>', lambda x: self.md5_clear())
        self.md5_clear_button_disbale.config(state='disable')
        self.md5_clear_button.place(x=120, y=20)

        # 文件MD5和大小显示
        self.md5_size_frame = tkinter.Frame(self.md5_size_root, width=500, height=200)
        self.md5_size_scrollbar = tkinter.Scrollbar(self.md5_size_frame)
        self.md5_size_text = tkinter.Text(self.md5_size_frame, yscrollcommand=(self.md5_size_scrollbar.set), width=53, height=15,
                                      font=('宋体', 13))
        self.md5_size_scrollbar.config(command=self.md5_size_text.yview)
        self.md5_size_scrollbar.pack(side=(tkinter.RIGHT), fill=(tkinter.Y))
        # self.md5_size_text.config(state='disable')  # 设为disable防止Text多行文本框能被点击
        self.md5_size_text.pack()
        self.md5_size_text.insert(tkinter.END, '请点击浏览文件，打开后自动计算文件MD5和大小！\n温馨提示：可把文件拖拽到这里获取文件MD5和大小哦！')
        self.md5_size_frame.place(y=70)
        self.windnd_hook_files(self.md5_size_text)

    def md5_clear(self):
        # 清空显示的MD5和大小（避免记录过多）
        def t_md5_clear():
            self.md5_clear_button_disbale.place(x=120,y=20)
            self.md5_size_text.delete(0.0,tkinter.END)
            self.md5_size_text.insert(tkinter.END, '请点击浏览文件，打开后自动计算文件MD5和大小！\n温馨提示：可把文件拖拽到这里获取文件MD5和大小哦！')
            self.md5_clear_button_disbale.place_forget()

        t_md5_clear = threading.Thread(target=t_md5_clear)
        t_md5_clear.setDaemon(True)
        t_md5_clear.start()

    def md5_size_button_bind(self):
        def t_md5_size_button():
            # 浏览文件（不限类型）
            self.md5_size_button_disable.place(x=20,y=20)
            # self.md5_size_entry.config(state='disable')
            if not os.path.exists(md5_size_path):
                with open(md5_size_path,'w') as fp:
                    fp.write('C:\\Users\\' + getpass.getuser() + '\\Desktop\\')
                fp.close()
            path_msg = open(md5_size_path, 'r').read()
            path_msg_finally = '\\'.join(path_msg.split('\\')[:-1])
            dlg = win32ui.CreateFileDialog(True, "csv", None, 0x04 | 0x02)
            dlg.SetOFNInitialDir(path_msg_finally)
            self.md5_size_root.wm_attributes('-topmost', 0)
            dlg.DoModal()  # 显示文件选择框
            file_path = dlg.GetPathName()  # 获取选择的文件名称
            if file_path == '':
                # self.md5_size_entry.config(state='normal')
                # self.md5_size_text.config(state='normal')
                self.md5_size_button_disable.place_forget()
                pass
            else:
                self.md5_size_str.set(file_path)
                with open(md5_size_path, 'w') as fp:
                    fp.write(file_path)
                fp.close()
                self.count_md5_size(file_path)  # 记录文件MD5和大小
            self.md5_size_root.wm_attributes('-topmost', 1)

        t_md5_size_button = threading.Thread(target=t_md5_size_button)
        t_md5_size_button.setDaemon(True)
        t_md5_size_button.start()
