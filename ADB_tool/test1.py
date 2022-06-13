#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/2/24 下午12:24
# @Author  : H贤笙

class valueType:
    def __init__(self):
        pass
    def toLog(self, input_message):
        input_message = int(input_message) + 123
        print(input_message)

# 日志模块
import logging
import traceback
# 引入日志
logging.basicConfig(filename='log.txt',
                    level=logging.DEBUG,
                    filemode='a+',
                    format='[%(asctime)s] [%(levelname)s] >>> \n%(message)s',
                    datefmt='%Y-%m-%d %I:%M:%S')
try:
    valueType = valueType()
    valueType.toLog("这是一个测试")
except Exception as e:
    traceback.print_exc() # 打印到控制台
    logging.error(traceback.format_exc())
