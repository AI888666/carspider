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
            item['link'] = 'https://www.guazi.com' + li.xpath('./a/@href').get()

            # 把每辆汽车详情页的连接交给调度器入队列
            # meta参数：在不同的解析函数之间传递数据
            yield scrapy.Request(url=item['link'], meta={'item': item}, callback=self.get_car_info)

    def get_car_info(self, response):
        """提取汽车详情页的数据"""
        # meta会随着response一起回来，作为response的一个属性
        item = response.meta['item']
        item['km'] = response.xpath('.//li[@class="two"]/span/text()').get().strip()
        item['displacement'] = response.xpath('.//li[@class="three"]/span/text()').get().strip()
        item['typ'] = response.xpath('.//li[@class="last"]/span/text()').get().strip()

        # 至此，一辆汽车的完整数据抓取完成，交个管道处理数据
        yield item
