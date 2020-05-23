# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

class SpiderweatherPipeline(object):
    def __init__(self):
        self.filename = open("temp.json", 'w')

    def process_item(self, item, spider):
        jsonText = json.dumps(dict(item), ensure_ascii=False)
        # self.filename.write(jsonText.encode('utf-8'))
        return item
