# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
#from itemadapter import ItemAdapter


#class NsfwScraperPipeline:
#    def process_item(self, item, spider):
#        return item
import logging
import pymongo

class vixenPipeline(object):

    collection_name = 'vixen'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        ## pull in information from settings.py
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        ## initializing spider
        ## opening db connection
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]




    def process_item(self, item, spider):
        ## how to handle each post
        #if self.db[self.collection_name].find({'name':item['name']}).first() is not None:
        #    pass
        #else:
        self.db[self.collection_name].update_one({'name':item['name']}, {'$set': dict(item)}, True)
        logging.debug("Vixen Scene added to MongoDB")
        return item

    def close_spider(self, spider):
        ## clean up when spider is closed
        self.client.close()