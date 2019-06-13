# 2019-4-05

# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import re
import aiohttp
import asyncio

import pandas as pd
import logging

import time
from dateutil.parser import parse
#from dateutil import parser  #这种引用方式有点问题

from lxml import etree

import requests


# 设置日志格式
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# pandas 函数
df = pd.DataFrame(columns=['event_id','wiki_url', 'page_title', 'link', 'start_date','end_date', 'city','country', 'submission_date'
    , 'abstract_reg_due', 'notification_due', 'final_due', 'categories', 'cfp_content', "related_resource","crawling_time"])


# 'organizerid'

# 异步HTTP请求
async def fetch(sem, session, url):
    async with sem:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
        # proxy="http://110.52.235.183:9999"
        async with session.get(url, headers=headers, timeout=60, verify_ssl=True) as response:
            response.encoding = "utf-8"
            return await response.text()


async def get_huiyi_urls(html):
    huiyi_urls = []
    try:
        root = etree.HTML(html)
        # print (etree.tostring(root))
    except Exception as e:
        print(e)

    # 提取表格所有行数据
    trs = root.xpath('/html/body/div[@class="contsec"]/center/form/table/tr/td[@align="center"]/table/tr')
    # print(trs)
    if len(trs) <= 0:
        return
    for index, tr in enumerate(trs[1:]):
        # 只处理偶数索引数据，因为每个会议信息由两行【tr】组成,只需要提取URL；改进：ragne(1,num,2),
        if index % 2 != 0:
            continue
        # 获取单个会议的url链接
        relatively_url = tr.xpath('td[@align="left"]/a/@href')[0]
        abs_url = "http://www.wikicfp.com" + relatively_url
        # print(abs_url)
        huiyi_urls.append(abs_url)
    # print(len(huiyi_urls))
    return huiyi_urls


