# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from collections import OrderedDict


class JsonPipeline(object):

    def __init__(self, FILEPATH):
        self.file = open(FILEPATH, 'w', encoding='UTF-8')

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings.get('FILEPATH'))

    def process_item(self, item, spider):
        line = json.dumps(OrderedDict(item), ensure_ascii=False, indent=4)
        self.file.write(line + '\n')
        return item

    def close_spider(self, spider):
        self.file.close()
