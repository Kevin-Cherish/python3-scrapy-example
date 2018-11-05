# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json


class MoviePipeline(object):
    def __init__(self):
        self.fp = open('movie.txt', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        # json.dump(dict(item), self.fp, ensure_ascii=False, indent=4)
        self.fp.write(str(item))
        self.fp.write('\n')

    def close_spider(self, spider):
        self.fp.close()