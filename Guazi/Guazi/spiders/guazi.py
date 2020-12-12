# -*- coding: utf-8 -*-
import scrapy
from ..items import GuaziItem

class GuaziSpider(scrapy.Spider):
    name = 'guazi'
    allowed_domains = ['www.guazi.com']
    i = 1
    # 第一页的URl地址
    start_urls = ['https://www.guazi.com/bj/buy/o1/#bread']

    def parse(self, response):
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

        # 生成下一页的地址，交给调度器入队列, scrapy多线程没有体现
        if self.i < 5:
            self.i += 1
            url = 'https://www.guazi.com/bj/buy/o{}/#bread'.format(self.i)
            # 把url交给调度器入队列
            yield scrapy.Request(url=url, callback=self.parse)
