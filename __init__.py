#coding:utf-8
import pymssql
import _mssql
import uuid
import decimal
import json
import requests
import time,sched
import collections
from time import sleep
import re
import http_saas_util
sql = "select labrp.rpt_itemcode, labrp.rpt_itemname , labre.result_str ,labrep.pat_no,labrep.pat_name  from  dbo.lab_result labre , dbo.lab_report labrep,dbo.lab_rptitem labrp where labrp.rpt_itemcode = labre.rpt_itemcode and labrep.reportid = labre.reportid and labrep.pat_no = '%d'"  #查找已审核通过的人
sql_no  ="select pat_no,pat_name from dbo.lab_report  where  unpriceflag = 0 and  rechk_dt is null" #查找未审核的人
_hospitalId='1000046'

def hasNumbers(inputString):
    return bool(re.search(r'\d', inputString))

def value_to_key(value):  
    if hasNumbers(value):
        return value
    
    if  '弱阳性' in  value:
        return '±'
    elif '阳性' in value:
        
        return  '+'
    elif '阴性' in value:
        return '-'
    elif '正常' in value:
        return '正常'
    else:
        code_list = re.findall('[-+±]{1,}', value)
        if len(code_list)>0:
            return code_list[0]
        
        return value

'''
获取未审核的 检查项目
'''
def qeryLabElementRsltNoRe(cursor):
    zanweishenhe =open('/Users/imac/Downloads/六号大街检查/暂未审核的项目.txt','w+') # 暂未审核的项目列表
    cursor.execute(sql_no)
    rs = cursor.fetchall()
    pat_no =''
    pat_name =''
    zanweishenhe_list =zanweishenhe.readlines()
    list_all_weishenhe =[];
    for row in rs :
        if row[0] is None:
            pat_no ='暂无'
        else:
            pat_no=row[0].encode('utf8')
        if row[1] is None:
            pat_name ='暂无'
        else:
            pat_name = row[1].encode('utf8')
        list_all_weishenhe.append('%s__%s\n' % (pat_no,pat_name))
        
    for one_zanweishenhe_list in zanweishenhe_list:
        if one_zanweishenhe_list not in list_all_weishenhe:
            qeryLabElementRslt(cursor,one_zanweishenhe_list.split('__')[0])
            
#     for one_zanweishenhe_list in list_all_weishenhe:
    zanweishenhe.writelines(list_all_weishenhe)
    
    zanweishenhe.flush()
    zanweishenhe.close()
        
def qeryLabElementRslt(cursor,reportid):
    zanweishenhe_yes =open('/Users/imac/Downloads/六号大街检查/已上传列表/已上传的项目列表_%d.txt' % reportid,'a+')
    cursor.execute(sql,reportid)
    rs = cursor.fetchall()
    if cursor.rowcount ==0 :
        print  u'没有数据，报表ID=',str(reportid)
        return

    report_element_list = []
    rpt_itemcode =''
    result_str =''
    list_jiancha_all =[]
    data = {}
    for row in rs :
        if row[0] is None:
            rpt_itemcode ='暂无'
        else:
            rpt_itemcode=row[0].encode('utf8')
        if row[2] is None:
            result_str ='暂无'
        else:
            result_str = row[2].encode('utf8')
       
        d = collections.OrderedDict()        
        d['instrumentCode']= rpt_itemcode
        d['checkResult']=value_to_key(result_str)
        report_element_list.append(d)
        
        list_jiancha_all.append('%s__%s__%s__%s__%s\n'% (rpt_itemcode,row[1].encode('utf8'),result_str,row[3].encode('utf8'),row[4].encode('utf8')))
        print rpt_itemcode +','+result_str
    data['dataStrs'] = json.dumps(report_element_list)
    data['hospitalId']= _hospitalId
    data['barCode']= str(reportid)
  
    zanweishenhe_yes.writelines(list_jiancha_all)
        
    zanweishenhe_yes.close()   
    
    return data

if __name__ == '__main__':
    conn = pymssql.connect(host= '192.168.1.120',port='1577',user='sa',password='ljhy2016',database='rmlis6',charset="utf8")
    cursor = conn.cursor()
    data = qeryLabElementRslt(cursor,20171214000455)
    http_saas_util.postLisData2Saas(data)
    # qeryLabElementRsltNoRe(cursor)
    
    sleep(10)

