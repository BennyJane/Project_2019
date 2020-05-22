#2019-4-04
import re
import time
import aiohttp
import asyncio
import pandas as pd
import logging
import random

# 设置日志格式
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

#pandas 函数
df = pd.DataFrame(columns=['book_name', 'book_url', 'author_info', 'pub_info', 'rating', 'people_num', 'brief', ])


# 异步HTTP请求
async def fetch(sem, session, url):
    async with sem:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}
        proxies = {'http:': '223.100.166.3:36945'}
        proxy='http:223.100.166.3:36945'
        async with session.get(url, headers=headers,verify_ssl=False) as response:
            response.encoding ="utf-8"
            assert response.status == 200
            return await response.text()

# 解析网页
async def parser(html):
    # 利用正则表达式解析网页
    #print (html)

    book_lists = re.findall(r'<ul class="subject-list">[\s\S]*</ul>', html,)[0]
    print (type(book_lists))
    print (len(book_lists))
    lis = re.findall(r'<li class="subject-item">[\s\S]*?</li>', book_lists)
    #print (len(lis))
    for book_info in lis:
        #print (book_info)
        global book_name

        book_name = re.findall(r'title="([^"]*?)"', book_info)[0].strip()
        #print (type(book_name))
        #print (book_name)
        try:
            desc_list = re.findall(r'<div class="pub">[^<]*?</div>', book_info)[0].split("/")
            # print (desc_list)
        except:
            pass
        book_url = re.findall(r'<a href="(.*?)" title=', book_info)[0]
        #print (type(book_url))
        #print (book_url)
        try:
            brief = re.findall(r"<p>([\s\S]*?)</p>", book_info, re.M)[0]
            #print(brief)
        except:
            brief="暂无"
        try:
            author_info = '作者/译者： ' + '/'.join(desc_list[0:-3])
        except:
            author_info = '作者/译者： 暂无'
        try:
            pub_info = '出版信息： ' + '/'.join(desc_list[-3:])
        except:
            pub_info = '出版信息： 暂无'
        try:
            rating =re.findall(r'<span class="rating_nums">([^<]*?)</span>', book_info)
            #print (type(rating))
            #str
            #print(rating)
        except:
            rating = '0.0'
        try:
            #<span class="p1">\n(\([^<]*?\))\n</span>
            #people_num = book_info.findAll('span')[2].string.strip()
            people_num =re.findall(r'\((\d*)?人评价\)', book_info, re.M|re.S)[-1]
            #people_num = people_num.strip('人评价')
            #print (people_num)
        except:
            people_num = '0'

        df.loc[df.shape[0] +1] = [book_name, book_url, author_info, pub_info,rating, people_num, brief, ]

    logger.info(str(df.shape[0]) + '\t'+book_name)


# 处理网页
async def download(sem, url):
    async with aiohttp.ClientSession() as session:
        try:
            #proxies=get_proxy()
            html = await fetch(sem, session, url)
            await parser(html)
        except Exception as err:
            #pass
            print(err)



if __name__=="__main__":
    # 全部网页

    #urls = ["https://book.douban.com/tag/漫画?start=%d&type=T" %(i*20) for i in range(50)]
    page_nums=[]
    #实际只有50页有效
    for i in range(50):
        page_num=i*20
        page_nums.append(page_num)
    urls = ["https://book.douban.com/tag/漫画?start=%d&type=T" %i for i in page_nums]
    print (urls)

    # 统计该爬虫的消耗时间
    print('*' * 50)
    t3 = time.time()

    # 利用asyncio模块进行异步IO处理
    loop = asyncio.get_event_loop()
    sem = asyncio.Semaphore(100)
    tasks = [asyncio.ensure_future(download(sem, url)) for url in urls]
    tasks = asyncio.gather(*tasks)
    loop.run_until_complete(tasks)

    df.to_csv('E://rong360.csv')

    t4 = time.time()
    print('总共耗时：%s' % (t4 - t3))
