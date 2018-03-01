#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import subprocess #导入执行命令模块
from time import sleep
ip_port=('127.0.0.1',9999) #定义元祖
#买手机

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #绑定协议，生成套接字
s.bind(ip_port)    #绑定ip+协议+端口：用来唯一标识一个进程，ip_port必须是元组格式
s.listen(5)        #定义最大可以挂起链接数
#等待电话
while True: 
    conn,addr=s.accept()  
    conn.sendall(open('/Users/imac/Desktop/江滨诊所数据12.txt','r').read())
    sleep(1000000000000)
    #收消息
    while True: 
            try:
                recv_data=conn.recv(1024) 
                if len(recv_data) == 0:break 
                #发消息
                p=subprocess.Popen(str(recv_data,encoding='utf8'),shell=True,stdout=subprocess.PIPE) #执行系统命令，windows平                                                                                     # 台命令的标准输出是gbk编码，需要转换
                res=p.stdout.read()   #获取标准输出
                if len(res) == 0:   #执行错误命令，标准输出为空，
                    send_data='cmd err'
                print(str)
                send_data=bytes(str(res,encoding='utf8'),encoding='utf8')


                #解决粘包问题
                ready_tag='Ready|%s' %len(send_data)
                conn.send(bytes(ready_tag,encoding='utf8')) #发送数据长度
                feedback=conn.recv(1024)  #接收确认信息
                feedback=str(feedback,encoding='utf8')

                if feedback.startswith('Start'):
                    conn.send(send_data)  #发送命令的执行结果
            except Exception:
                break
    #挂电话
    conn.close()