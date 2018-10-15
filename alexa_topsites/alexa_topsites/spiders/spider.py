import json
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from misc.spider import *
from alexa_topsites.items import AlexaTopsitesItem

class alexa_topsitesSpider(CommonSpider):
    name = "alexa_topsites"
    allowed_domains = ["alexa.com"]
    start_urls = [
        "http://www.alexa.com/topsites",
    ]
    rules = [
        Rule(LinkExtractor(allow=("https://www.alexa.com/topsites$", )), callback='parse_1', follow=True),
    ]

    list_css_rules = {
        '.site-listing': {
            'rank': '.count::text',
            'name': '.desc-paragraph a::text',
            'desc': '.description::text'
        }
    }

    content_css_rules = {
        'text': '#Cnt-Main-Article-QQ p *::text',
        'images': '#Cnt-Main-Article-QQ img::attr(src)',
        'images-desc': '#Cnt-Main-Article-QQ div p+ p::text',
    }

    def parse_1(self, response):
        self.logger.info('Parse ' + response.url)
        # x = self.parse_with_rules(response, self.list_css_rules, dict)
        # x = self.parse_with_rules(response, self.content_css_rules, dict)
        # print(x)
        # yield x

        # print('-----------', json.dumps(x, ensure_ascii=False, indent=2))
        # pp.pprint(x)
        x = self.parse_with_rules(response, self.list_css_rules, AlexaTopsitesItem)
        print(x)
        return x

