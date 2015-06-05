#!/usr/bin/env python 
#-*- coding=utf-8 -*-
#Author:shizhongxian@126.com
#2015-06

"""
从国家统计局网站获取 
宏观年度数据hgnd
分省年度数据fsnd
分省季度数据fsjd
分省月度数据fsyd
"""

import ConfigParser
import sys
import re
import os
import random
import time
import urllib

global null
#替换文件中的null，防止获取到的数据转化词典错误
null = ""



#windows
type = sys.getfilesystemencoding()
#eclipse
#type = "utf-8"

note_menu = {'1':'获取宏观年度数据', 
                            '2':'获取各省份年度数据',
                             '3':'获取各省份季度数据',
                             '4':'获取各省份月度数据'}

data_dirs     = {'1':'hgnd', 
                            '2':'fsnd',
                             '3':'fsjd',
                             '4':'fsyd'}

def load_dict(tdfile,key_col,value_col_list):
    """
        根据文件和列来构造dict数据结构
    tdfile: 纯文本 表格样式的文件,列之间用"\t"分割 
    key_col:key列号,从0开始
    value_col_lilst:充当value的列号，列表形式[1,2,4],列号必须递增 
    """
    print "载入词典"
    result = {}
    fin = open(tdfile)
    line_no = 0
    line = fin.readline()
    if len(line.split("\t"))-1 < value_col_list[-1] or len(line.split("\t"))-1 < key_col :
        print "输入的列号大于文件列号".decode('utf-8').encode(type)
        sys.exit() 
    while line:
        line_no += 1
        if line_no%500==0:
            #print "加载数据 ".decode('utf-8').encode(type),line_no,"条"
            sys.stdout.write("加载数据".decode('utf-8').encode(type)+str(line_no)+"条".decode('utf-8').encode(type)+"\r")
        items = line.split("\t")
        if len(items)-1 < value_col_list[-1] or len(items)-1 < key_col:
            print line," 列数小于输入的列数".decode('utf-8').encode(type)
        else:
            if result.has_key(items[key_col]):
                pass
            else:
                tmp_list = []
                for i in value_col_list:
                    tmp_list.append(items[i])
                result[items[key_col]] = tmp_list
        line = fin.readline()
    fin.close()
    return result

def construct_urls(data_cls,data_dir,area_codes):
    """
    
    """
    urls = []
    init_url = "http://data.stats.gov.cn/workspace/index?a=l"
    inlist_filename = os.path.join(data_dir,"index_list.data")
    indexex_list = []
    try:
        fin = open(inlist_filename)
    except Exception,e:
        print "文件打开失败".decode("utf08").encode(type)
    else:
        indexex_list = fin.readlines()
        
    
    if data_cls == "hgnd":
        
        pass
    
    else:
        pass
    
  
