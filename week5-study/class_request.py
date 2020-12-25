import urllib.request as ur
import urllib.parse as up
kw = '美剧'
data ={
    'kw':kw,
    'ie':'utf-8',
    'pn':'100'
}
# url 编码
data_url = up.urlencode(data)
print(data_url)
# URL 解码
ret = up.unquote(data_url)
print(ret)

request = ur.Request('https://tieba.baidu.com/f?'+data_url)
response = ur.urlopen(request).read()
#print(response)
print(str(response,'utf-8'))

with open('%s.html' % kw,'wb') as f:
    f.write(response)
