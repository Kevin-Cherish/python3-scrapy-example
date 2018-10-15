# -*- coding: utf-8 -*-
from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractor import LinkExtractor
from amazonbook.items import AmazonbookItem


class AmazonSpider(CrawlSpider):
    name = 'amazon'
    allowed_domains = ['www.amazon.com']
    start_urls = [
        "https://www.amazon.com/books-used-books-textbooks/b?node=283155",
    ]

    rules = [
        Rule(LinkExtractor(allow=("/books-used-books-textbooks/.*", )), callback='parse0', follow=True)
    ]

    def parse0(self, response):
        self.logger.info('pares ' + response.url)
        rows = response.css('.inner .a-row')
        for row in rows:
            items = AmazonbookItem()
            items['url'] = row.css('.title::attr(href')
            items['title'] = row.css('.spTitleText::text')
            items['comments'] = row.css('.a-icon-row .a-size-small::text')
            yield items


