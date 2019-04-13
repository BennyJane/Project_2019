import re
import time
import aiohttp
import asyncio
import pandas as pd
import logging
import json
import time
import random

# 设置日志格式
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

#pandas 函数，建立表结构
df = pd.DataFrame(columns=['nickname', 'contents', 'creationTime' ,])


# 异步HTTP请求
async def fetch(sem, session, url):
    async with sem:
        async with session.get(url, verify_ssl=False) as response:
            response.encoding ="utf-8"
            time.sleep(random.randint(2,5)*1.32)
            if response.status == 200:
                return await response.text()
            else:
                return await fetch(sem, session , url)

# 解析网页
async def parser(html,url):

    try:
        content = re.findall(r'\((.*)\)', html)[0]
    except Exception as e:
        print(url)
        print(e)

    result = json.loads(content)
    # print(comment)
    for i in result["comments"]:
        try:
            nickname=i['nickname']
            #nickname.replace('*','A')
            #print(nickname)
        except Exception as e:
            nickname='无'

        try:
            contents = i['content']
        except Exception as e:
            contents = '无'

        try:
            creationTime = i['creationTime']
        except Exception as e:
            creationTime = '无'

        df.loc[df.shape[0] +1] = [nickname, contents, creationTime ]

    logger.info(str(df.shape[0]) + '\t'+creationTime)

# 处理网页
async def download(sem, url):
    async with aiohttp.ClientSession() as session:
        try:
            html = await fetch(sem, session, url)
            await parser(html,url)
        except Exception as err:
            #pass
            print(err)


if __name__=="__main__":
    # 统计该爬虫的消耗时间
    print('*' * 50)
    t3 = time.time()

    item_name='华为手环b5_商务版'
    # 一次性复制五种品论的url链接
    urls=[
        'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv1504&productId=30764834196&score=7&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1',
        'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv1504&productId=30764834196&score=5&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1',
        'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv1504&productId=30764834196&score=3&sortType=6&page=0&pageSize=10&isShadowSku=0&fold=1',
        'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv1504&productId=30764834196&score=2&sortType=6&page=0&pageSize=10&isShadowSku=0&fold=1',
        'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv1504&productId=30764834196&score=1&sortType=6&page=0&pageSize=10&isShadowSku=0&fold=1',
    ]
    # 注意url、页面、视频名称的匹配
    Names = ['视频', '追加', '好评', '中评', '差评']

    # 设置各类评论爬取数量
    max_pages = [20, 10, 100, 2, 3]

    i=0
    for url in urls:
        #替换页面符号
        url=url.replace('page=0', 'page=%d')
        urls=[url %i for i in range(0,max_pages[i])]
        # 利用asyncio模块进行异步IO处理
        loop = asyncio.get_event_loop()
        sem = asyncio.Semaphore(2)
        tasks = [asyncio.ensure_future(download(sem, url)) for url in urls]
        tasks = asyncio.gather(*tasks)
        loop.run_until_complete(tasks)

        PathName = r"E:\Dada\%s_%s.csv'" %(item_name, Names[i])
        df.to_csv(PathName)
        print("第%s部分已爬完" %Names[] )
        i=i+1

    #记录总时间
    t4 = time.time()
    print('总共耗时：%s' % (t4 - t3))
