# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
import json
from bs4 import BeautifulSoup
from movie.items import MovieItem
import re
from scrapy import FormRequest


class SpiderSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']

    def start_requests(self):
        self.offset = 180
        return [FormRequest(
            url='https://www.douban.com/accounts/login?',
            formdata={
                'source': 'movie',
                'redir': 'https://movie.douban.com/subject/26985127/comments?start=180&limit=20&sort=new_score&status=P&comments_only=1',
                'form_email': '942203701@qq.com',
                'form_password': 'l98l10l23',
                'login': '登录  ',
            },
            callback=self.parse
        )]

    def parse(self, response):
        r = json.loads(response.text)
        html = r['html']
        soup = BeautifulSoup(html, 'lxml')
        all_comment = soup.find_all(class_='comment')
        for comment in all_comment:
            item = MovieItem()
            item['Commentator'] = comment.find('a', class_='').text
            item['time'] = comment.find('span', class_='comment-time').text.strip()
            item['votes'] = comment.find('span', class_='votes').text
            item['short'] = comment.find('span', class_='short').text
            try:
                allstar = comment.find('span', {'class': re.compile('allstar\d.*')}).attrs['class']
                item['allstar'] = allstar[0][-2]
            except:
                item['allstar'] = 0
            yield item
        self.offset += 20
        if self.offset > 1001:
            return None
        data = {
            'start': self.offset,
            'limit': '20',
            'sort': 'new_score',
            'status': 'P',
            'comments_only': '1'
        }
        url = 'https://movie.douban.com/subject/26985127/comments?' + urlencode(data)
        yield scrapy.Request(url, callback=self.parse)
