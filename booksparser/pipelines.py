# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import re


class BooksparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.books

    def process_item(self, item, spider):
        #item['_id'] = re.findall(r'\b\d+\b', item.get('_id'))[0]
        item['price'] = ''.join(re.findall(r'\b\d+\b', item.get('price')))

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)

        return item
