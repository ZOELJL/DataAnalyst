import re
with open('D:\ljl\practice\课件\第一章\第一章：数据提取与清洗策略【308705】re模块使用案例\\02.re模块使用案例\代码\\re模块使用案例\index.html','r',encoding='utf-8') as f:
    html = f.read()
    #print(html)
    html = re.sub('\n','',html)
    pattern_1 = '<div class="email">(.*?)</div>'
    ret_1 = re.findall(pattern_1,html)
    print(ret_1[0].strip())

password_pattern = r'^[a-zA-Z][a-zA-Z0-9_]{5,15}$'
pass1 = '1234567'
pass2 = 'k123456'
pass3 = 'k1123'
print(re.match(password_pattern,pass1))
print(re.match(password_pattern,pass2))
print(re.match(password_pattern,pass3))