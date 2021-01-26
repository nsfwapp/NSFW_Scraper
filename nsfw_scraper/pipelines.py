# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
#from itemadapter import ItemAdapter


#class NsfwScraperPipeline:
#    def process_item(self, item, spider):
#        return item
#from scrapy import signals
import logging
from sqlalchemy.orm import sessionmaker
from nsfw_scraper.models import Scene, db_connect, create_scenes_table


class vixenPipeline(object):
    """Vixen pipeline for storing scraped items in the database"""
    
    def __init__(self):
        engine = db_connect()
        create_scenes_table(engine)
        self.Session = sessionmaker(bind=engine)
        

    def process_item(self, item, spider):

        session = self.Session()
        scene = Scene(**item)
        #scene = Scene(**item)
        scene_exists = session.query(Scene).filter_by(title=item['title'],rating_native=item['rating_native']).first() is not None

        if scene_exists:
            logging.info(f'Item {scene} is in db')
            return item
        else:
            try:
                session.add(scene)
                session.commit()
                logging.info(f'Item {scene} stored in db')
            except:
                logging.info(f'Failed to add {scene} to db')
                session.rollback()
                raise
            finally:
                session.close()
        return item