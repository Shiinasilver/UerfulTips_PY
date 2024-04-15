# 在访问某些网站的时候 例如https://ssr3.scrape.center 可能会弹出认证窗口
# 遇到这种情况 就表示这个网站启用了基本身份认证  英文名叫做 HTTP Basic Access Authentication
# 这是一种登陆验证方式 允许网页浏览器或者其他客户端程序在请求网站时提供用户名和口令形式的身份凭证
from urllib.error import URLError
from urllib.request import HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler, build_opener

username = 'admin'
password = 'admin'
url = 'https://ssr3.scrape.center/'

p = HTTPPasswordMgrWithDefaultRealm()
p.add_password(None,url,username,password)
auth_handler = HTTPBasicAuthHandler(p)
opener = build_opener(auth_handler)

try:
    result = opener.open(url)
    html = result.read().decode('utf-8')
    print(html)
except URLError as err:
    print(err.reason)