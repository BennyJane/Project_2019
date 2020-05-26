# -*- coding: utf-8 -*-
import scrapy
from scrapy import cmdline, Request
import datetime
import time
import json
# from spiderWeather.spiders.constant import SITE, MONTH
from ..items import SpiderCurrentItem

MONTH = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
YEAR = ['2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']
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
    '莱芜': 'shandong-laiwu',
    '临沂': 'linyi2'
}


class WeatherSpider(scrapy.Spider):
    name = 'current'
    # allowed_domains = ['http://d1.weather.com']
    start_urls = ['http://d1.weather.com.cn/calendar_new/2019/101120101_201910.html']
    base_url = 'http://lishi.tianqi.com/{}/{}{}.html'

    def start_requests(self):
        for site in SITE.values():
            for year in YEAR:
                for month in MONTH:
                    for day in range(1, 32):
                        if day < 10:
                            day = '0' + str(day)
                        else:
                            day = str(day)
                        url = 'http://lishi.tianqi.com/{}/{}{}{}.html'.format(site, year, month, day)
                        yield Request(url=url, callback=self.parse)
                        # break

    def parse(self, response):
        weatherItme = SpiderCurrentItem()
        weatherItme['site'] = self.site(response)
        date = self.date(response)
        max_temp = self.max_temp(response)
        min_temp = self.min_temp(response)
        climate = self.climate(response)
        wind = self.wind(response)
        weatherItme['date'] = date
        weatherItme['max_temp'] = max_temp
        weatherItme['min_temp'] = min_temp
        weatherItme['climate'] = climate
        weatherItme['wind'] = wind
        return weatherItme

    def site(self, response):
        site = response.xpath(r'//div[@class="linegraphtitle"]/text()').extract_first()
        site = site.strip('\r\n').strip()
        site = site[:2]
        return site

    def date(self, response):
        # /html/body/div[8]/div[3]/div[1]/div/div[1]/div/select/option[1]
        res = response.xpath(f'//div[@class="optionbox"]/select/option[@selected="selected"]/text()').extract_first()
        if res:
            date = res.replace('\r\n', '').strip()
            return date
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

    def wind(self, response):
        res = response.xpath(f'//div[@class="hisdailywind"]/text()').extract_first()
        if res:
            res = res.replace('\r\n', '').strip()
            return res
        else:
            return ''
