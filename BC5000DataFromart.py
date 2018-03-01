# -*- coding:utf-8 -*-
'''
Created on 2018年2月26日
迈瑞仪器对接 数据解析
map 格式 NAME VALUE 
六号大街是  CODE VALUE 

@author: liqingju

'''
import collections
import http_saas_util
import json

source_data = open('/Users/imac/Desktop/江滨诊所数据12.txt','r').read() # 读取数据
_hospitalId =10000246
list_xuechanggui =['WBC','BAS#','BAS%','NEU#','NEU%','EOS#','EOS%','LYM#','LYM%','MON#','MON%','RBC','HGB','MCV']
report_element_list = []
data = {}
reportid = ''
def txt_2_data(source_data):
    source_data_list = source_data.split('\r')
    for one_source_data_list in source_data_list:
        if 'UNICODE' in one_source_data_list.split('|'):
            report_element_list = []
            data = {}
            reportid = ''
            if (len(report_element_list) > 0):
                http_post()
            print '开始一个新的'
        if one_source_data_list.startsswith('Count'):
            reportid = one_source_data_list.split('|')[3]
        if one_source_data_list.startswith('OBX'):
            one_source_data_list_one = one_source_data_list.split('|')
            if (one_source_data_list_one[3].split('^')[1] in list_xuechanggui): # 直方图跟散点图 不上传到服务器
                print one_source_data_list_one[3].split('^')[0] + '    ' + one_source_data_list_one[3].split('^')[1] + '   ' + one_source_data_list_one[5]
                d = collections.OrderedDict()
                d['instrumentCode'] = one_source_data_list_one[3].split('^')[1]
                d['checkResult'] = one_source_data_list_one[5]
                report_element_list.append(d)
    
    http_post()


def http_post():
    data['dataStrs'] = json.dumps(report_element_list)
    data['hospitalId']= _hospitalId
    data['barCode']= str(reportid)
    http_saas_util.postLisData2Saas(data)
    
# txt_2_data(source_data, list_xuechanggui)


