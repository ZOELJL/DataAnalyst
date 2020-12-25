import lxml.etree as le
'''
xpath 封装工具
传入参数：
    1、content :为 html 内容
    2、text : 为 xpath 文本内容
    3、default : 为 默认值 None
    
'''

# 对返回数据进行分隔符拼接得到想要的字符窜
def xpath_union(content,text,split,defalut=None):
    rets = le.HTML(content).xpath(text)
    data = split.join([ret.strip() for ret in rets])
    return data if data else  defalut

# 直接返回 无修饰 内容
def xpath_origin(content,text):
    data = le.HTML(content).xpath(text)
    return data

# 返回内容中的第一个元素
def xpath_first(content,text):
    rets = le.HTML(content).xpath(text)
    data = rets[0]
    return data if data else None