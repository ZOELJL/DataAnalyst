import urllib.request as ur
import user_agent
import re
import json
import xpath_tool as xt
import pymongo
import mysql.connector

# mac 使用urllib.request 会有ssl证书问题 故加入
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


# 输入url 获取html
def get_html(url):
    req = ur.Request(
        url=url,
        headers={
            'User-Agent': user_agent.get_user_agent_pc()
        }
    )
    content = ur.urlopen(req).read().decode('gbk', 'ignore')
    return content if content else None


# 第一级列表页面数据爬取
def parse1(keyword,page):
    url = 'https://search.51job.com/list/010000,000000,0000,00,9,99,{keyword},2,{page}.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='.format(
        keyword=keyword,
        page=page
    )
    content = get_html(url)
    data = json.loads(re.findall('window.__SEARCH_RESULT__ = (.*?)</script>', content)[0])
    results = data['engine_search_result']
    return results


# 第二级职位详细页面数据获取
def parse2(url):
    content = get_html(url)
    xpath_job = '//div[@class="tCompany_main"]/div[@class="tBorderTop_box"][1]//text()'
    xpath_phone = '//div[@class="tCompany_main"]/div[@class="tBorderTop_box"][2]//text()'
    xpath_company = '//div[@class="tCompany_main"]/div[@class="tBorderTop_box"][3]//text()'
    parse2_job = xt.xpath_union(content=content, text=xpath_job, split='\n')
    parse2_phone = xt.xpath_union(content=content, text=xpath_phone, split='\n')
    parse_company = xt.xpath_union(content=content, text=xpath_company, split='\n')
    return dict(
        parse2_job=parse2_job,
        parse2_phone=parse2_phone,
        parse_company=parse_company
    )


# 爬取数据，且将二级页面获取的数据并入获取的一级数据中
def spider_job(keyword,start_page = 1,end_page = 100):
    parse1_results={}
    for page in range(start_page,end_page+1):
        parse1_results = parse1(keyword=keyword, page=page)
        for parse1_result in parse1_results:
            parse2_data = parse2(parse1_result['job_href'])
            parse1_result['parse2_job'] = parse2_data['parse2_job']
            parse1_result['parse2_phone'] = parse2_data['parse2_phone']
            parse1_result['parse_company'] = parse2_data['parse_company']
            #print(parse1_result)
        #result_list.append(parse1_results)
    return parse1_results

# 爬取的数据插入mysql 数据库中
def mysql_store(data):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="123456",
        database="spider"
    )
    mycursor = mydb.cursor()
    sql = "INSERT INTO 51job ( jobid,coid,job_href,job_name,job_title,company_href,company_name,providesalary_text,workarea,workarea_text,updatedate,companytype_text,degreefrom,workyear,issuedate,jobwelf,companysize_text,companyind_text,parse2_job,parse2_phone,parse_company) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    infos = []
    for info in data:
        # 获取所需字段存入list  因并非所有字段都有用，故存入数据库中的只有选取列部分数据
        info_list = [
            info['jobid'], info['coid'], info['job_href'], info['job_name'], info['job_title'], info['company_href'],
            info['company_name'], info['providesalary_text'], info['workarea'], info['workarea_text'],
            info['updatedate'], info['companytype_text'], info['degreefrom'], info['workyear'], info['issuedate'],
            info['jobwelf'], info['companysize_text'], info['companyind_text'], info['parse2_job'],
            info['parse2_phone'], info['parse_company']
        ]
        # 将所需字段的list转成tuple 再存入另一个list中，构成批量插入的值
        infos.append(tuple(info_list))
    #print(infos)
    #sqlcnn.insert(infos)
    mycursor.executemany(sql, infos)
    mydb.commit()
    print("mysql数据库插入成功！")

# 爬取的数据插入mongodb数据库中
def mongo_store(data):
    client = pymongo.MongoClient()
    db = client.get_database('spider')
    c = db.get_collection('51job')
    c.insert_many(data)
    print('mongodb数据库插入成功！')


if __name__ == '__main__':
    keyword = input("请输入要爬取的职位：")
    start_page = input("请输入爬取的起始页面：")
    end_page = input("请输入爬取的截止页面：")
    database = input("存入mysql请按1，存入mongodb请按2 :")
    print("开始爬取......")
    job_info = spider_job(keyword,start_page=int(start_page),end_page=int(end_page))
    if(database == '1'):
        mysql_store(job_info)
    else:
        mongo_store(job_info)
    print("爬取成功～ 请到数据库查看您的数据哟～亲")
