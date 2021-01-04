import requests
import json
import urllib

# mac 使用urllib.request 会有ssl证书问题 故加入
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

listDataUrl = 'https://ecp.sgcc.com.cn/ecp2.0/ecpwcmcore//index/noteList'
listPageUrl = 'https://ecp.sgcc.com.cn/ecp2.0/portal/#/list/list-spe/2018032600289606_1_2018032700291334'
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


## 使用requests库
data_res = requests.post(url=listDataUrl,data=json.dumps(param),headers=header)
print(data_res.text)
# str 转 dict
res = json.loads(data_res.text)

noteList = res['resultValue']['noteList']
for item in noteList:
    noticeId = item['noticeId']
    projectstatus = item['prjStatus']  # 招标状态  1 正在招标  0 已经截止
    url2 = 'https://ecp.sgcc.com.cn/ecp2.0/portal/#/doc/doci-bid/%s_2018032700291334'%noticeId
    url22 = 'https://ecp.sgcc.com.cn/ecp2.0/ecpwcmcore//index/getNoticeBid'

    #res2 = requests.post(url=url22, data=str(noticeId), headers=header)
    res2 = requests.get(url=url2, headers=header)
    print(res2.text)


