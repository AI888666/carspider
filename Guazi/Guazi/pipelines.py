# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import pymysql
from .settings import *
import pymongo


# 管道1：终端打印输出
class GuaziPipeline(object):
    # 第三步
    def process_item(self, item, spider):
        """数据处理"""
        print(item['name'],item['price'])
        return item


# 管道2 - 存入MySQL数据库中，要建库建表
# create database guazidb charset utf8;
# use guazidb;
# create table guazitab(
#     name varchar(200),
#     price varchar(100),
#     link varchar(300)
# );
class GuaziMysqlPipeline(object):
    def open_spider(self, spider):
        """爬虫程序开始时，只执行一次，一般用于数据库的连接"""
        self.db = pymysql.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PWD, MYSQL_DB, charset=CHARSET)
        self.cur = self.db.cursor()

    def process_item(self, item, spider):
        ins = 'insert into guazitab values(%s, %s, %s)'
        li = [
            item['name'].strip(),
            item['price'].strip(),
            item['link'].strip()
        ]
        self.cur.execute(ins, li)
        # 注意---要提交到数据库执行
        self.db.commit()
        # 会把上一个管道的item交于下一个管道
        return item

    def close_spider(self, spider):
        """爬虫程村结束时，只执行一次，一般用于数据库的断开"""
        self.cur.close()
        self.db.close()


# 管道3 - 存入MongoDB数据库
class GuaziMongodbPipeline(object):
    def open_spider(self, spider):
        """爬虫程序开始时，只执行一次，一般用于数据库的连接"""
        self.conn = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
        self.db = self.conn[MONGO_DB]
        self.myset = self.db[MONGO_SET]

    def process_item(self, item, spider):
        d = dict(item)
        self.myset.insert_one(d)

        return item


# 管道4：把数据存入CSV文件 或者直接在run.py中写
# cmdline.execute('scrapy crawl guazi2 -o guazi.csv'.split())
class GuaziCsvPipeline(object):
    def open_spider(self, spider):
        """爬虫程序开始时，只执行一次，一般用于数据库的连接"""
        self.f = open('guazi.csv', 'w')
        self.writer = csv.writer(self.f)

    def process_item(self, item, spider):
        li = ['%s:%s' % (k, v) for k, v in item.items()]
        self.writer.writerow(li)
        return item

    def close_spider(self, spider):
        """爬虫程村结束时，只执行一次，一般用于数据库的断开"""
        self.f.close()
