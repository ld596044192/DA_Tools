import getpass,os
import sys

username = getpass.getuser()
make_dir = 'C:\\Users\\' + username + '\\Documents\\ADB_Tools(DA)\\'


# #输出环境变量
# env=os.environ
# for key in env:
#  print (key + ' : ' + env[key])

#只看PATH变量

print(os.environ["PATH"])

#增加路径到环境中
os.environ["PATH"] += ";" + make_dir
#
# #注意这些环境变量都会动态的，就是重新打开变量就没有了，需要继续添加
# env=os.environ
# for key in env:
#  print (key + ' : ' + env[key])

print(os.environ["PATH"])
