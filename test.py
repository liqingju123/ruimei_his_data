#coding:utf-8

import os


print os.path.isfile('/Users/imac/Downloads/测试创建/测试创建.txt')
print os.path.exists('/Users/imac/Downloads/测试创建')


create_txt =open('/Users/imac/Downloads/测试创建/测试创建.txt','r+')
print create_txt.readlines()
create_txt.seek(0)
create_txt.truncate()
create_txt.write('111111122')
create_txt.write('\n')
create_txt.close()


