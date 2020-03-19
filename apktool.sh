#!/bin/bash

echo -n  "please enter an stationnum ->"
read  stationnum
time=$(date "+%Y-%m-%d %H:%M:%S")
echo "${time}"
python -c 'import apktool; apktool.get_object("/static/uploadfile/gcbao/origin.apk","./origin_'$stationnum'.apk")' #源文件
python -c 'import apktool; apktool.sign('$stationnum')'
./sign.sh './origin_'$stationnum'/dist/origin_'$stationnum'.apk'
python -c 'import apktool; apktool.put_object("/static/uploadfile/gcbao/origin_$stationnum.apk","./origin_'$stationnum'.apk")' //上传到服务器
python -c 'import apktool; apktool.set_to_sql("/static/uploadfile/gcbao/origin_'$stationnum'.apk",'$stationnum')' #保存到数据库

time=$(date "+%Y-%m-%d %H:%M:%S")
echo "${time}"