import lxml.etree as le

with open('D:\ljl\practice\课件\第一章\第一章：数据提取与清洗策略【308708】Python中的lxml模块\\05.Python中的lxml模块\代码\Python中的lxml模块\edu.html','r',encoding='utf-8') as f:
    html = le.HTML(f.read())
   # print(html)
    categorys = html.xpath('//div[@class="classify_cList"]')
    print(categorys)
    datas = []
    for category in categorys:
        title = category.xpath('./h3/a/text()')
        course = category.xpath('./div/span/a/text()')
        datas.append(dict(
            title = title,
            course = course
        ))
    for data in datas:
        print(data.get('title')[0])
        for item in data.get('course'):
            print('   ',item)
