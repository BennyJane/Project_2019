# -*- coding: utf-8 -*-
#import scrapy
#直接引入 Spider Request
import json
from scrapy import Spider, Request
#from items import UserItem
import re

import sys
sys.path.append(r"E:\Python学习\Python Projects\爬取知乎用户信息_Scrapy 框架\user\user")
from items import *


class ZhihuSpider(Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    start_user = "excited-vczh"

    user_url = "https://www.zhihu.com/api/v4/members/{user}?include={include}"
    user_query = "allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics"

    followers_url = "https://www.zhihu.com/api/v4/members/{user}/followees?include={include}s&offset={offset}&limit={limit}"
    followers_query = "	data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics"


    def start_requests(self):
        #用户详细信息
        #user = "https://www.zhihu.com/api/v4/members/TempWorker?include=allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics"
        #follows = "https://www.zhihu.com/api/v4/members/excited-vczh/followees?include=data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics&offset=20&limit=20"
        #回调函数 不需要小括号()

        yield Request(self.user_url.format(user=self.start_user, include=self.user_query), self.parse_user)
        yield Request(self.followers_url.format(user=self.start_user, include = self.followers_query, offset=0, limit = 20), callback=self.parse_follows)

    def parse_user(self, response):
        result = json.loads(response.text)
        #导入
        item = UserItem()
        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)
        yield item

    def parse_follows(self, response):
        results = json.loads(response.text)

        if "data" in results.keys():
            for result in results.get("data"):
                yield Request(self.user_url.format(user=result.get("url_token"), include=self.user_query), self.parse_user)


        #直接提取 next 链接，无法访问；需要自己构造 next_page
        if "paging" in results.keys() and results.get("paging").get("is_end") == False:
            origin_url = response.url
            pattern = re.compile(r"&offset=(\d+)")
            offset = pattern.search(origin_url)
            offset = offset.group(1)
            next_offset = int(offset) + 20
            next_page =re.sub(r"&offset=(\d+)","&offset="+str(next_offset),origin_url)
            yield Request(next_page, self.parse_follows)


'''
请求接口不需要另外的请求头信息
'''
