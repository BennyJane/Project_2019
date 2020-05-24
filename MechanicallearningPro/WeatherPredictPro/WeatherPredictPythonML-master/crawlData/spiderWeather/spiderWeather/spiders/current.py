# -*- coding: utf-8 -*-
import scrapy
from scrapy import cmdline, Request
import datetime
import time
import json
# from spiderWeather.spiders.constant import SITE, MONTH
from ..items import SpiderweatherItem

CURRENT_MONTH = '05'
MONTH_DAYS_NUM = 31
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


class CurrentSpider(scrapy.Spider):
    name = 'current'
    # allowed_domains = ['http://d1.weather.com']
    start_urls = ['http://d1.weather.com.cn/calendar_new/2019/101120101_201910.html']
    base_url = 'http://lishi.tianqi.com/{}/202005{}.html'

    def start_requests(self):
        for site in SITE.values():
            for day in range(MONTH_DAYS_NUM):
                url = 'http://lishi.tianqi.com/{}/2020{}0{}.html'.format(site, CURRENT_MONTH, day)
                yield Request(url=url, callback=self.parse)
            break

    def parse(self, response):
        weatherItme = SpiderweatherItem()
        weatherItme['site'] = self.site(response)
        weatherItme['month_mean_max_temp'] = '无'
        weatherItme['month_mean_min_temp'] = '无'
        date = self.date(response)
        max_temp = self.max_temp(response)
        min_temp = self.min_temp(response)
        climate = self.climate(response)
        air = self.air(response)
        weatherItme['date'] = date[:6]
        temp = {
            'date': date,
            'week': '无',
            'max_temp': max_temp,
            'min_temp': min_temp,
            'climate': climate,
            'air': air,
        }
        all_month_day_text = json.dumps(temp, ensure_ascii=False)
        weatherItme['month_data'] = all_month_day_text
        return weatherItme

    def site(self, response):
        site = response.xpath(r'//div[@class="linegraphtitle"]/text()').extract_first()
        if site:
            site = site.strip()
            site = site[:2]
            return site
        return ''

    def dayNum(self, response):
        # /html/body/div[8]/div[1]/div[6]/ul/li[1]
        res = response.xpath(r'//ul[@class="thrui"]/li').extract()
        return res

    def date(self, response):
        # /html/body/div[8]/div[3]/div[1]/div/div[1]/div/select
        res = response.xpath(f'//div[@class="optionbox"]/select/option[@selected="selected"]/text()').extract_first()
        if res:
            res = res.replace('\r\n', '').strip()
            res = res.replace('年', '0').replace('日', '').replace('月', '0')
            return res
        else:
            return ''

    def max_temp(self, response):
        res = response.xpath(f'//div[@class="hisdailytemp"]/span[1]/text()').extract_first()
        if res:
            res = res.replace('\r\n', '').strip()
            return res
        else:
            return ''

    def min_temp(self, response):
        res = response.xpath(f'//div[@class="hisdailytemp"]/span[2]/text()').extract_first()
        if res:
            res = res.replace('\r\n', '').strip()
            return res
        else:
            return ''

    def climate(self, response):
        res = response.xpath(f'//div[@class="hisdailywea"]/text()').extract_first()
        if res:
            res = res.replace('\r\n', '').strip()
            return res
        else:
            return ''

    def air(self, response):
        res = response.xpath(f'//ul[@class="hisdailywind"]/text()').extract_first()
        if res:
            res = res.replace('\r\n', '').strip()
            return res
        else:
            return ''
