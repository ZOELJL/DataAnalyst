import requests
import json

url = 'https://ecp.sgcc.com.cn/ecp2.0/ecpwcmcore//index/noteList'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
}

param = {
    'firstPageMenuId': "2018032700291334",
    'index': 1,
    'key': "",
    'orgId': "",
    'purOrgCode': "",
    'purOrgStatus': "",
    'purType': "",
    'size': 20,
}
response = requests.post(url=url,data=json.dumps(param),headers=header)
# str 转 dict
res = json.loads(response.text)
noteList = res['resultValue']['noteList']
for item in noteList:
    noticeId = item['noticeId']
    url2 = 'https://ecp.sgcc.com.cn/ecp2.0/portal/#/doc/doci-bid/%s_2018032700291334'%noticeId
    res2 = requests.get(url=url2,  headers=header)
    print(res2.text)
