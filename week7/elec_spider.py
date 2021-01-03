import requests

import urllib.request
# mac 使用urllib.request 会有ssl证书问题 故加入
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


url="https://ecp.sgcc.com.cn/ecp2.0/portal/#/doc/doci-bid/2020123197948534_2018032700291334"
file=urllib.request.urlopen(url)
print('获取当前url:',file.geturl() )
print('file.getcode,HTTPResponse类型:',file.getcode )
#print('file.info 返回当前环境相关的信息：' ,file.info())
print(file.info())
