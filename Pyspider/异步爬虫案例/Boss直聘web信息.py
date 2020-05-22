#2019-4-05
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
df = pd.DataFrame(columns=['job_url','job_name', 'wage', 'location', 'yearsOfwork','school_age','welfare', 'job_evaluation','teamwork'
                           ,'company',])

# 异步HTTP请求
async def fetch(sem, session, url):
    async with sem:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}
        proxy="http://110.52.235.183:9999"
        async with session.get(url, headers=headers,timeout=60,verify_ssl=False) as response:
            response.encoding = "utf-8"
            return await response.text()


async def get_job_urls(html):
    jobs_urls = []
    try:
        root = etree.HTML(html)
        # print (etree.tostring(root))
    except Exception as e:
        print(e)

    urls = root.xpath("//div[@class='job-list']/ul/li//a[@data-jobid]/@href")
    #print(type(urls))
    for i in urls:
        url = str(i)
        #print(i)
        abs_url='https://www.zhipin.com'+url
        jobs_urls.append(abs_url)
    return jobs_urls


# 解析网页
async def parser(html,url):
    try:
        root = etree.HTML(html)
        # print (etree.tostring(root))
    except Exception as e:
        print(e)
    job_url=url
    job_name = root.xpath("//div[@class='info-primary']/div[@class='name']/h1/text()")[0]
    wage = root.xpath("//div[@class='info-primary']/div[@class='name']/span/text()")[0].strip()
    # 子节点顺序从1开始
    location = root.xpath("//div[@class='job-location']/div[1]/text()")[0]
    yearsOfwork = root.xpath("//div[@class='job-primary detail-box']/div[@class='info-primary']/child::p[1]/text()")[1]
    school_age = root.xpath("//div[@class='job-primary detail-box']/div[@class='info-primary']/child::p[1]/text()")[2]
    welfare = root.xpath("//div[@class='job-tags']/span/text()")
    if len(welfare)==0:
        welfare="暂无"
    job_evaluation = root.xpath("//div[@class='job-sec']/child::div[@class='text']/text()")
    job_evaluation = ''.join(job_evaluation).strip()
    teamwork = root.xpath("//div[@class='job-sec company-info']/div/text()")
    teamwork = ''.join(teamwork).strip()
    company = root.xpath("//div[@class='sider-company']/p/text()")

    df.loc[df.shape[0] + 1] = [job_url,job_name, wage, location, yearsOfwork,school_age,welfare,job_evaluation,teamwork,company]
    logger.info(str(df.shape[0]) + '\t' + job_url)


# 处理网页
async def download(sem, url):
    async with aiohttp.ClientSession() as session:
        try:
            html = await fetch(sem, session, url)
            job_urls = await get_job_urls(html)
            for job_url in job_urls:
                html=await fetch(sem, session,job_url )
                await parser(html,job_url)
        except Exception as err:
            print(err)


if __name__=="__main__":
    # 全部网页
    urls = ['https://www.zhipin.com/c100010000/?query=python开发&page=%d&ka=page-2' %i for i in range(1,11)]
    #print(urls)
    # 统计该爬虫的消耗时间
    print('*' * 50)
    t3 = time.time()

    # 利用asyncio模块进行异步IO处理
    loop = asyncio.get_event_loop()
    sem = asyncio.Semaphore(100)
    tasks = [asyncio.ensure_future(download(sem, url)) for url in urls]
    tasks = asyncio.gather(*tasks)
    loop.run_until_complete(tasks)

    df.to_excel('E://boss直聘_python开发.xls')

    t4 = time.time()
    print('总共耗时：%s' % (t4 - t3))
