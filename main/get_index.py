#!/usr/bin/env  python
#-*- coding=utf-8 -*-

import re

def get_index(urlsfilename="urls.txt"):
    fin = open(urlsfilename)
    urls = fin.readlines()
    m = re.compile('&index=([\w\d%]+)&')
    indexes_list = []
    for url in urls:
        g = re.search(m,url)
        indexex_str = g.group(1)
        indexes_list.append(indexex_str.split("%2C"))
    fout = open("index_list.dat","w")
    for indexes in indexes_list:
        fout.write(str(indexes)+"\n")
        #print str(indexes)
    fout.close()
    fin.close()



if __name__ == "__main__":
    get_index("urls.txt")