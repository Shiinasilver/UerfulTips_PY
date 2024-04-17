# Urllib库和Requests可以爬取绝大多数网站的数据 但是对于某些网站依然无能为力
# 有些网站强制使用HTTP/2.0协议访问 这种情况下Urllib和Request无法访问 因为它们只支持HTTP/1.1 不支持HTTP/2.0
# 我们可以使用一些支持HTTP/2.0的请求库就好了 比较有代表性的就算hyber 和 httpx 后者使用起来更加方便 功能也更加强大
import httpx
import requests

"""
url = 'https://spa16.scrape.center/'
response = requests.get(url)
print(response.text)
"""

# 这里会抛出ConnectTimeout异常其实是网络链接超时没办法 应该抛出的是RemoteDisconnected 错误
# 可能是没有设置请求头导致的 其实不是 真实原因的requests这个库使用是Http/1.1访问目标网站
# 而目标网站会检测请求使用的协议是不是HTTP/2.0 如果不是就拒绝返回任何结果
# 安装 pip install httpx
# 但是这样安装完的httpx是不支持HTTP/2.0的 如果想要支持可以安装
# pip install "httpx[http2]"
"""
httpx 和 requests 的很多API存在相似之处 下面是GET请求的用法
"""
response = httpx.get('https://www.httpbin.org/get')
print(response.status_code)
print(response.headers)
print(response.text)


response = httpx.get('https://spa16.scrape.center/')
print(response.text)
# 这里又报错了 和上面一样的错误 为什么呢 因为httpx默认不会开启对HTTP/2.0的支持 需要手动打开

# 打开HTTP/2.0
client = httpx.Client(http2=True)
response = httpx.get('https://spa16.scrape.center/')
print(response.text)


"""
httpx和requests有很多相似的API 上面实现的get请求 对于POST请求和PUT 和 DELETE实现方式也是类似
"""
r = httpx.get("https://httpbin.org/get",params={'name':'germey'})
r = httpx.post("https://httpbin.org/post",data={'name':'germey'})
r = httpx.put("https://httpbin.org/put")
r = httpx.delete("https://httpbin.org/delete")
r = httpx.patch("https://httpbin.org/patch")

"""
基于得到的response对象 可以使用如下属性和方法获取想要的内容
status_code:状态码
text:响应体的文本内容
content: 响应的二进制内容，当请求的目标是二进制数据（如图片）时，可以使用此属性获取。
headers:响应头，是headers对象，可以用像获取字典中的内容一样获取其中某个Header的值
json:方法 可以调用此方法将文本结果转化为JSON对象
"""

"""
Client对象
httpx中有一些基本的API和request中的非常相似 但也有一些API是不相似的 比如httpx中的Client对象
"""
with httpx.Client() as client:
    response = client.get('https://httpbin.org/get')
    print(response)
# 这个方法等价于
client = httpx.Client()
try:
    response = client.get("https://httpbin.org/get")
finally:
    client.close()
"""
两种方式的运行结果是一样的 只不过这里需要我们在最后显式地调用close方法来关闭client对象
在声明Client对时可以指定一些参数 例如headers 这样使用该对象发起的所有请求都会默认带上这些参数配置
"""

url = 'http://httpbin.org/headers'
headers = {'User-Agent': 'my-app/0.0.1'}
with httpx.Client(headers=headers) as client:
    r = client.get(url)
    print(r.json()['headers']['User-Agent'])