# 解析网页
async def parser(html, url):
    global end_date, start_date
    try:
        root = etree.HTML(html)
        # print (etree.tostring(root))
    except Exception as e:
        print(e)

    # event_id
    try:
        event_id = str(url).split("?")[1].split("&")[0].split("=")[1]
    except Exception as e:
        event_id = re.findall(r'event_id=(.*?)&', str(url))[0]

    #wiki_url
    wiki_url = url

    # title
    page_title = root.xpath("/html/head/title/text()")[0]
    # print(page_title)

    # 官网链接
    link = root.xpath(r"//a[@target='_newtab']/@href")[0]
    # print(link)

    # 处理中间表格内容:when where abstract_reg_due submission_date notification_due final_due
    # when
    try:
        when = root.xpath(r"//th[contains(text(), 'When')]/following-sibling::td/text()")[0].strip()
        start_time = when.split("-")[0]
        end_time = when.split("-")[1]
        # print(type(end_time))
        start_01 = parse(start_time)
        start_date = start_01.strftime('%Y-%m-%d')

        end_01 = parse(end_time)
        end_date = end_01.strftime('%Y-%m-%d')
        # print(start_date, end_date)
    except Exception as e:
        when = None
        # print(e)

    #where
    try:
        addr = root.xpath(r"//th[contains(text(), 'Where')]/following-sibling::td/text()")[0]
        print(addr)       #<class 'lxml.etree._ElementUnicodeResult'>
        city = "".join(addr.split(",")[:-1])
        country = addr.split(",")[-1].strip()
        # print(city, "\n" , country)
        # print(type(addr))
    except Exception as e:
        addr = None
        # print(e)

    #submission_date
    try:
        submission_date = root.xpath(
            r"//th[contains(text(), 'Submission Deadline')]/following-sibling::td//span[@property='v:startDate']/text()")[
            0]
        submission_date = parse(submission_date)
        submission_date = submission_date.strftime("%Y-%m-%d")
        # print(submission_date)
    except Exception as e:
        submission_date = None
        # print(e)

    #abstract_reg_due
    try:
        abstract_reg_due = root.xpath(
            r"//th[contains(text(), 'Abstract Registration Due')]/following-sibling::td//span[@property='v:startDate']/text()")[
            0]
        abstract_reg_due = parse(abstract_reg_due)
        abstract_reg_due = abstract_reg_due.strftime("%Y-%m-%d")
        # print(abstract_reg_due)
        # print(type(abstract_reg_due))
    except Exception as e:
        abstract_reg_due = None
        # print(e)

    # notification_due
    try:
        notification_due = root.xpath(
            r"//th[contains(text(), 'Notification Due')]/following-sibling::td//span[@property='v:startDate']/text()")[
            0]
        notification_due = parse(notification_due)
        notification_due = notification_due.strftime("%Y-%m-%d")
        # print(notification_due)
    except Exception as e:
        notification_due = None
        # print(e)

    # final_due
    try:
        final_due = root.xpath(
            r"//th[contains(text(), 'Final Version Due')]/following-sibling::td//span[@property='v:startDate']/text()")[0]
        final_due = parse(final_due)
        final_due = final_due.strftime("%Y-%m-%d")
        # print(final_due)
    except Exception as e:
        final_due = None
        # print(e, "04")

    # 确定分类
    try:
        categories = root.xpath(r"//h5/a/text()")[:]
        if len(categories) == 0:
            categories = None
        # print(categories)   #有时候为空
    except Exception as e:
        categories = None
        # print(e, "05")

    # cfp_content内容获取
    try:
        cfp_content_01 = root.xpath(r"//tr/td[@align='center']/div[@class='cfp']")[0]
        cfp_content = cfp_content_01.xpath('string(.)').replace('\n', '').replace('\r', '')
        # print(len(cfp_content))
    except Exception as e:
        cfp_content=None
        # print(e, "06")

    # related_resource内容获取
    try:
        related_resource_01 = root.xpath(r"/html/body/div[@class='contsec']/div[@class='cfp']/table")[0]
        related_resource = related_resource_01.xpath("string(.)").replace('\n', '').replace('\r', '')
        # print(len(related_resource))
    except Exception as e:
        related_resource=None
        # print(e, "07")

    # 数据抓取时间
    crawling_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 数据筛选
    length = len(link)
    if link.rfind("github.io", length - 9, length) == -1 and link.rfind("google.site", length - 11, length) == -1: #网址后缀清洗
        if when is not None:   #会议时间不可缺少
            if (end_01-start_01).days <= 10:    #会议召开时间不大于10天

                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/74.0.3729.169 Safari/537.36'}

                response = requests.get(link, headers=headers, timeout = 30)
                # 200 正常访问； 302 页面重新定向，访问新的页面
                VALID_STATUS_CODES = [200, 302]

                if response.status_code in VALID_STATUS_CODES:
                    print("URL 可以访问！")

                    df.loc[df.shape[0] + 1] = [event_id, wiki_url,page_title, link,start_date,end_date, city, country, submission_date, abstract_reg_due,
                                               notification_due, final_due, categories, cfp_content, related_resource, crawling_time]
                    logger.info(str(df.shape[0]) + '\t' + link)
                else:
                    print("URL, 不能访问！")
    else:
        pass  # 只要不满足任一条件，就舍弃该条会议数据


# 处理网页
async def download(sem, url):
    async with aiohttp.ClientSession() as session:
        try:
            html = await fetch(sem, session, url)
            huiyi_urls = await get_huiyi_urls(html)
            for huiyi_url in huiyi_urls:
                html = await fetch(sem, session, huiyi_url)
                await parser(html, huiyi_url)
        except Exception as err:
            print(err)


if __name__ == "__main__":
    # 全部网页
    urls = ['http://www.wikicfp.com/cfp/allcfp?page=%d' % i for i in range(1, 11)]
    # print(urls)
    # 统计该爬虫的消耗时间
    print('*' * 50)
    t3 = time.time()

    # 利用asyncio模块进行异步IO处理
    loop = asyncio.get_event_loop()
    sem = asyncio.Semaphore(20)
    tasks = [asyncio.ensure_future(download(sem, url)) for url in urls]
    tasks = asyncio.gather(*tasks)
    loop.run_until_complete(tasks)

    df.to_csv('D:/DataWorking/result/con_0613_02.csv')
    # df.to_csv('D:/DataWorking/result/huiyi08.csv',, encoding="utf-8")

    t4 = time.time()
    print('总共耗时：%s' % (t4 - t3))
