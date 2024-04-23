import json
import logging
import multiprocessing
import re
from os import makedirs
from os.path import exists
from urllib.parse import urljoin
import requests


# 定义一些基本参数
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s-%(levelname)s: %(message)s')
BASE_URL = 'https://ssr1.scrape.center'
TOTAL_PAGE = 10
RESULTS_DIR = 'RESULT_DIR'
exists(RESULTS_DIR) or makedirs(RESULTS_DIR)


# 这里我们引入了requests库来爬取页面 logging库用来输出信息 re库用来实现正则表达式解析
# urljoin模块用来做URL的拼接
# 接着我们定义了日志输出级别和输出格式 以及BASE_URL 为当前站点的根URL
# TOTAL_PAGE为需要爬取的总页码数量

# 考虑到不仅要爬取列表页 还要爬取详情页
# 我们在这里定义了一个较通用的爬取页面的方法 叫做scrape_page
# 它接收了一个参数url 返回页面的HTML代码
# 首先判断代码是不是200， 如果是 就直接返回页面的HTML代码
# 如果不是 则输出错误日志信息
# 另外在这里实现了requests的异常处理 如果出现了爬取异常
# 就输出对应的错误日志信息 我们将logging 库中的error方法里的exc_info参数设为True 可以打印出Traceback错误信息
def scrape_page(url):
    logging.info('scraping %s...', url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        logging.error('get invalid status code %s while scraping %s',
                      response.status_code, url)
    except requests.RequestException:
        logging.error('error occurred while scraping %s', url,
                      exc_info=True)

# scrape_index 在这个方法里面实现列表页的URL拼接
# 然后调用scrape_page方法爬取即可
def scrape_index(page):
    index_url = f'{BASE_URL}/page/{page}'
    return scrape_page(index_url)

# 获取HTML之后 下一步就算解析列表页 并得到每部电影的详情页的URL
# 这里我们定义了parse_index 方法 它接收了一个参数html 即列表页的HTML代码
# 在parse_index 方法中 我们定义了一个提取标题超链接href属性的正则表达式
# <a.*?href="(.*?)".*?class="name">
# 其中我们使用非贪婪通用匹配 .*?来匹配任意字符 同时在href属性的引号之间使用了分组匹配（.*?）正则表达式
# 这样我们便能在匹配结果里面获取href的属性值 正则表达式后面紧跟着class = ’name‘，用来表示这个<a>节点是代表电影名称的节点
# 现在有了正则表达式 如何提取页面所有href的值呢？
# 使用re库的findall方法就可以了
# 第一个参数传入这个正则表达式结构的pattern对象 第二个参数传入html 这样findall方法便会搜索html中所有能与该正则表达式相匹配的内容
# 之后把匹配的结果返回并赋值为ITEM
# 如果items为空 那么可以直接返回空列表 如果items不为空 那么直接遍历处理即可
# 遍历items得到的item就算我们在上文所说的类似/detail/1这样的结果
# 由于这并不是一个完整的URL 所以需要借助urljoin方法把BASE_URL 和href拼接在一起 获得详情页的完整URL
# 得到完整的URL 最后调用yield返回即可
def parse_index(html):
    pattern = re.compile('<a.*?href="(.*?)".*?class="name">')
    items = re.findall(pattern,html)
    if not items:
        return []
    for item in items:
        detail_url = urljoin(BASE_URL, item)
        logging.info('get detail url %s', detail_url)
        yield detail_url

# 已经可以成功抓取所有详情页的URL 下一步就算解析详情页
# 下面定义一个详情页的爬取方法
# 有个疑问 这个scrape_detail方法里面只调用了scrape_page方法 而没有别的功能
# 那爬取详情直接用scrape_page方法 不就好了 还有必要在单独定义scrape_detail方法嘛？
# 有必要
# 单独定义一个scrape_detail方法在逻辑上会显得更清晰 而且以后如果想对scrape_detail方法进行改动
# 例如添加日志输出、增加预处理、都可以在scrape_detail里实现 而不用改动scrape_page 方法，灵活性更好
def scrape_detail(url):
    return scrape_page(url)

def parse_detail(html):
    """
    parse detail page
    :param html: html of detail page
    :return: data
    """

    cover_pattern = re.compile(
        'class="item.*?<img.*?src="(.*?)".*?class="cover">', re.S)
    name_pattern = re.compile('<h2.*?>(.*?)</h2>')
    categories_pattern = re.compile(
        '<button.*?category.*?<span>(.*?)</span>.*?</button>', re.S)
    published_at_pattern = re.compile('(\d{4}-\d{2}-\d{2})\s?上映')
    drama_pattern = re.compile('<div.*?drama.*?>.*?<p.*?>(.*?)</p>', re.S)
    score_pattern = re.compile('<p.*?score.*?>(.*?)</p>', re.S)

    cover = re.search(cover_pattern, html).group(
        1).strip() if re.search(cover_pattern, html) else None
    name = re.search(name_pattern, html).group(
        1).strip() if re.search(name_pattern, html) else None
    categories = re.findall(categories_pattern, html) if re.findall(
        categories_pattern, html) else []
    published_at = re.search(published_at_pattern, html).group(
        1) if re.search(published_at_pattern, html) else None
    drama = re.search(drama_pattern, html).group(
        1).strip() if re.search(drama_pattern, html) else None
    score = float(re.search(score_pattern, html).group(1).strip()
                  ) if re.search(score_pattern, html) else None
    return {
        'cover': cover,
        'name': name,
        'category': categories,
        'published_at': published_at,
        'drama': drama,
        'score': score
    }

def save_data(data):
    name = data.get('name')
    date_path = f'{RESULTS_DIR}/{name}.json'
    json.dump(data,open(date_path,'w',encoding='utf-8'),ensure_ascii=False,indent=2)

def main(page):
    """
    main process
    :return:
    """
    index_html = scrape_index(page)
    detail_urls = parse_index(index_html)
    for detail_url in detail_urls:
        detail_html = scrape_detail(detail_url)
        data = parse_detail(detail_html)
        logging.info('get detail data %s', data)
        logging.info('saving data to json file')
        save_data(data)
        logging.info('data saved successfully')


if __name__ == '__main__':
    pool = multiprocessing.Pool()
    pages = range(1, TOTAL_PAGE + 1)
    pool.map(main, pages)
    pool.close()