#2019-4-04
import re
import time
import aiohttp
import asyncio
import pandas as pd
import logging
from lxml import etree

# 设置日志格式
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

#pandas 函数
df = pd.DataFrame(columns=['name','url', 'brief', 'play_counts', 'message_counts','Date', 'period'])


# 异步HTTP请求
async def fetch(sem, session, url):
    async with sem:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}
        async with session.get(url, headers=headers) as response:
            response.encoding = "utf-8"
            return await response.text()


# 解析网页
async def parser(html):
    #print (html)
    # 利用lxml解析网页,
    #将html传入etree 的构造方法,得到一个文档的对象
    root = etree.HTML(html)
    #print (root)
    one_vedios = root.xpath("//li[@class='video matrix']")
    print (one_vedios)
    print (type(one_vedios))
    print (len(one_vedios))
    result = etree.tostring(one_vedios[0]).decode()
    #print (result)
    #for item in one_vedios:
       # result = etree.tostring(item).decode()
       # print (result)

    #print(one_vedios[0])
    for i in range(20):
        name=root.xpath("//li[@class='video matrix']/a[@title]/@title")[i]
        #print (len(name))
        url=root.xpath("//li[@class='video matrix']/a[@title]/@href")[i]
        #print (url)
        brief=root.xpath("//li[@class='video matrix']/div[@class='info']/div[@class='des hide']/text()")[i]
        play_counts=root.xpath("//li[@class='video matrix']/div[@class='info']/div[@class='tags']/span[1]/text()")[i]
        message_counts = root.xpath("//li[@class='video matrix']/div[@class='info']/div[@class='tags']/span[2]/text()")[i]
        Date = root.xpath("//li[@class='video matrix']/div[@class='info']/div[@class='tags']/span[3]/text()")[i]
        period=root.xpath("//li[@class='video matrix']/a/div[@class='img']/span/text()")[i]
        print (period.strip())

        df.loc[df.shape[0] + 1] = [name,url, brief, play_counts, message_counts,Date,period]

    logger.info(str(df.shape[0]) + '\t' + name)


# 处理网页
async def download(sem, url):
    async with aiohttp.ClientSession() as session:
        try:
            html = await fetch(sem, session, url)
            await parser(html)
        except Exception as err:
            print(err)




if __name__=="__main__":
    # 全部网页
    urls = ["https://search.bilibili.com/all?keyword=PYTHON爬虫&page=%d" %i for i in range(1,51)]

    # 统计该爬虫的消耗时间
    print('*' * 50)
    t3 = time.time()

    # 利用asyncio模块进行异步IO处理
    loop = asyncio.get_event_loop()
    sem = asyncio.Semaphore(100)
    tasks = [asyncio.ensure_future(download(sem, url)) for url in urls]
    tasks = asyncio.gather(*tasks)
    loop.run_until_complete(tasks)

    df.to_csv('E://B站爬虫视频.csv')

    t4 = time.time()
    print('总共耗时：%s' % (t4 - t3))
