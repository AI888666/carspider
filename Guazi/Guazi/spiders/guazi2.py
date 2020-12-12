# -*- coding: utf-8 -*-
import scrapy
from ..items import GuaziItem


class GuaziSpider(scrapy.Spider):
    name = 'guazi2'
    allowed_domains = ['www.guazi.com']
    # 第一页的URl地址
    # start_urls = ['https://www.guazi.com/bj/buy/o1/#bread']

    # 1. 去掉start_urls变量
    # 2. 重新start_requests()方法
    def start_requests(self):
        """一次性生成所有要抓取的URl地址，一次性交给调度器入队列"""
        for i in range(1, 6):
            url = 'https://www.guazi.com/bj/buy/o{}/#bread'.format(i)
            # 交给调度器入队列，并指定解析函数
            yield scrapy.Request(url=url, callback=self.detail_page)

    def detail_page(self, response):
        """解析函数"""
        # 第二步
        li_list = response.xpath('/html/body/div[6]/ul/li')
        for li in li_list:
            # 给items.py中的GuaziItem类做实例化
            item = GuaziItem()
            item['name'] = li.xpath('./a/h2/text()').get()
            item['price'] = li.xpath('.//div[@class="t-price"]/p/text()').get()
            item['link'] = li.xpath('./a/@href').get()

            # 如何吧值赋值给管道文件处理，用 yield item
            yield item
