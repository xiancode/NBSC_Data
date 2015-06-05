#!/usr/bin/env  python
# coding=utf-8

from progressbar import *
import sys,time
total = 100000
type = sys.getfilesystemencoding()

progress = ProgressBar()
#for i in range(total):
#    #print  "正在处理",i,"\r"
#    sys.stdout.write("已经处理".decode('utf-8').encode(type)+str(i)+"条记录".decode('utf-8').encode(type)+"\r")


for file_no in range(10000000):
        file_no += 1
        if file_no%10 == 0:
            #print "已经处理 ".decode('utf-8').encode(type),file_no," 条记录".decode('utf-8').encode(type)
            sys.stdout.write("已经处理".decode('utf-8').encode(type)+str(file_no)+"条记录".decode('utf-8').encode(type)+"\r")
            sys.stdout.flush()