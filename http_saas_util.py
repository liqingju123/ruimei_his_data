#coding:utf-8
'''
Created on 2018年3月1日

@author: imac
'''
import requests
import jiangbin_log

def postLisData2Saas(data) :
    resp = requests.post('http://dev.rolinzs.com/clinic/order/checkInstrument',data)
    jiangbin_log.http_post_info(data,resp.text.encode('utf8'))