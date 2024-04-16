import logging

import requests
import urllib3

# disable_warnings()这个方法是用来忽略警告的方式 来屏蔽这个警告
urllib3.disable_warnings()
response = requests.get('http://ssr2.scrape.center/',verify=False)
print(response.status_code)

# 或者是通过捕获警告到日志的方式忽略警告
logging.captureWarnings(True)
response = requests.get('http://ssr2.scrape.center/',verify=False)
print(response.status_code)

# 我们也可以指定一个本地证书用作客户端证书 这可以是单个文件（包含密钥和证书）
# 或一个包含两个文件路径的元组
response = requests.get('http://ssr2.scrape.center/',cert=('/path/server.txt','/path/server.key'))
print(response.status_code)
# 上面的代码需要crt 和 key文件 并且指定它们的路径
# 另外注意本地私有证书key必须是解密状态 加密状态的key是不支持的1