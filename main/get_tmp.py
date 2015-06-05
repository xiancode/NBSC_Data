#!/usr/bin/env  python
#-*- coding=utf-8 -*-

import re

def get_index(urlsfilename="urls.txt"):
    fin = open(urlsfilename)
    urls = fin.readlines()
    tmp_list = []
    m = re.compile('&tmp=(\d+)&')
    for url in urls:
        g = re.search(m,url)
        tmp_list.append(g.group(1))
    fout = open("url_tmp.dat","w")
    for tmp_num in tmp_list:
        fout.write(tmp_num+"\n")
    fout.close()
    fin.close()



if __name__ == "__main__":
    get_index("urls.txt")