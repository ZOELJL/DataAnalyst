import requests
from lxml import etree
import re
import urllib
import os
import zipfile
import shutil
import pandas as pd
from sqlalchemy import create_engine
import threading
from pathlib import Path
import pymysql
pymysql.install_as_MySQLdb()
import mysql.connector

## 解压文件  并同步写入状态
def unzipfile():
    filepath = './unpackedfile'
    ## 创建解压存放的文件夹
    os.mkdir(filepath)
    failnum = 0
    sucessnum = 0
    for zipfiles in os.listdir('./savefiles'):
        if not zipfiles.startswith('.'):  # 排除隐藏文件
            filedirectory = re.search('(.*?).zip', zipfiles).group(1)
            filecontents = zipfile.ZipFile('./savefiles/%s' % zipfiles, 'r')
            for file in filecontents.namelist():
                try:
                    # 解决解压文件中文乱码
                    newname = file.encode('cp437').decode('gbk')
                    filecontents.extract(file, '{}/{}'.format(filepath, filedirectory))
                    file = '%s/%s/%s' % (filepath, filedirectory, file)
                    newname = '%s/%s/%s' % (filepath, filedirectory, newname)
                    os.rename(file, newname)
                    sucessnum += 1
                except:
                    failnum += 1
                    print('该文件解压失败->',zipfiles)
                    continue
            # 多线程写入状态
            t2 = threading.Thread(target=write_status, args=([filedirectory]))
            t2.setDaemon(False)
            t2.start()
    print("失败解压文件数：%d" % failnum)
    print("成功解压文件数：%d" % sucessnum)


# 写入状态
def write_status(filename):
    status = re.match('(\w){4}',filename).group()
    writein = open('./unpackedfile/%s/status.txt'%filename,'w')
    writein.write(status)
    writein.close()

# 合并所有文件为一张表，并且写入数据库
def write_list(type):
    filepath = './unpackedfile'
    listdir = []
    dataframe = []
    for hide in os.listdir(filepath):
        if not hide.startswith('.'):
            listdir.append(hide)
    for i in listdir:
        i = os.path.join(filepath,i)
        for j in os.listdir(i):
            if re.search('[货物清单].*?.xls',j):
                if not j.startswith('.'):
                    excel = os.path.join(i,j)
                    #df = pd.read_excel(excel)
                    sheetall = pd.ExcelFile(excel)
                    status = open('%s/status.txt'%i,'r')
                    sta = status.read()
                    for sheet in sheetall.sheet_names:
                        colnum = 0  # 计量表头含有空列的数量
                        # 判断表头是否含有unamed 的空列
                        for col in list(sheetall.parse(sheet_name=sheet).columns):
                            if 'Unnamed' in col :
                                colnum +=1
                        # 如果含有Unamed的空列数量 大于3 就略过第一行，取第二行作为表头，否则取第一行作为表头
                        if  colnum >3 :
                            df = sheetall.parse(sheet_name=sheet,skiprows=1)
                        else:
                            df = sheetall.parse(sheet_name=sheet)
                        df['项目状态'] = sta
                        dataframe.append(df)
    dataall = pd.concat(dataframe)
    print(len(dataall.columns))
    col = ['包号','网省采购申请行号','项目单位','需求单位','项目名称','工程电压等级','物资名称','物资描述','单位','数量','交货日期','交货地点','备注','技术规范ID','项目状态']
    df3 = dataall[col]
    # 去除 包号列的空值的数据
    df4 = df3.dropna(subset=['包号'])
    print(df4.info())
    if type == '1':
    # 数据写入csv文件，保存在本地
        df4.to_csv('test.csv',encoding='utf_8_sig')
    else:
        # 数据存入数据库
        cur = create_engine('mysql://root:123456@localhost/spider?charset=utf8').connect()
        df4.to_sql(name='elec_spider', con=cur,index=False,if_exists='append')


# 爬取数据 并同步解压
def spider(begin):
    # try:
    #     os.mkdir('./savefiles')  # 创建文件夹存放下载的招标文件
    # except:
    #     print('已经存在，不需要重复创建')
    filepath = './savefiles'
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    else:
        shutil.rmtree(filepath)
        os.mkdir(filepath)
    # 设置计数变量
    globalf = 0
    globalg = 0

    # 循环页码
    for i in range(begin, 10):
        url = 'http://ecp.sgcc.com.cn/ecp1.0/project_list.jsp?site=global&column_code=014001001&project_type=%d' % i
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
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
        #print('第%d页下载成功%d份标书' %(i, locala))
        print('第%d页下载完成' % i)
        #print('截止此刻下载成功%d份标书' % globalf)
        print('全部下载成功文件数量：', globalf)
        print('全部下载失败文件数量：', globalg)
    # 数据全部下载之后，再开始解压
    print("数据下载完毕，现在开始解压。")
    unzipfile()
    # 数据爬取解压完成后，合并
    print("数据解压完毕，现在开始处理并存储。")
    way = input("请选择最终数据存储方式：1 csv文件； 2 mysql 数据库 ")
    write_list(way)
    print("数据处理完毕")


if __name__ == "__main__":
    begin = input("请输入起始页码： ")
    spider(int(begin))
    #unzipfile()



