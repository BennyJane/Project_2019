# -*- coding: utf-8 -*-
import scrapy


class WeatherSpider(scrapy.Spider):
    name = 'weather'
    allowed_domains = ['http://www.weather.com.cn']
    start_urls = ['http://http://www.weather.com.cn/']

    def parse(self, response):
        pass
