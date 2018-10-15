import json
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class alexa_topsitesSpider(CrawlSpider):
    name = "alexa_topsites"
    allowed_domains = ["alexa.com"]
    start_urls = [
        "http://www.alexa.com/topsites",
    ]
    rules = [
        Rule(sle(allow=("http://www.alexa.com/topsites")), callback='parse_1', follow=True),
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
        self.info('Parse '+response.url)
        x = self.parse_with_rules(response, self.list_css_rules, dict)
        # x = self.parse_with_rules(response, self.content_css_rules, dict)
        print(json.dumps(x, ensure_ascii=False, indent=2))
        # pp.pprint(x)
        # return self.parse_with_rules(response, self.css_rules, alexa_topsitesItem)
