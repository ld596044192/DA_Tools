import os,getpass
import sys
import time,re,win32api,shutil,subprocess
import public,pywinauto_adb
import tkinter,tkinter.ttk,tkinter.messagebox,tkinter.filedialog
import threading,ctypes

LOGO_path = public.resource_path(os.path.join('icon', 'android.ico'))
flow_package = public.resource_path(os.path.join('temp','flow_package.txt'))
flow_package_log = public.resource_path(os.path.join('temp','flow_package_log.txt'))
# 判断当前包名是否一致标记
package_flag = False


# 截图工具界面
class Flow_Screen(object):
    def flow_form(self,flow_Button,flow_Button_disable,device,devices_type_log):
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
        self.main_frame(device,devices_type_log)
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
        self.flow_root.destroy()

    def main_frame(self,device,devices_type_log):
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
        self.start_button = tkinter.Button(self.flow_root,width=15,text='开始检测流量')
        self.start_button_disbale = tkinter.Button(self.flow_root,width=15,text='正在检测中...')
        self.start_button_disbale.config(state='disable')
        self.start_button.bind('<Button-1>',lambda x:self.flow_main(device,devices_type_log))
        self.start_button.place(x=130,y=100)

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

    def flow_main(self,device,devices_type_log):
        def flow_text_normal():
            self.flow_text.config(state='normal')

        def flow_text_disable():
            self.flow_text.config(state='disable')

        def get_pid_uid():
            global package_flag
            # 获取包名及Uid
            # 获取当前应用的包名
            time.sleep(1)
            flow_text_normal()
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
                self.flow_text.insert(tkinter.END, '已检测到正在使用的应用包名：' + package_name + '\n')
                self.flow_text.see(tkinter.END)
                flow_text_disable()
                # 获取对应的包名的pid
                public.execute_cmd('adb shell ps > ' + flow_package_log)
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
                    flow_text_disable()
                    # 获取包名的uid
                    uid_result_status = public.execute_cmd('adb shell cat /proc/' + pid_result + '/status')
                    uid_result_re = re.findall('Uid.*?(\d+).*?', uid_result_status)
                    uid_result = ''.join(uid_result_re)
                    flow_text_normal()
                    self.flow_text.insert(tkinter.END, package_name + '获取的Uid：' + uid_result + '\n')
                    self.flow_text.see(tkinter.END)
                    self.flow_text.insert(tkinter.END, '正在计算当前应用流量值中...\n')
                    self.flow_text.see(tkinter.END)
                    flow_text_disable()
                    return uid_result

        def t_flow_main():
            global package_flag
            # 查询流量主要逻辑
            self.start_button_disbale.place(x=130,y=100)
            with open(flow_package,'w') as fp:
                fp.write('')
            # 开始输入内容前需要编辑
            flow_text_normal()
            self.flow_text.insert(tkinter.END,'正在开始查询应用流量...\n')
            self.flow_text.see(tkinter.END)
            flow_text_disable()
            device_state = public.device_connect()
            devices_type = open(devices_type_log,'r').read()
            if not device_state:
                flow_text_normal()
                self.flow_text.insert(tkinter.END,'设备没有连接，无法获取应用使用流量情况！\n')
                self.flow_text.see(tkinter.END)
                # 显示内容后立即禁用
                flow_text_disable()
            else:
                if devices_type != 'Android':
                    flow_text_normal()
                    self.flow_text.insert(tkinter.END, '检测到非安卓设备，请使用安卓设备进行操作！\n')
                    self.flow_text.see(tkinter.END)
                    flow_text_disable()
                else:
                    flow_text_normal()
                    self.flow_text.insert(tkinter.END, '开始获取当前的应用包名...\n')
                    self.flow_text.see(tkinter.END)
                    flow_text_disable()
                    # 初始化计算总和的变量
                    rcv_total = 0
                    snd_total = 0
                    try:
                        while True:
                            device_state = public.device_connect()
                            if not device_state:
                                flow_text_normal()
                                self.flow_text.insert(tkinter.END, '设备突然断开连接，线程终止！\n')
                                self.flow_text.see(tkinter.END)
                                flow_text_disable()
                                break
                            if not package_flag:
                                try:
                                    # 默认第一次必须执行
                                    uid_result = get_pid_uid()
                                    if not uid_result:
                                        continue
                                    package_flag = True
                                except AttributeError:
                                    continue
                            flow_exists = self.flow_root.winfo_exists()
                            try:
                                # 获取第一次的上行速度
                                snd1 = public.execute_cmd('adb shell cat /proc/uid_stat/' + uid_result + '/tcp_snd')
                                # 获取第一次的下行速度
                                rcv1 = public.execute_cmd('adb shell cat /proc/uid_stat/' + uid_result + '/tcp_rcv')
                                time.sleep(1)
                                # 获取第二次的上行速度
                                snd2 = public.execute_cmd('adb shell cat /proc/uid_stat/' + uid_result + '/tcp_snd')
                                # 获取第二次的下行速度
                                rcv2 = public.execute_cmd('adb shell cat /proc/uid_stat/' + uid_result + '/tcp_rcv')
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
                            except (UnboundLocalError,ValueError,TypeError):
                                pass
                    except tkinter.TclError:
                        pass
            try:
                self.start_button_disbale.place_forget()
            except tkinter.TclError:
                pass

        def t_package():
            global package_flag
            # 实时检测当前包名
            with open(flow_package,'w') as fp:
                fp.write('')
            print('开始实时检测包名......')
            try:
                while True:
                    device_state = public.device_connect()
                    if not device_state:
                        print('设备突然断开连接，线程终止！')
                        package_flag = False
                        break
                    package_name = public.found_packages(device)
                    package_name_orgin = open(flow_package,'r').read()
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
                        self.up_flow_str.set('0')
                        self.down_flow_str.set('0')
                        break
                    time.sleep(2)
            except tkinter.TclError:
                pass

        t_flow_main = threading.Thread(target=t_flow_main)
        t_flow_main.setDaemon(True)
        t_flow_main.start()

        t_package = threading.Thread(target=t_package)
        t_package.setDaemon(True)
        t_package.start()
