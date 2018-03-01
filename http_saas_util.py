#coding:utf-8
'''
Created on 2018年3月1日

@author: imac
'''
import requests

def postLisData2Saas(data) :
    print u'传输数据:' ,data
    resp = requests.post('http://dev.rolinzs.com/clinic/order/checkInstrument',data)
    print resp.text