import re
with open('D:\ljl\practice\课件\第一章\第一章：数据提取与清洗策略【308706】实战：提取商城分类结构\\03.提取商城分类结构\代码\提取商城分类结构\static\html\index.html','r',encoding='utf-8') as f:
    html = re.sub('\n','',f.read())
    courses_pattern = '<section class="main_section">(.*?)</section>'
    cname_pattern = '<span class="course_name">(.*?)</span>'
    ctitle_pattern = '<h1>(.*?)</h1>'
    courses = re.findall(courses_pattern,html)
    datas = []
    for title in courses:
        course_title = re.findall(ctitle_pattern,title)[0]
        course_name = re.findall(cname_pattern,title)
        datas.append(
            {
                'title':course_title,
                'name':course_name
            }
        )
    print(datas)
    for data in datas:
        print(data.get('title'))
        for item in data.get('name'):
            print('    ',item)
    #print(courses_title)


