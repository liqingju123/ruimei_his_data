

import time
import os


# 日子目录搭建
def mkdir_log_path():
    if os.path.exists('传递原始数据'):
        os.makedirs('传递原始数据')
    if os.path.exists('江滨诊所'):
        os.makedirs('江滨诊所')

#读取出来的原始数据 写入LOG 进行存档
def write_jiancha_info(str_total):
    write_str_total =open('传递原始数据\\%s.txt' % str(int(time.time())),'a+')
    write_str_total.write(str_total.encode('utf8'))
    write_str_total.close()

#存储清洗之后的数据
def write_jiancha_info_from(code,name,str_total):
    write_str_total =open('上传用户信息\\%s__%s__%s.txt' % (code,name,str_total),'a+')
    write_str_total.write(str_total.encode('utf8'))
    write_str_total.close()

# data 请求参数  
# resp_text 返回参数
# 每次的请求日志进行存档
def http_post_info(data,resp_text):
    request_data =open('江滨诊所\\请求数据.txt'.decode('utf-8'),'a+')
    request_data.write(str(data))
    request_data.write(resp_text.encode('utf8'))
    request_data.write('\n')
    request_data.close()