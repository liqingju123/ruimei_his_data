#coding:utf-8
import pymssql
import json
import requests
import collections
from  time import sleep
import os
import  re
sql = "select labrp.rpt_itemcode, labrp.rpt_itemname , labre.result_str ,labrep.pat_no,labrep.pat_name  from  dbo.lab_result labre , dbo.lab_report labrep,dbo.lab_rptitem labrp where labrp.rpt_itemcode = labre.rpt_itemcode and labrep.reportid = labre.reportid and labrep.pat_no ='%s'"  #查找已审核通过的人
sql_no  ="select pat_no,pat_name from dbo.lab_report  where ( unpriceflag = 0 or unpriceflag is null) and  rechk_dt is null" #查找未审核的人
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

def initPath():
    if os.path.exists('六号大街检查'.decode('utf8')):
        os.mkdir('六号大街检查'.decode('utf8'))
        os.mkdir('六号大街检查\\已上传列表'.decode('utf-8'))
        

def postLisData2Saas(data) :
    request_data =open('六号大街检查\\请求数据.txt'.decode('utf-8'),'a+')
    request_data.write(str(data))
    resp = requests.post('http://dev.rolinzs.com/clinic/order/checkInstrument',data)
    request_data.write(resp.text.encode('utf8'))
    request_data.write('\n')
    request_data.close()
    #print resp.text
'''
获取未审核的 检查项目
'''
def qeryLabElementRsltNoRe(cursor):
    zanweishenhe_r =open('暂未审核的项目.txt'.decode('utf-8'),'a+') # 暂未审核的项目列表
    zanweishenhe_list =zanweishenhe_r.readlines()
    zanweishenhe_r.close()
    zanweishenhe_w =open('暂未审核的项目.txt'.decode('utf-8'),'w+') # 暂未审核的项目列表
    cursor.execute(sql_no)
    rs = cursor.fetchall()
    pat_no =''
    pat_name =''
    
    list_all_weishenhe =[];
    list_all_weishenhe_only_pat_no=[];
    index=1
    for row in rs :
        if row[0] is None:
            pat_no ='暂无'
        else:
            pat_no=row[0].encode('utf8')
        if row[1] is None:
            pat_name ='暂无'
        else:
            pat_name = row[1].encode('utf8')
        list_all_weishenhe_only_pat_no.append(pat_no)
        list_all_weishenhe.append('%d__%s__%s\n' % (index,pat_no,pat_name))
        index=index+1
        
    for one_zanweishenhe_list in zanweishenhe_list:
        
        if len(one_zanweishenhe_list) > 3 and one_zanweishenhe_list.split('__')[1] not in list_all_weishenhe_only_pat_no:
            qeryLabElementRslt(cursor,one_zanweishenhe_list.split('__')[1])
            
 
    zanweishenhe_w.writelines(list_all_weishenhe)
    
    zanweishenhe_w.flush()
    zanweishenhe_w.close()
        
def qeryLabElementRslt(cursor,reportid):
    zanweishenhe_yes =open(str('六号大街检查\\已上传列表\\已上传的项目列表_'+str(reportid)+'.txt').decode('utf-8'),'a+')
    sql_write =open(r'六号大街检查\SQL.txt'.decode('utf-8'),'a+');

    sql_write.write(sql % reportid.strip())
    sql_write.write('\n')
    sql_write.close()
    
    cursor.execute(sql % reportid.strip())
    rs = cursor.fetchall()
    if cursor.rowcount ==0 :
        print  u'没有数据，报表ID=|',reportid.strip()
        return

    report_element_list = []
    rpt_itemcode =''
    result_str =''
    pat_name=''
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
        if row[4] is None:
            pat_name ='暂无'
        else:
            pat_name =row[4].encode('utf8')
        d = collections.OrderedDict()        
        d['instrumentCode']= rpt_itemcode
        d['checkResult']=result_str
        report_element_list.append(d)
        
        list_jiancha_all.append('%s__%s__%s__%s__%s\n'% (rpt_itemcode,row[1].encode('utf8'),result_str,row[3].encode('utf8'),pat_name))
      
    data['dataStrs'] = json.dumps(report_element_list)
    data['hospitalId']= _hospitalId
    data['barCode']= str(reportid)
  
    zanweishenhe_yes.writelines(list_jiancha_all)
        
    zanweishenhe_yes.close()   
    postLisData2Saas(data)
    return data



if __name__ =='__main__':
    while True :
        try:
            #sleep(60*3) # 保证服务器先启动
            conn = pymssql.connect(host= '127.0.0.1',port='1577',user='sa',password='ljhy2016',database='rmlis6',charset="utf8")
            cursor = conn.cursor()
            print 'conn  session'
            break
        except Exception as err:
            print 'conn not session'
            sleep(10)
    while True:
        qeryLabElementRsltNoRe(cursor)
        sleep(2)
   


#qeryLabElementRsltNoRe(cursor)
#data = qeryLabElementRslt(cursor,20171214000455)



