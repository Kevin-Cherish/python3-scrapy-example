import urllib

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from alexa.items import *


class alexaSpider(CrawlSpider):
    name = "alexa"
    allowed_domains = ["alexa.com"]
    start_urls = [
        "http://www.alexa.com/",
        "http://www.alexa.com/topsites/category/Top",
    ]
    rules = [
        Rule(LinkExtractor(allow=("/topsites/category;?[0-9]?/Top/[^/]*$")), callback='parse_category_top_xxx',
             follow=True),
        Rule(LinkExtractor(allow=("/topsites/category/Top$",)), callback='parse_category_top', follow=True),
        # Rule(sle(allow=("/people/[^/]+$", )), callback='parse_people', follow=True),
    ]

    # www.alexa.com/topsites/category/Top/Computers
    # www.alexa.com/topsites/category;1/Top/Computers
    def parse_category_top_xxx(self, response):
        self.logger.info('parsed ' + response.url)
        items = []
        sites = response.css('.site-listing')
        # sites = response.xpath('//*[@class="tr site-listing"]')
        for site in sites:
            item = alexaSiteInfoItem()
            item['url'] = site.css('a[href*=siteinfo]::attr(href)')[0].extract()
            # item['url'] = site.css('a[href*=siteinfo]::attr(href)').extract_first()
            item['name'] = site.css('a[href*=siteinfo]::text')[0].extract()
            item['name'] = site.css('a[href*=siteinfo]::text')[0].extract()
            item['description'] = site.css('.description::text')[0].extract()
            remainder = site.css('.remainder::text')
            if remainder:
                item['description'] += remainder[0].extract()
            # more specific
            item['category'] = response.url.split('/')[-1]
            items.append(item)
        return items

    def parse_category_top(self, response):
        self.logger.info('parsed ' + response.url)
        items = []
        categories = response.css('li a[href*="/topsites/category/Top/"]')
        for category in categories:
            item = alexaCategoryItem()
            item['url'] = category.css('::attr(href)')[0].extract()
            item['name'] = category.css('::text')[0].extract()
            # yield item
            items.append(item)
        return items


class alexaCNSpider(CrawlSpider):
    name = "alexa.cn"
    allowed_domains = ["alexa.com"]
    start_urls = [
        "http://www.alexa.com/",
        "http://www.alexa.com/topsites/category/World/Chinese_Simplified_CN",
    ]
    rules = [
        Rule(LinkExtractor(allow=("/topsites/category;?[0-9]*/Top/World/Chinese_Simplified_CN/.*$")),
             callback='parse_category_top_xxx', follow=True),
        Rule(LinkExtractor(allow=("/topsites/category/World/Chinese_Simplified_CN$",)),
             callback='parse_category_top_xxx', follow=True),
        # Rule(sle(allow=("/people/[^/]+$", )), callback='parse_people', follow=True),
    ]

    # www.alexa.com/topsites/category/Top/Computers
    # www.alexa.com/topsites/category;1/Top/Computers
    def parse_category_top_xxx(self, response):
        self.logger.info('parsed ' + str(response))
        items = []

        sites = sel.css('.site-listing')
        for site in sites:
            item = alexaSiteInfoItem()
            item['url'] = site.css('a[href*=siteinfo]::attr(href)')[0].extract()
            item['name'] = site.css('a[href*=siteinfo]::text')[0].extract()
            item['description'] = site.css('.description::text')[0].extract()
            remainder = site.css('.remainder::text')
            if remainder:
                item['description'] += remainder[0].extract()
            # more specific
            item['category'] = urllib.unquote('/'.join(response.url.split('/')[-3:])).decode('utf-8')
            items.append(item)
        return items

    def parse_category_top(self, response):
        self.logger.info('parsed ' + str(response))
        items = []
        sel = Selector(response)

        categories = sel.css('li a[href*="/topsites/category/Top/"]')
        for category in categories:
            item = alexaCategoryItem()
            item['url'] = category.css('::attr(href)')[0].extract()
            item['name'] = category.css('::text')[0].extract()
            items.append(item)
        return items
