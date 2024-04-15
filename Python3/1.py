from urllib.parse import urlsplit, urlunsplit

result = urlsplit("https://www.baidu.com/index.html;user?id=5#comment")
print(result.scheme,result[0])

data = ['https','www.baidu.com','index.html','a=6','comment']
print(urlunsplit(data))