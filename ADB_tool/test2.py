import re,public

# adb shell 获取流量值
public.execute_cmd('adb shell ps > C:\\Users\\lida\\Desktop\\1.txt')

pid_all_result = open('C:\\Users\\lida\\Desktop\\1.txt','r').read()
# print(pid_all_result)
pid_result_re = re.findall('\nsystem.*?(\d+).*?com.dosmono.scanningpen\n',pid_all_result)
# print(pid_result_re)
pid_result = ''.join(pid_result_re)
print('com.dosmono.scanningpen pid：' + pid_result)

public.execute_cmd('adb shell cat /proc/' + pid_result + '/status > C:\\Users\\lida\\Desktop\\2.txt')
uid_all_result = open('C:\\Users\\lida\\Desktop\\2.txt','r').read()
# print(uid_all_result)
uid_result_re = re.findall('Uid.*?(\d+).*?',uid_all_result)
# print(uid_result_re)
uid_result = ''.join(uid_result_re)
print('com.dosmono.scanningpen Uid：' + uid_result)

while True:
    rcv_input1 = input('按下回车键即可获取第一次下行流量：')
    if rcv_input1 == '':
        rcv1 = public.execute_cmd('adb shell cat /proc/uid_stat/' + uid_result + '/tcp_rcv')  # 下行流量
        print('第一次下行流量:' + rcv1)
        rcv_input2 = input('按下回车键即可获取第二次下行流量（必须请求完再回车）：')
        if rcv_input2 == '':
            rcv2 = public.execute_cmd('adb shell cat /proc/uid_stat/' + uid_result + '/tcp_rcv')
            print('第二次下行流量:' + rcv2)
            rcv_finally = (int(rcv2) - int(rcv1)) / 1024
            rcv_finally_b = round(rcv_finally,2)
            print('本次请求网络流量为：' + str(rcv_finally_b) + 'KB\n')
    print('----------------------------------------------------------\n')
