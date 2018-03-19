import re
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import pymongo
from config import *

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

def get_url_function(url):
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        if r.status_code == 200:
            return r.text
        return None
    except RequestException:
        return None

def parser_html_function(html):
    pattern = re.compile('<li.*?indexBody">.*?review/">(.*?)</a>.*?<b>(.*?)</b>.*?info"></span>(.*?)</p>.*?</div>'
                         +'.*?datetime=.*?>(.*?)</time>.*?scoreBox"><span>(.*?)</span>(.*?)</div>.*?</li>', re.S)
    result = re.findall(pattern, html)
    for item in result:
        yield{
            '游戏名称':item[0],
            '游戏类型':item[1],
            '游戏简介':item[2],
            '评测日期':item[3],
            '游戏评分':item[4],
            '总体评价':item[5]
        }

def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('成功')
    except Exception:
        print('失败')


if __name__ == '__main__':
    url ='http://www.ign.xn--fiqs8s/article/review?page='
    for i in range(1,14):
        urlt = url + str(i)
        response = get_url_function(urlt)
        final_response = parser_html_function(response)
        for item in final_response:
            print(item)
            save_to_mongo(item)