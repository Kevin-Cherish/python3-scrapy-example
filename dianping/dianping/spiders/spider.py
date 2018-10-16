# -*- coding: utf-8 -*-
from scrapy import Spider
import requests
from scrapy import Request

BAIDU_GEO = u'http://api.map.baidu.com/geocoder/v2/?address={}&output=json&ak=gQsCAgCrWsuN99ggSIjGn5nO'

base_category_url = "http://www.dianping.com/search/category"

start_url_dict = {
    u"足疗按摩": "/2/30/g141r1471",
    u"中医养生": "/2/30/g2827r1471",
    u"健康体检": "/2/80/g612",
    u"妇幼保健": "/2/70/g258",
    u"美容Spa": "/2/50/g158",
    u"整形塑体": "/2/85/g183",
    u"运动健身": "/2/45/g147",
    u"口腔健康": "/2/85/g182",
    u"药店": "/2/85/g235"
}


def clean_string(string):
    return string.replace(' ', '').replace('\n', '') if string else ''


def address_to_geo(address):
    data = requests.get(BAIDU_GEO.format(address)).json()
    longitude = data['result']['location']['lng'] if 'result' in data else 120.260569
    latitude = data['result']['location']['lat'] if 'result' in data else 30.242865
    return {'longitude': longitude, 'latitude': latitude}


class SpiderSpider(Spider):
    name = 'dianping'
    allowed_domains = ['www.dianping.com']
    start_urls = ['http://www.dianping.com/']

    def start_requests(self):
        for k, v in start_url_dict.items():
            for i in range(1, 3):
                url = base_category_url + v + 'p{}'.format(i)
                yield Request(url, callback=self.parse, meta={'category': k})

    def parse(self, response):
        shops = response.xpath('//div[@class="tit"]/a/@href').extract()
        for shop in shops:
            if shop.startswith('/shop/'):
                yield Request("http://www.dianping.com{}".format(shop), callback=self.parse_shop,
                              meta=response.request.meta)
            break

    def parse_shop(self, response):
        shop = {}
        shop_name = response.css('.shop-name::text').extract_first()
        shop['name'] = clean_string(shop_name)
        address = response.css('.address span.item::text').extract_first()
        shop['address'] = clean_string(address)
        phone_number = response.css('.tel span.item::text').extract_first()
        shop['phone_number'] = clean_string(phone_number)
        path = u'//span[contains(text(), "营业时间：")]/following-sibling::span/text()'
        opening_hours = response.xpath(path).extract_first()
        shop['opening_hours'] = clean_string(opening_hours)
        geo = address_to_geo(address)
        shop.update(geo)
        store_images = response.xpath("//div[@class='photos-container']//img/@src").extract()
        shop['store_images'] = ','.join(store_images[:2])
        deals = response.xpath("//div[@id='sales']//a/@href").extract()
        shop['deals'] = deals
        shop['category'] = response.request.meta['category']
        return shop




