# 在访问某些网站的时候 例如https://ssr3.scrape.center 可能会弹出认证窗口
# 遇到这种情况 就表示这个网站启用了基本身份认证  英文名叫做 HTTP Basic Access Authentication
# 这是一种登陆验证方式 允许网页浏览器或者其他客户端程序在请求网站时提供用户名和口令形式的身份凭证
from urllib.error import URLError
from urllib.request import HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler, build_opener
import requests
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth1

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


# 这个网站启用的基本身份认证 我们利用urllib库来实现身份的校验 但是实现起来相对繁琐
# 我们可以用requests库里的身份认证功能 通过auth参数即可设置
r = requests.get('https://ssr3.scrape.center',auth=HTTPBasicAuth('admin','admin'))
print(r.status_code)

# 此外 request库还提供了其他认证方式 如OAuth认证 不过此时需要安装oauth包
# pip install requests_oauthlib
url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1('YOUR API KEY','YOUR_APP_SECRET','USER_OAUTH_TOKEN','USER_OAUTH_TOKEN_SECRET')
requests.get(url, auth=auth)
