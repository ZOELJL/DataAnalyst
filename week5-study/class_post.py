import urllib.request as ur
import urllib.parse as up
import json

word =input('请输入要翻译的单词：')
data = {
    'kw':word
}

data_url = up.urlencode(data)
request = ur.Request(
    url ='https://fanyi.baidu.com/sug',
    data = data_url.encode('utf-8')
)

response = ur.urlopen(request).read()

ret = json.loads(response)
#print(ret)
print(ret['data'][0]['v'])