def data_extract(data_dir):
    print "正在抽取".decode('utf-8').encode(type),data_dir,"下的数据".decode('utf-8').encode(type)
    filelist = []
    file_no = 0
    current_dir = os.path.dirname(data_dir)
    for root,dirs,files in os.walk(data_dir):
        for file_ in files:
            filelist.append(os.path.join(root,file_))

    indicator_num_filename = os.path.join(current_dir,"tabledata.txt")
    indicator_meta_filename = os.path.join(current_dir,"indicator_meta.txt")
    indicator_num_file = open(indicator_num_filename,"w")
    indicator_meta = open(indicator_meta_filename,"w")
    #region_meta = open("region_meata.txt","w")

    for filename in filelist:
        file_no += 1
        if file_no%10 == 0:
            #print "已经处理 ".decode('utf-8').encode(type),file_no," 条记录".decode('utf-8').encode(type)
            sys.stdout.write("已经处理".decode('utf-8').encode(type)+str(file_no)+"条记录".decode('utf-8').encode(type)+"\r")
        try:
            fin = open(filename)
        except Exception,e:
            print e
        else:
            all_data = fin.readlines()
            if len(all_data) == 1:
                try:
                    data_dict = eval(all_data[0])
                except Exception,e:
                    print e
                else:
                    tabledata = data_dict["tableData"]
                    for query,num in  tabledata.iteritems():
                        indi_no,rego_no,year = query.split("_")
                        indicator_num_file.write(indi_no+"\t"+rego_no+"\t"+year+"\t"+num+"\n")
                    
                    value_dict = data_dict["value"]
                    index_list = value_dict["index"]
                    for index_item in index_list:
                        in_id = index_item["id"]
                        in_name = index_item["name"]
                        unit = index_item["unit"]
                        note = index_item["note"]
                        in_ename = index_item["ename"]
                        in_eunit = index_item["eunit"]
                        enote = index_item["enote"]
                        indicator_meta.write(in_id+"\t"+in_name+"\t"+unit+"\t"+note+"\t"+in_ename+"\t"+in_eunit+"\t"+enote+"\n")

            fin.close() 
    indicator_num_file.close()
    indicator_meta.close()
    #返回数值文件名和指标元信息文件名
    return [indicator_num_filename,indicator_meta_filename]


def merge(finame,col,d,foutname):
    """
    
    """
    foutname = os.path.join(os.path.dirname(finame),foutname)
    fin = open(finame)
    fout = open(foutname,"w")
    file_no = 0
    line = fin.readline()
    cols = len(line.split("\t"))
    while line:
        #line = line.strip()
        file_no += 1
        if file_no%1000 == 0:
            #print "处理数据:".decode('utf-8').encode(type),file_no,"条".decode('utf-8').encode(type)
            sys.stdout.write("已经处理 ".decode('utf-8').encode(type)+str(file_no)+" 条记录".decode('utf-8').encode(type)+"\r")
        items = line.split("\t")
        
        if len(items) == cols:
            tmp_str = ""
            if col == 0:
                pass 
            elif col >=1:
                for i in range(col):
                    tmp_str += items[i]+"\t" 
            else:
                print "输入列参数有错误".decode('utf-8').encode(type)
                sys.exit()
            key = items[col]
            if d.has_key(key) :
                tmp_str += key+"\t"
                for d_item in d[key]:
                    tmp_str += d_item.strip() + "\t"
                for i in range(col+1,len(items)-1):
                    tmp_str += items[i].strip() + "\t"
                tmp_str += items[len(items)-1].strip()

                tmp_str += "\n"
                tmp_str2 = tmp_str.strip()
                tmp_str2 = tmp_str2.strip("\t")
                if tmp_str2 != "":
                    fout.write(tmp_str)
                    #print tmp_str,"------"
                else:
                    print items[0]," 字典中没找到，或此条目字典格式不正确".decode('utf-8').encode(type)
            else:
                print  "没有找到与".decode('utf-8').encode(type),
                print key,"相对应的值，请修改词典文件".decode('utf-8').encode(type)
        else:
            print line,"格式有错误,此行与首行字段个数不一致".decode('utf-8').encode(type)    
        line = fin.readline()
    fin.close()
    fout.close()
    return foutname

def load_urls(dir_name):
    urls_file_name = os.path.join(dir_name,"urls.txt")
    urls=[]
    try:
        fin = open(urls_file_name)
    except Exception,e:
        print urls_file_name,"文件打开失败".decode('utf-8').encode(type),e
        sys.exit()
    else:
        urls = fin.readlines()
        return urls

