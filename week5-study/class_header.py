import urllib.request as ur

proxy_address = ur.urlopen('').read().trip()
print(proxy_address)


proxy_handler = ur.ProxyHandler({
    'http':proxy_address
})

# 创建opener 对象
proxy_opener = ur.build_opener(proxy_handler)

