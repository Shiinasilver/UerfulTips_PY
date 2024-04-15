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

# 这里首先实例化了一个HTTPBasicAuthHandler对象auth_handler 其参数是HTTPPasswordMgrWithDefaultRealm
# 对象,它利用add_password方法添加用户名和密码，这样就建立了一个用来处理验证的Handler类
#  然后将刚建立的auth_handler类当作参数传入build_opener方法，构建一个Opener，
# 这个Opener在发送请求时就相当于已经验证成功了
# 最后利用Opener类中的open方法打开链接，即可完成验证。