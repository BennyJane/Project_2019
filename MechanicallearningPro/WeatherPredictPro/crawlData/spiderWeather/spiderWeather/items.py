# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderweatherItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    site = scrapy.Field()  # 地点名称
    date = scrapy.Field()  # 日期
    week = scrapy.Field()  # 星期*
    max_temp = scrapy.Field()  # 最高气温
    min_temp = scrapy.Field()  # 最低气温
    month_mean_max_temp = scrapy.Field()  # 每月最高平均气温
    month_mean_min_temp = scrapy.Field()  # 每月最低平均气温
    climate = scrapy.Field()  # 天气
    air_quality = scrapy.Field()  # 空气质量


class SpiderCurrentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    site = scrapy.Field()  # 地点名称
    date = scrapy.Field()  # 日期
    max_temp = scrapy.Field()  # 最高气温
    min_temp = scrapy.Field()  # 最低气温
    climate = scrapy.Field()  # 天气
    wind = scrapy.Field()  # 空气质量
