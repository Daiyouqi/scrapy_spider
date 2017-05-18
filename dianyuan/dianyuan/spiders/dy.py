# -*- coding: utf-8 -*-
import scrapy
import os
from scrapy.http import Request
from dianyuan.items import DianyuanItem
 
class DySpider(scrapy.Spider):
    name = "dy"
    allowed_domains = ["www.qihuiwang.com"]
    start_urls = ['http://company.dianyuan.com/index.php?do=biz_product_list&productName=电源适配器&city=&vip=&only=&rcTotal=1714&rcStart=0&rcLimit=1714']
    def parse(self, response):
        item = DianyuanItem()
        movies = response.xpath('//div[@class="list"]/table/tr')
        for k in range(1,len(movies)):
             item['product'] = movies[k].xpath('./td[3]/h3/a/text()').extract()[0]
             item['company'] = movies[k].xpath('./td[3]/p[1]/a/text()').extract()[0]
             item['uptime'] = movies[k].xpath('./td[3]/p[2]/span/text()').extract()[0]
             item['city'] = movies[k].xpath('./td[4]/text()').extract()[0]
             urlst = movies[k].xpath('./td[@class="l cpy"]/h3/a/@href').extract()[0]
             yield Request (url=urlst, meta={'item': item}, callback = self.parse_sickinfo)
    def parse_sickinfo(self,response):
        trs = response.xpath('//div[@class="cpyContact mCommStyle"]/table/tr')
        item = response.meta['item']
        item['name'] = trs[0].xpath('./td[1]/text()').extract()[0]
        item['phone'] = trs[1].xpath('./td[1]/text()').extract()[0]
        item['mailbox'] = trs[2].xpath('./td[1]/a/text()').extract()[0]
        item['Mphone'] = trs[4].xpath('./td/text()').extract()[0]
        item['Clink'] = trs[6].xpath('./td[1]/a/text()').extract()[0]
        yield item