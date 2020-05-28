# -*- coding: utf-8 -*-
import scrapy
from scrapy import cmdline, Request
import datetime
import time
import json
# from spiderWeather.spiders.constant import SITE, MONTH
from ..items import SpiderweatherItem

MONTH = ['01', '02', '03', '04', '05']
SITE = {
    '济南': 'jinan',
    '青岛': 'qingdao',
    '淄博': 'zibo',
    '枣庄': 'zaozhuang',
    '东营': 'dongying',
    '烟台': 'yantai',
    '潍坊': 'weifang',
    '济宁': 'jining1',
    '泰安': 'taian1',
    '威海': 'weihai',
    '日照': 'rizhao',
    '滨州': 'binzhou',
    '德州': 'dezhou',
    '聊城': 'liaocheng',
    '菏泽': 'heze',
    '莱芜': 'laiwu',
    '临沂': 'linyi2'
}


class WeatherSpider(scrapy.Spider):
    name = 'weather'
    # allowed_domains = ['http://d1.weather.com']
    start_urls = ['http://d1.weather.com.cn/calendar_new/2019/101120101_201910.html']
    base_url = 'http://lishi.tianqi.com/{}/2020{}.html'

    def start_requests(self):
        for site in SITE.values():
            for month in MONTH:
                if month == '05':
                    # 五月份的数据需要单独抓
                    pass
                else:
                    url = 'http://lishi.tianqi.com/{}/2020{}.html'.format(site, month)
                    yield Request(url=url, callback=self.parse)
                # break

    def parse(self, response):
        weatherItme = SpiderweatherItem()
        weatherItme['site'] = self.site(response)
        weatherItme['month_mean_max_temp'] = self.month_mean_max_temp(response)
        weatherItme['month_mean_min_temp'] = self.month_mean_min_temp(response)
        dayNum = self.dayNum(response)
        print('==========================================', len(dayNum))
        all_month_day = []
        for i in range(1, len(dayNum) + 1):
            date, week = self.date(response, i)
            max_temp = self.max_temp(response, i)
            min_temp = self.min_temp(response, i)
            climate = self.climate(response, i)
            air = self.air(response, i)
            weatherItme['date'] =date[:6]
            temp ={
                'date': date,
                'week': week,
                'max_temp': max_temp,
                'min_temp': min_temp,
                'climate': climate,
                'air':air,
            }
            all_month_day.append(temp)
        all_month_day_text = json.dumps(all_month_day, ensure_ascii=False)
        weatherItme['month_data'] = all_month_day_text
        return weatherItme

    def site(self, response):
        site = response.xpath(r'//div[@class="tian_one"]/div[1]/h3/text()').extract_first()
        if site:
            site = site.replace('历史天气', '').strip()
            return site
        return ''

    def month_mean_max_temp(self, response):
        res = response.xpath(r'//div[@class="tian_twoa"][1]/text()').extract_first()
        return res

    def month_mean_min_temp(self, response):
        # /html/body/div[8]/div[1]/div[5]/ul/li[1]/div[2]/div[1]
        res = response.xpath(r'//ul[@class="tian_two"]/li/div[2]/div[1]/text()').extract_first()
        return res

    def dayNum(self, response):
        # /html/body/div[8]/div[1]/div[6]/ul/li[1]
        res = response.xpath(r'//ul[@class="thrui"]/li').extract()
        return res

    def date(self, response, index):
        res = response.xpath(f'//ul[@class="thrui"]/li[{index}]/div[1]/text()').extract_first()
        if res:
            res = res.replace('\r\n', '').strip()
            date, week = res.split(' ')
            return date, week
        else:
            return '', ''

    def max_temp(self, response, index):
        res = response.xpath(f'//ul[@class="thrui"]/li[{index}]/div[2]/text()').extract_first()
        if res:
            res = res.replace('\r\n', '').strip()
            return res
        else:
            return ''

    def min_temp(self, response, index):
        res = response.xpath(f'//ul[@class="thrui"]/li[{index}]/div[3]/text()').extract_first()
        if res:
            res = res.replace('\r\n', '').strip()
            return res
        else:
            return ''

    def climate(self, response, index):
        res = response.xpath(f'//ul[@class="thrui"]/li[{index}]/div[4]/text()').extract_first()
        if res:
            res = res.replace('\r\n', '').strip()
            return res
        else:
            return ''

    def air(self, response, index):
        res = response.xpath(f'//ul[@class="thrui"]/li[{index}]/div[6]/span/text()').extract_first()
        if res:
            res = res.replace('\r\n', '').strip()
            return res
        else:
            return ''
