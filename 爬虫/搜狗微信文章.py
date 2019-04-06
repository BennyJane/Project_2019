#encoding='utf-8'
#2019-4-06
from urllib.parse import urlencode
import pymongo
import requests
from lxml.etree import XMLSyntaxError
from requests.exceptions import ConnectionError
from pyquery import PyQuery as pq
from config import *

client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_DB]

base_url = 'https://weixin.sogou.com/weixin?query={}&type=2&page={}'
#base_url="https://weixin.sogou.com/weixin?oq=&query={}&_sug_type_=1&sut=0&lkt=0%2C0%2C0&s_from=input&ri=0&_sug_=n&type=3&sst0=1554520170909&page={}&ie=utf8&p=40040108&dp=1&w=01015002&dr=1"

#每爬取45—50個列表左右，就會封IP；需要手動輸入驗證碼，并更新cookies
headers = {
    'Cookie': 'SUID=0EA04B2F1508990A000000005CA4C45C; SUV=00DE67642F4BA00E5CA4C45CFB052740; ld=8Zllllllll2tItyVlllllVhOeuZlllllL7QB$kllllwlllllxllll5@@@@@@@@@@; ABTEST=6|1554517983|v1; JSESSIONID=aaa9B-Ocg-CtxaTsFJCNw; weixinIndexVisited=1; ppinf=5|1554520058|1555729658|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxOkF8Y3J0OjEwOjE1NTQ1MjAwNTh8cmVmbmljazoxOkF8dXNlcmlkOjQ0Om85dDJsdUtCRmN6c3ZVNGp6Sm41SGZrOTdzcGNAd2VpeGluLnNvaHUuY29tfA; pprdig=OzAU-Ngg9w4erDwrPbK2uYE3z8uAr7McXUKd00qCtvu3iH4Dw26PjgkW-H2s0cA3iTi39H98sthcB6dCQv4QNpvD7nM0FRJr4xNm7gEdjsCL42dimjgM88nVEaASDT-H_hs5ahvS9jmYkRheQl1jVJJFy5Gk3OBHDe5og16MiXM; sgid=07-37847289-AVyoFicq8VF3gQicYv9KvJ2uE; sct=1; PHPSESSID=mt8q8gm9s5juc4ef3rvhauig92; IPLOC=CN8100; ppmdig=1554526590000000b87feded89fce703beabf29a2b360ff4; SNUID=15BC50331C1E99CEBE0E1F9D1CF65A81; seccodeRight=success; successCount=1|Sat, 06 Apr 2019 05:16:18 GMT',
    'Host': 'weixin.sogou.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.127'
}



def get_html(url, count=1):
    print('Crawling', url)
    print('Trying Count', count)
    #全局变量的使用，现在函数、类外面定义变量，在用的地方用Global调用
    try:
        response = requests.get(url, allow_redirects=False, headers=headers)
        #print(response.text)
        if response.status_code == 200:
            return response.text
        if response.status_code == 302:
            #Need Proxy
            print('302')
            return get_html(url)

    except ConnectionError as e:
        print('Error Occurred', e.args)
        count += 1
        return get_html(url, count)



def get_index(keyword, page):
    #构造请求链接，并请求网页
    url = base_url.format(keyword, page)
    #print(url)
    html = get_html(url)
    return html

def parse_index(html):
    #使用pyquery解析网页
    doc = pq(html)
    items = doc('.news-box .news-list li .txt-box h3 a').items()
    for item in items:
        yield item.attr('data-share')

def get_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None

def parse_detail(html):
    try:
        doc = pq(html)
        title = doc('.rich_media_title').text()
        content = doc('.rich_media_content').text()
        date = doc('#publish_time').text()
        nickname = doc('#js_profile_qrcode > div > strong').text()
        wechat = doc('#js_profile_qrcode > div > p:nth-child(3) > span').text()
        return {
            'title': title,
            'content': content,
            'date': date,
            'nickname': nickname,
            'wechat': wechat
        }
    except XMLSyntaxError:
        return None

def save_to_mongo(data):
    if db['articles'].update({'title': data['title']}, {'$set': data}, True):
        print('Saved to Mongo', data['title'])
    else:
        print('Saved to Mongo Failed', data['title'])


def main():
    for page in range(100, 101):
        html = get_index(KEYWORD, page)
        if html:
            article_urls = parse_index(html)
            for article_url in article_urls:
                article_html = get_detail(article_url)
                if article_html:
                    article_data = parse_detail(article_html)
                    print(article_data)
                    if article_data:
                        save_to_mongo(article_data)



if __name__ == '__main__':
    main()

#10min 46
#26min 99