def get_data(data_cls,data_dir,area_codes_list):
    """
    根据选择来获取数据
    data_cls:数据分类
    data_dir:数据目录
    """    
    urls = load_urls(data_dir)
    cf = ConfigParser.ConfigParser()
    cf.read("stats_data.conf")
    
    time_pattern = ""
    try:
        time_pattern = cf.get("timepattern", data_cls)
    except Exception,e:
        print "配置文件timepattern获取错误".decode('utf-8').encode(type),e
        sys.exit()
        
    btime = ""
    try:
        btime = cf.get("begintime",data_cls)
    except Exception,e:
        print "配置文件begintime参数获取错误".decode('utf-8').encode(type),e
        sys.exit()
    #url中获取数据的时间
    btime = "&time=-1%2C" + btime + "&"

    time_patt = re.compile(time_pattern)
    #需要替换的检索地区
    select_pattern = re.compile('&selectId=\d{6}&')
    #日志文件
    log_file = open("url_error.txt","w")

    #为地区数据文件创建文件夹
    data_dir = os.path.join(data_dir,"data")
    for area_code in area_codes_list:
        print "当前处理地区:".decode('utf-8').encode(type),area_code
        
        area_dir = os.path.join(data_dir,area_code)
        if os.path.exists(area_dir):
            pass
        else:
            try:
                os.makedirs(area_dir)
            except  Exception,e:
                print area_dir,"文件夹创建失败".decode('utf-8').encode(type),e
                sys.exit()
        #获取数据
        file_no = 0
        for url in urls:
            file_no += 1
            if file_no%5==0:
                #print "正在获取第:".decode('utf-8').encode(type),file_no,"条数据".decode('utf-8').encode(type)
                sys.stdout.write("已经处理 ".decode('utf-8').encode(type)+str(file_no)+" 条记录".decode('utf-8').encode(type)+"\r")
            target_url = url
            target_area = "&selectId="+str(area_code)+"&"
            target_url = re.sub(time_patt,btime,target_url)
            target_url = re.sub(select_pattern,target_area,target_url)
            #等在0-3秒，防止被屏蔽
            #获取数据
            wait_time = 3*random.random()
            time.sleep(wait_time)
            try:
                page = urllib.urlopen(target_url)
                data = page.read()
            except Exception,e:
                log_file.write(url+"\n"+e+"\n")
            else:
                pass
            #下载数据
            try:
                file_name = str(file_no)+".dat"
                save_path  = os.path.join(area_dir,file_name)
                fin = open(save_path,"w")
                fin.write(data)
                fin.close()
            except Exception,e:
                print file_no,":",e
            else:
                #print file_no," 文件保存成功"
                pass        
        log_file.close()           
    return data_dir 
    
def letter_quarter(filename,foutname,patterns):
    """
        将包含年份字母的字段转化为年份 季度 ，如2004A  转化为 2004    一季度
    200401  转化为2004    1月份
    filename 文件名
    patterns 转换模式
    """
    foutname = os.path.join(os.path.dirname(filename),foutname)
    fout = open(foutname,"w")

    line_no = 0
    with open(filename) as f:
        for line in f:
            line_no += 1
            if line_no %1000 == 0:
                #print "处理数据".decode('utf-8').encode(type),line_no,"条".decode('utf-8').encode(type)
                sys.stdout.write("处理数据".decode('utf-8').encode(type)+str(line_no)+"条".decode('utf-8').encode(type)+"\r")
            items = line.split("\t")
            if len(items) != 7:
                print line,"格式不正确".decode('utf-8').encode(type)
            else:
                for k,v in patterns.iteritems():
                    #patt = "'"+k+"'"
                    pattern_str = re.compile(k)
                    #repl_str = "'"+v+"'"
                    if re.search(pattern_str, items[5]):
                        items[5] = re.sub(re.compile(k),v, items[5])
                        for i  in range(len(items)-1):
                            fout.write(items[i]+"\t")
                        fout.write(items[-1])
    fout.close()


