def run_way3():
    import os
    os.system('scrapy crawl mzitu')


def run_way4():
    from scrapy.crawler import CrawlerRunner
    from scrapy.utils.project import get_project_settings
    from twisted.internet import reactor, defer
    from mzitu_scrapy.spiders import spider
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    d = runner.crawl(spider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()


# sequentially 
def run_way5():
    from scrapy.crawler import CrawlerRunner
    from scrapy.utils.project import get_project_settings
    from twisted.internet import reactor, defer
    from mzitu_scrapy.spiders import spider
    settings = get_project_settings()
    runner = CrawlerRunner(settings)

    @defer.inlineCallbacks
    def crawl():
        yield runner.crawl(spider)
        reactor.stop()

    crawl()
    reactor.run()