# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import redis

# 连接本地redis
redis_db = redis.Redis(host='127.0.0.1', port=6379, db=1)
redis_data_dict = 'news'  # key的名字，里面的内容随便写，这里的key相当于字典名称，而不是key值。为了后面引用而建的


class SohuspiderPipeline(object):

    collection_name = 'News' # 选择mongodb数据库集合

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        redis_db.flushdb()
        if redis_db.hlen(redis_data_dict) == 0:  # 判断redis数据库中的key，若不存在就读取mongodb数据并临时保存在redis中
            df = self.db[self.collection_name].find()   # 读取mongodb中的数据

            for news in df:
                redis_db.hset(redis_data_dict, news['url'], 1)
                print(news)  # 把每个url写入field中

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if redis_db.hexists(redis_data_dict, item['url']):  # 比较的是redis_data_dict里面的field
            print("数据库已经存在该条数据，不再继续追加")
        else:
            exist = self.db[self.collection_name].find_one({'url': item['url']})
            print(exist)
            if exist:
                print("其他来源去重")    # 去除因为url相同channel不同而未被去重的相同新闻
            else:
                self.db[self.collection_name].insert_one(dict(item))
                print("添加一条新数据")
        return item
