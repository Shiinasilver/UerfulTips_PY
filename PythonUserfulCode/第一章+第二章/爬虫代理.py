# 在做爬虫的时候，免不了要使用代理，如果要添加代理
from urllib.error import URLError
from urllib.request import ProxyHandler, build_opener

proxy_handler = ProxyHandler({
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'
})
opener = build_opener(proxy_handler)
try:
    response = opener.open('http://www.baidu.com')
    print(response.read().decode('utf-8'))
except URLError as e:
    print(e.reason)

# 这里我们需要事先在本地搭建一个HTTP代理 并且让其运行在8080端口上
# 上面使用的ProxyHandler 其参数是一个字典 键名是协议类型（例如HTTP或者是HTTPS等）
# 键值是代理链接，也可以添加多个代理
