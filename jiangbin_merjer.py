# -*- coding:utf-8 -*-
#  Author: liqingju

import socket
import  BC5000DataFromart
import jiangbin_log


# 接收信息
def recv_basic(the_socket):
    str_total =''
    while True:
        data = the_socket.recv(1024) 
        if not data: 
            jiangbin_log.write_jiancha_info(str_total)
            BC5000DataFromart.txt_2_data(str_total) # 格式处理并且上传到服务器
            print str_total
            str_total =''  
            break
        str_total = str_total+data
    

#连接仪器
def connect_mid():
    ip_port=('127.0.0.1',9999)
    s=socket.socket()
    s.connect(ip_port)
    recv_basic(s)
    s.close() 



if __name__ =='__main__': 
    jiangbin_log.mkdir_log_path()      
    connect_mid()
