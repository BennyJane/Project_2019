import re
import time
import aiohttp
import asyncio
import pandas as pd
import logging
import json
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
    #获取字典形式的数据
    try:
        content = re.findall(r'\((.*)\)', html)[0]
    except Exception as e:
        print(url)
        print(e)
    
    #将字符串转化为字典形式
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
    #每个商品的评论信息分为5类

    # 统计该爬虫的消耗时间
    print('*' * 50)
    t3 = time.time()

    # 抓取视频
    max_page =7
    urls=['https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv6306&productId=7301584&score=7&sortType=5&page=%d&pageSize=10&isShadowSku=0&fold=1'
          %i for i in range(0,max_page)]

    # 利用asyncio模块进行异步IO处理
    loop = asyncio.get_event_loop()
    sem = asyncio.Semaphore(2)
    tasks = [asyncio.ensure_future(download(sem, url)) for url in urls]
    tasks = asyncio.gather(*tasks)
    loop.run_until_complete(tasks)

    #df.to_excel('E:/Dada/华为B3.xls')
    df.to_csv('E:\Dada\乐心手环3_视频.csv')
    print("01已爬完")

    #抓取追加评论
    rows_num_01=df.shape[0]+1
    max_page = 10
    urls = [
        'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv6306&productId=7301584&score=5&sortType=5&page=%d&pageSize=10&isShadowSku=0&fold=1'
        % i for i in range(0, max_page)]

    # 利用asyncio模块进行异步IO处理
    loop = asyncio.get_event_loop()
    sem = asyncio.Semaphore(2)
    tasks = [asyncio.ensure_future(download(sem, url)) for url in urls]
    tasks = asyncio.gather(*tasks)
    loop.run_until_complete(tasks)

    #选择新增数据，并生成新的表
    newDf_01 = pd.DataFrame(df.loc[rows_num_01:, :])

    newDf_01.to_csv('E:\Dada\乐心手环3_追加.csv')
    print("02已爬完")

    #抓取好评
    rows_num_02=df.shape[0]+1

    max_page = 100
    urls = [
        'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv6306&productId=7301584&score=3&sortType=6&page=%d&pageSize=10&isShadowSku=0&fold=1'
        % i for i in range(0, max_page)]

    # 利用asyncio模块进行异步IO处理
    loop = asyncio.get_event_loop()
    sem = asyncio.Semaphore(2)
    tasks = [asyncio.ensure_future(download(sem, url)) for url in urls]
    tasks = asyncio.gather(*tasks)
    loop.run_until_complete(tasks)

    #选择新增数据，并生成新的表
    newDf_02 = pd.DataFrame(df.loc[rows_num_02:, :])

    newDf_02.to_csv('E:\Dada\乐心手环3_好评.csv')
    print("03已爬完")

    #抓取中评
    rows_num_03=df.shape[0]+1

    max_page = 5
    urls = [
        'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv6306&productId=7301584&score=2&sortType=6&page=%d&pageSize=10&isShadowSku=0&fold=1'
        % i for i in range(0, max_page)]

    # 利用asyncio模块进行异步IO处理
    loop = asyncio.get_event_loop()
    sem = asyncio.Semaphore(2)
    tasks = [asyncio.ensure_future(download(sem, url)) for url in urls]
    tasks = asyncio.gather(*tasks)
    loop.run_until_complete(tasks)

    #选择新增数据，并生成新的表
    newDf_03 = pd.DataFrame(df.loc[rows_num_03:, :])

    newDf_03.to_csv('E:\Dada\乐心手环3_中评.csv')
    print("04已爬完")

    #抓取差评
    rows_num_04=df.shape[0]+1

    max_page = 5
    urls = [
        'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv6306&productId=7301584&score=1&sortType=6&page=%d&pageSize=10&isShadowSku=0&fold=1'
        % i for i in range(0, max_page)]

    # 利用asyncio模块进行异步IO处理
    loop = asyncio.get_event_loop()
    sem = asyncio.Semaphore(2)
    tasks = [asyncio.ensure_future(download(sem, url)) for url in urls]
    tasks = asyncio.gather(*tasks)
    loop.run_until_complete(tasks)

    #选择新增数据，并生成新的表
    newDf_04 = pd.DataFrame(df.loc[rows_num_04:, :])

    newDf_04.to_csv('E:\Dada\乐心手环3_差评.csv')
    print("05已爬完")

    #记录总时间
    t4 = time.time()
    print('总共耗时：%s' % (t4 - t3))






