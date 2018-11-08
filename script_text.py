import scrapy
from scrapy.linkextractors import LinkExtractor


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['www.xunbibao.com']
    start_urls = ['http://www.xunbibao.com/zixun/']
    download_delay = 5
    rule = LinkExtractor(allow=('http://www.xunbibao.com/zixun/\d{4}.html',))
    # rule = LinkExtractor()

    def parse(self, response):
        # urls = response.xpath('//div[@class="detail"]/h4/a/@href').extract()
        # for url in urls:
        #     yield response.follow(url, callback=self.parse_detail)
        links = self.rule.extract_links(response)
        self.logger.info(links)
        for x in links:
            self.logger.info(x.url)
            yield scrapy.Request(x.url, callback=self.parse_detail)

    def parse_detail(self, response):
        self.logger.info(response.url)
        pass


if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess()
    process.crawl(SpiderSpider)
    process.start()
