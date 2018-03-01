#coding:utf-8
import pymssql
import _mssql
import uuid
import decimal
import json
import requests
import time,sched
import collections
import os,sys
import ConfigParser
#import logging
#全局变量
_fileName = 'resultid.txt'
_config = 'config.ini'
_hospitalId =''
#设置日志文件
#logging.basicConfig(filename='mejer.log',format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#    datefmt='%a, %d %b %Y %H:%M:%S',level=logging.DEBUG)

# 初始化sched模块的scheduler类
schedule = sched.scheduler(time.time, time.sleep)

#读取配置文件
conf = ConfigParser.ConfigParser()
conf.read(_config)
_hospitalId = conf.get("hospital","id")

def postLisData2Saas(data) :
    print u'传输数据:' ,data
    resp = requests.post(conf.get("saas","api"),data)
    print 'status_code:',resp.status_code
    #logging.info('headers:'+resp.headers)
    #print data
    #print 'send data to saas'
def readLastQry():
    '读取上一次查询的最大值'
    if os.path.isfile(_fileName) == False :
        lastResId =0
        return lastResId
    # 打开一个文件
    with open(_fileName, 'r') as file :
        lines = file.readlines()
        lastLine = lines[-1]
        
    strs = lastLine.split('|') #行内容是 时间戳 行ID
    return int(strs[1])
def writeQryRow(resultid):
    '写入本次读取的最后一个行'
    with open(_fileName,'a') as file :
        file.write('\n')
        file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "|" + str(resultid))
def readDBConfig():
    '读取数据库配置'    
    options = conf.options("DB")

    if 'host' not in options :
        print u'数据库IP必须配置 like host=172.0.0.1'
        return None
    if 'user' not in options :
        print  u'用户名必须配置 like user=me'
        return    None
    if 'password' not in options :
        print u'密码必须配置 like password=pwd'
        return None
    if 'database' not in options :
        print u'数据库实例必须配置 like database=mydb'
        return    None
    return     conf    

def qryLabElementRslt(cursor,reportid) :
    print u'读取报告ID=',reportid
    sql = "select rpt_itemcode,result_str from dbo.lab_result where reportid =%d"
    cursor.execute(sql,reportid)
    rs = cursor.fetchall()
    if cursor.rowcount ==0 :
        print  u'没有数据，报表ID=',str(reportid)
        return

    report_element_list = []
    for row in rs :
        d = collections.OrderedDict()        
        d['instrumentCode']= row[0]
        if row[1] is not None :
            d['checkResult']= row[1].decode('utf-8')
        else :
            d['checkResult']=''
        report_element_list.append(d)
    return json.dumps(report_element_list)

def qryLabRslt(reportid):
    maxReportId =0
    conf = readDBConfig()
    if conf == None : 
        return 0
    try:
        conn = pymssql.connect(host=conf.get("DB","host"),user=conf.get("DB","user"),password=conf.get("DB","password"),database=conf.get("DB","database"),charset="utf8")
        cursor = conn.cursor()
        sql = "select reportid,pat_no from dbo.lab_report where  reportid >%d and pat_no <>'' order by reportid desc"
        cursor.execute(sql,reportid)
        #用一个rs变量获取数据
        rs = cursor.fetchall()
        if cursor.rowcount ==0 :
            print  u'没有数据'
            return 0

        pos =-1        
        for row in rs :
            #d = collections.OrderedDict()
            d = {}
            #查询用户的检验明细项
            report_element_list = qryLabElementRslt(cursor,int(row[0]))            
            if report_element_list is None :
                continue

            d['dataStrs'] = report_element_list
            d['hospitalId']= _hospitalId
            d['barCode']= row[1].encode("gbk")
            postLisData2Saas(d)
            pos +=1
            if pos ==0 :
                maxReportId =int(row[0])
        return maxReportId
    except Exception as e:
        print e
    finally:
        cursor.close()
        conn.close()    
# 被周期性调度触发的函数
def loopSyncData(cmd, inc):
    #logging.info( "now is:"+ time.time())
    #logging.info(  sys.getdefaultencoding())
    #os.system(cmd)
    schedule.enter(inc, 0, loopSyncData, (cmd, inc))
    #找出上一次查询到哪里
    lastReportId = readLastQry()
    print u'上一次获取报告ID=',str(lastReportId)
    #查出未读的检验数据,找出最大的reportid
    lastReportId=qryLabRslt(lastReportId)
    print lastReportId
    if lastReportId ==0 :
        return
    print u'本次抽取最后的报告ID=',str(lastReportId)
    #record本次同步
    writeQryRow(lastReportId)

    
def main():
    # enter四个参数分别为：间隔时间、优先级（用于同时间到达的两个事件同时执行时定序）、被调用触发的函数，给该触发函数的参数（tuple形式）
    schedule.enter(0, 0, loopSyncData, ('something', 180))
    schedule.run()
    #d ={}
    #d['dataStrs'] = '[{"instrumentCode":"201710110001","checkResult":"0.76"},{"instrumentCode":"201710110002","checkResult":"21"}]'
    #d['hospitalId']= _hospitalId
    #d['barCode']= '20170927000702'
    #postLisData2Saas(d)
    #print qryLabRslt(613)
    #rowid = readLastQry()
    #if(rowid ==0) :
    #    writeQryRow(10)
    #else :
    #    rowid +=12
    #    writeQryRow(rowid)
#

if __name__ == '__main__':
    main()
