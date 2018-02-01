# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin
from  ..items import node_imfor



class BangumiSpider(scrapy.Spider):
    name = 'bangumi'
    allowed_domains = ['bangumi.tv']
    start_urls = ['http://bangumi.tv/anime/browser?sort=rank&page=1']

    def parse(self, response):
        items = response.css('li[class="item odd clearit"]') + response.css('li[class="item even clearit"]')

        for item in items:
            url = item.css('a[class="subjectCover cover ll"]::attr(href)').extract_first()
            node = node_imfor()
            node['node_url'] = response.urljoin(url)
            node['chinese_name'] = item.css('a[class="l"]::text').extract_first()
            node['japanese_name'] = item.css('small[class="grey"]::text').extract_first()
            node['score'] = item.css('small[class="fade"]::text').extract_first()
            node['detail'] = item.css('p[class="info tip"]::text').extract_first().strip()
            node['rank'] = item.css('span[class="rank"] ::text').extract()[1]
            yield node
        next_url = response.xpath('//div[contains(@class, "page_inner")]/a[contains(@class, "p")]/@href').extract()[-2]
        if next_url is not None:
            next_url = urljoin(self.start_urls[0], next_url)
            yield scrapy.Request(next_url, callback=self.parse)

