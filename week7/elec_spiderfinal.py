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

## 解压文件  并同步写入状态
def unzipfile(filename):
    filepath = './unpackedtest'
    ## 如果解压文件夹不存在就创建，如果存在就先清空再创建
   #shutil.rmtree(filepath)
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    else:
        shutil.rmtree(filepath)
        os.mkdir(filepath)

    filecontents = zipfile.ZipFile('./savefiles/%s' % filename, 'r')
    print(filecontents.namelist())
    for file in filecontents.namelist():
        try:
            print(file)
            newname = file.encode('cp437').decode('gbk')
            print(newname)
            filecontents.extract(file, '{}/{}'.format(filepath, filename))
            file = '%s/%s/%s' % (filepath, filename, file)
            newname = '%s/%s/%s' % (filepath, filename, newname)
            os.rename(file, newname)
        except:
            print('该文件解压失败->',filename)
            continue
    # 多线程
    t2 = threading.Thread(target=write_status, args=([filename]))
    t2.setDaemon(False)
    t2.start()

# 解压文件  并同步写入状态
def unzipfile_forpath(fn):
    filename = '%s.zip'%fn
    filepath = './unpackedtest'
    ##
# 如果解压文件夹不存在就创建，如果存在就先清空再创建
   #shutil.rmtree(filepath)
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    else:
        shutil.rmtree(filepath)
        os.mkdir(filepath)
    #
    # filecontents = zipfile.ZipFile('./savefiles/%s' % filename, 'r')
    # print(filecontents.namelist())
    with zipfile.ZipFile('./savefiles/%s' % filename, 'r') as f:
        for file in f.namelist():
            extracted_path = Path(f.extract(file,'{}/{}'.format(filepath, fn)))
            print(file)

            newfile = file.encode('cp437').decode('gbk')
            newfile = '{}/{}/{}'.format(filepath, fn,newfile)
            print(newfile)
            extracted_path.rename(newfile)

    # 多线程
    # t2 = threading.Thread(target=write_status, args=([filename]))
    # t2.setDaemon(False)
    # t2.start()




# 写入状态
def write_status(filename):
    status = re.match('(\w){4}',filename).group()
    writein = open('./unpackedtest/%s/status.txt'%filename,'w')
    writein.write(status)
    writein.close()



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
    for i in range(begin, 3):
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
                # 多线程进行解压
                filename = '{}.zip'.format(projectname)
                t1 = threading.Thread(target=unzipfile,args=([filename]))
                t1.setDaemon(False)
                t1.start()
            except:
                globalg += 1
                print('这个地址下载失败', downloadurl)
                continue  # 下载失败则跳过 继续下载
        #print('第%d页下载成功%d份标书' %(i, locala))
        print('第%d页下载完成' % i)
        #print('截止此刻下载成功%d份标书' % globalf)
        print('全部下载成功文件数量：', globalf)
        print('全部下载失败文件数量：', globalg)


# 将状态写入货物清单
def write_list():
    filepath = './unpacked'
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
                        #print(colnum)
                        # 如果含有Unamed的空列数量 大于3 就略过第一行，取第二行作为表头，否则取第一行作为表头
                        if  colnum >3 :
                            df = sheetall.parse(sheet_name=sheet,skiprows=1)
                        else:
                            df = sheetall.parse(sheet_name=sheet)
                        #print(df.columns)
                        df['项目状态'] = sta
                        dataframe.append(df)
    dataall = pd.concat(dataframe)
    print(len(dataall.columns))
    col = ['包号','网省采购申请行号','项目单位','需求单位','项目名称','工程电压等级','物资名称','物资描述','单位','数量','交货日期','交货地点','备注','技术规范ID','项目状态']
    df3 = dataall[col]
    #print(df3.info())
    # 去除 包号列的空值的数据
    df4 = df3.dropna(subset=['包号'])
    print(df4.info())
    # 数据写入csv文件，保存在本地
    df4.to_csv('test.csv')
    # 数据存入数据库

    cur = create_engine('mysql://root:123456@localhost/test?charset=utf-8').connect()
    df4.to_sql(name='df4', con=cur)

# 保存
def save_sql():
    cur = create_engine('mysql://root:123456@localhost/test?charset=utf-8').connect()
    df4.to_sql(name='df4',con=cur)



if __name__ == "__main__":
    filename1 = '已经截标国网福建省电力有限公司福建南平太阳电缆股份有限公司10MW分布式光伏发电项目配套物资采购'
    filename = '已经截标国网信息通信产业集团有限公司2020年第三批集中采购项目公开招标（物资）'
    unzipfile_forpath(filename)


