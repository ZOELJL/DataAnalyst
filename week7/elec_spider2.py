import requests
from lxml import etree
import re
import urllib
import os
import zipfile
import shutil

def spider(begin):
    try:
        os.mkdir('./savefiles')  # 创建文件夹存放下载的招标文件
    except:
        print('已经存在，不需要重复创建')

    # 设置计数变量
    globalf = 0
    globalg = 0

    # 循环页码
    for i in range(begin, 3):
        url = 'http://ecp.sgcc.com.cn/ecp1.0/project_list.jsp?site=global&column_code=014001001&project_type=%d' % i
        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }
        response = requests.get(url=url, headers=header)
        xpathtree = etree.HTML(response.text)
        res = xpathtree.xpath('//tr[@align="left"]')
        if len(res) == 0:
            print('第%d页获取数据失败，跳过此页'%i)
            continue
        else:
            del res[0]
        locala = 0
        for resi in res:
            try:
                str1 = resi.xpath('./td[@class="black40"]/a/@onclick')[0]
                num = re.search('showProjectDetail\((.*?),\'(.*?)\'\);', str1)
                num = num.group(2)
                url2 = 'http://ecp.sgcc.com.cn/ecp1.0/html/project/014001001/%s.html' % num
                response2 = requests.get(url=url2, headers=header)
                projectstatus = etree.HTML(response2.text).xpath('//tr/td/text()')[1]  # //td[2]
                projectstatus = re.search('(\S+.*?)', projectstatus).group(1)
                projectname = etree.HTML(response2.text).xpath('//td[2]/text()')[2]
                projectname = projectstatus+projectname  # 使文件名打上状态标签
                url3 = etree.HTML(response2.text).xpath('//td/a/@href')[0]
                originalurl = 'http://ecp.sgcc.com.cn'
                downloadurl = originalurl + url3
            except:
                print('本页面有问题', url2)

            try:
                urllib.request.urlretrieve(url=downloadurl, filename='./savefiles/%s.zip' % projectname)
                globalf += 1
                locala += 1
            except:
                globalg += 1
                print('这个地址下载失败', downloadurl)
                continue  # 下载失败则跳过 继续下载
        print('第%d页下载成功%d份标书' %(i, locala))
        print('第%d页下载完成' % i)
        print('截止此刻下载成功%d份标书' % globalf)

        print('全部下载成功文件数量：', globalf)
        print('全部下载失败文件数量：', globalg)

## 解压文件
def unzipfile():
    filepath = './unpacked'

    ## 如果解压文件夹不存在就创建，如果存在就先清空再创建
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    else:
        shutil.rmtree(filepath)
        os.mkdir(filepath)

    failnum = 0
    sucessnum = 0
    for zipfiles in os.listdir('./savefiles'):
        if not zipfiles.startswith('.'):  # 排除隐藏文件

            filedirectory = re.search('(.*?).zip', zipfiles).group(1)
            print(filedirectory)
            filecontents = zipfile.ZipFile('./savefiles/%s' % zipfiles, 'r')
            for file in filecontents.namelist():
                if not os.path.isfile(file):
                    print(file)
                try:
                    print(file)
                    newname = file.encode('cp437').decode('gbk')
                    print(newname)
                    filecontents.extract(file, '{}/{}' .format(filepath,filedirectory) )
                    file = '%s/%s/%s' % (filepath,filedirectory, file)
                    newname = '%s/%s/%s' % (filepath,filedirectory, newname)
                    os.rename(file,newname)
                    sucessnum += 1
                except:
                    failnum +=1
                    print('这个文件解压失败 {}'.format(zipfiles))
                    continue

    print("失败解压文件数：%d"%failnum)
    print("成功解压文件数：%d"%sucessnum)

if __name__ == "__main__":
    # print("准备爬取电网招标文书。")
    # start = input("请输入爬取起始页码：")
    # spider(int(start))
    unzipfile()