def stats_data():
    
    print "[1]获取中国宏观年度数据".decode('utf-8').encode(type)
    print "[2]获取各省份年度数据".decode('utf-8').encode(type)
    print "[3]获取各省份季度数据".decode('utf-8').encode(type)
    print "[4]获取各身份月度数据".decode('utf-8').encode(type)
    
    data_dir_path = ""
    while True:
        sn = raw_input("输入对应的数字序号进行选择:".decode('utf-8').encode(type))
        if sn != '1' and sn != '2' and sn !='3' and sn != '4':
            continue
        print "确定".decode('utf-8').encode(type),
        print note_menu[sn].decode('utf-8').encode(type),"请输入y,否则请输入其他字符.输入0退出程序".decode('utf-8').encode(type)
        select = raw_input(":")
        if select == "y":
            current_dir = os.getcwd()
            data_dir_path = os.path.join(current_dir,data_dirs[sn])
            if os.path.exists(data_dir_path):
                pass
            else:
                try:
                    os.makedirs(data_dir_path)
                except  Exception,e:
                    print data_dir_path,"文件夹创建失败".decode('utf-8').encode(type),e
                    sys.exit()
            print "相关数据将会保存在:".decode('utf-8').encode(type),data_dir_path
            break
        elif select == '0':
            sys.exit()
        else:
            pass
    print "载入地区列表中".decode('utf-8').encode(type)
    area_code_dict  = load_dict("area_code", 0, [1])
    area_codes = area_code_dict.keys()
    if data_dirs[sn] == "hgnd":
        area_codes = ["000000"]
    else:                                                            #测试
        area_codes =  ['150000', '110000'] #测试
    print "地区列表为:".decode('utf-8').encode(type),area_codes
    #获取数据
    data_dir = get_data(data_dirs[sn],data_dir_path , area_codes)
    #data_dir = '/home/jay/workspace_new/stats_data/main/hgnd/data'
    print "获取数据完成".decode('utf-8').encode(type)
    #data_dir = '/home/jay/workspace_new/stats_data/main/fsyd/data'
    result_names   =  data_extract(data_dir)
    #填充地区名称
    indi_region_filename = merge(result_names[0],1, area_code_dict,"indicator_regionname.txt")
    #填充指标名称和单位
    indi_dict =  load_dict(result_names[1],0,[1,2])
    indi_regin_unit_filename = merge(indi_region_filename,0, indi_dict,"indicator_regionname_unit.txt")
    
    #indi_regin_unit_filename = '/home/jay/workspace_new/stats_data/main/fsyd/indicator_regionname_unit.txt'
    if data_dirs[sn] == "fsjd":
        print "拆分时间字段，转化为季度中..".decode('utf-8').encode(type)
        patterns = {"(\d{4})A":"\g<1>\t一季度","(\d{4})B":"\g<1>\t二季度","(\d{4})C":"\g<1>\t三季度","(\d{4})D":"\g<1>\t四季度"}
        letter_quarter(indi_regin_unit_filename, "indi_regin_unit_jidu.txt", patterns)
    elif data_dirs[sn] == "fsyd":
        print "拆分时间字段，转化为月度中..".decode('utf-8').encode(type)
        patterns = {"(\d{4})01":"\g<1>\t1月份",
                            "(\d{4})02":"\g<1>\t2月份",
                            "(\d{4})03":"\g<1>\t3月份",
                            "(\d{4})04":"\g<1>\t4月份",
                            "(\d{4})05":"\g<1>\t5月份",
                            "(\d{4})06":"\g<1>\t6月份",
                            "(\d{4})07":"\g<1>\t7月份",
                            "(\d{4})08":"\g<1>\t8月份",
                            "(\d{4})09":"\g<1>\t9月份",
                            "(\d{4})10":"\g<1>\t10月份",
                            "(\d{4})11":"\g<1>\t11月份",
                            "(\d{4})12":"\g<1>\t12月份",}
        letter_quarter(indi_regin_unit_filename, "indi_regin_unit_yuedu.txt", patterns)
    else:
        pass

if __name__ == "__main__":
    stats_data()
    print "数据处理完毕!   End!".decode('utf-8').encode(type)

