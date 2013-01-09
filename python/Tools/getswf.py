#-*- coding:utf-8 -*-
__author__ = 'icestar'


import os
import urllib


fileFormat = [
    'swf',
    'jpg',
    'png',
    'dds',
    'do'

]


def downloadswf(url, foldname, filename):
    try:
        f = urllib.urlopen(url)
        sb = f.read(-1)
        f.close()
        f1 = open(foldname + "/" + filename, "wb")
        f1.write(sb)
        f1.close()

    except Exception as e:
        print e




if __name__ == '__main__' :
    with open("urls", "r") as urls:
        for line in urls:
            url =  line.split("?")[0]
            format = url.split(".")[-1]
            if format in fileFormat:
                name = url.split("/")[-1]
                print "download ", name
                downloadswf(url, "E:\\res\\djj", name)



    #