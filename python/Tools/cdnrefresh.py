#-*- coding:UTF-8 -*-
__author__ = 'icestar'
import urllib, urllib2,cookielib
import time
import sys

if len(sys.argv) < 2:
    print "请输入url"
    print "python  urls"
    sys.exit(1)


#刷新路径
path = sys.argv[1]

#设置urllib
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

#R4API提交地址
url_commit = "https://r.chinacache.com/content/refresh"


#刷新字符串
json ='{"dirs":["http://%s"]}'%path
params=urllib.urlencode({'username':'zzsf', 'password': 'rzcdn.1234', 'task' : json})
req = urllib2.Request(url_commit, params)
res = urllib2.urlopen(req)

#获取r_id
result = eval(res.read())

print "commid url:",url_commit + "?" + params
print "result:\n", result

r_id = result['r_id']

#查询地址
url_query = "https://r.chinacache.com/content/refresh/%s"%r_id
params=urllib.urlencode({'username':'zzsf', 'password': 'rzcdn.1234'})
url_query = url_query + "?" + params

print "query url:", url_query

while True:
    urllib2.install_opener(opener)
    reponse = urllib2.urlopen(url_query)
    result = reponse.read()
    result = result.replace("null", "None")
    result = eval(result)

    print result

    if result['status'] == 'status':
        break

    time.sleep(30)
