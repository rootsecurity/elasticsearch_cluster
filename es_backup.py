# -*- coding:UTF-8 -*- #
"""
备份ElaticSearch
"""

import sys,requests
import simplejson
import time,os
import zipfile
from public import sendMail

URL="http://10.98.10.10:9200/_snapshot/backup"
BAK_DIR="/export/JD/elasticsearch_backup/data" 
ZIP_DIR="/export/JD/elasticsearch_backup/zip"
MailList='no-reply@member.jd.com'

if __name__=='__main__':
    date=time.strftime('%Y.%m.%d',time.localtime(time.time()-86400*50))

    data1={"type": "fs","settings": {"location":BAK_DIR ,"compress": True}}
    r1=requests.post(URL,simplejson.dumps(data1))
    print r1.text

    index='logstash-sec-'+date
    #index='logstash-sec-attacklog-'+date
    url=URL+'/'+index

    #开始备份指定INDEX
    data2={"indices":index,"ignore_unavailable": True,"include_global_state": False }
    r2=requests.post(url,simplejson.dumps(data2))
    print r2.text
    
    #查询备份状态
    r3=requests.get(url)
    dic=simplejson.loads(r3.text)
    while  (dic['snapshots'][0]['state']=='IN_PROGRESS'):
        print "%s Backup is IN_PROGRESS..." % index
        time.sleep(10)
        r3=requests.get(url)
        dic=simplejson.loads(r3.text)
    
    if dic['snapshots'][0]['state']=='SUCCESS':
        print '%s 备份成功' % index
    	try:
            #压缩文件
            zfile=ZIP_DIR+'/'+index+'.zip'
            z = zipfile.ZipFile(zfile,'w',zipfile.ZIP_DEFLATED,allowZip64=True) 
            print "开始压缩文件..."
            for dirpath, dirnames, filenames in os.walk(BAK_DIR):  
                for filename in filenames:  
                    z.write(os.path.join(dirpath,filename))  
            z.close()

            os.system('rm -rf '+BAK_DIR) #删除原文件目录

            print "备份结束"
            
            title='ES-BACKUP:%s 备份成功' % index
            mailMsg='%s 备份成功!\n' % index
            mailMsg += 'ES返回结果:\n'+r3.text.encode('utf8')
            sendMail(mailMsg,MailList,title)

        except Exception,e:
            print e
            title='ES-BACKUP:%s 备份失败' % index
            mailMsg='文件压缩失败!'
            sendMail(mailMsg,MailList,title)

    else:
        print '%s 备份失败' % index
        title='ES-BACKUP:%s 备份失败' % index
        mailMsg='%s 备份失败!\n' % index
        mailMsg += 'ES返回结果:\n'+r3.text.encode('utf8')
        sendMail(mailMsg,MailList,title)
