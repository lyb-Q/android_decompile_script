#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import oss2
import ConfigParser
import pexpect
import MySQLdb
import time
import xml.etree.ElementTree as ET

config = ConfigParser.ConfigParser()
config.read("config.ini")

#remote_dir = 'static/uploadfile/gcbao/origin.apk' #apk包路径
#remote_dir = 'origin.apk'
#sign_pwd = config.get('sign_param', 'sign_pwd')
version = "1.1.1.1"
def get_db():
    db_host = config.get('mysql', 'host')
    db_user = config.get('mysql', 'user')
    db_password = config.get('mysql', 'password')
    db_name = config.get('mysql', 'db')
    db_port = int(config.get('mysql', 'port'))
    db = MySQLdb.connect(host=db_host, user=db_user, passwd=db_password,
                         db=db_name, port=db_port)
    return db

# 获取桶（阿里服务）
def get_bucket():
    access_key_id = config.get('bucket_config', 'access_key_id')
    access_key_secret = config.get('bucket_config', 'access_key_secret')
    bucket_name = config.get('bucket_config', 'bucket_name') #Bucket
    endpoint = config.get('bucket_config', 'endpoint')  #访问域名 
    bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)
    return bucket

# 上传文件
def put_object(remote,local):
    bucket = get_bucket()
    bucket.put_object_from_file(remote,local)

# 下载文件
def get_object(remote,local):
    bucket = get_bucket()
    bucket.get_object_to_file(remote, local)
    

# 删除文件
def del_object(remote):
    bucket = get_bucket()
    bucket.delete_object(remote)

# 修改文件(xml)
def UP_file(dir,stationnum):
    tree = ET.parse(dir)
    root = tree.getroot()
    for info in root.findall('string'):
        if info.attrib['name'] == 'agentId':
            info.text = stationnum
        if info.attrib['name'] == 'app_name':
            info.text = "xxxxx"
        if info.attrib['name'] == 'version':
            version = info.text
            print(version)
        
    print(dir)
    tree.write(dir)
    
# 处理apk
def sign(file_data):
    os.system('apktool d ./origin_%s.apk'%(file_data)) #反编译apk 
    UP_file('./origin_%s/res/values/strings.xml'%(file_data),file_data) #更新文件数据
    os.system('apktool b ./origin_%s'%(file_data)) #编译
    print("sign func end")
    
def set_to_sql(path,stationnum):
    db = get_db()
    cursor = db.cursor()
    cond = "SELECT `versionid` FROM `tl_check_version` WHERE `stationnum`=%s\
    and `channel`=%s and version=%sand deleted=0 \
    "%(stationnum,"gancaibao",version)  
    datas = cursor.execute(cond)  
    if not datas:
        now = int(time.time())
        sql ="""INSERT INTO `tl_check_version` ( `alwaysshow`, `version`,`stationnum`, `info`, `isshow`, 
            `channel`, `device_type`,`data`,`down`, `provinceid`,`created`,`updated`, `status`)
        VALUES( %s, %s, %s,  %s,  %s, %s,  %s,  %s,  %s,  %s )"""
        args = (0,version,stationnum,"更新新版本",0,"gancaibao","android",path,"更新新功能",path,36,now,now,1)
        cursor.execute() 
        db.commit()
        db.close()
    
if __name__ == '__main__':
    print("running")


