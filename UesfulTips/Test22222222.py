from urllib import parse, request

url = 'http://www.httpbin.org/post'
headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT)',
    'host': 'www.httpbin.org'
}
dict = {'name':'germey'}
data = bytes(parse.urlencode(dict), encoding='utf-8')
req = request.Request(url = url,data = data,headers=headers,method='POST')
response = request.urlopen(req)
print(response.read().decode('utf-8'))