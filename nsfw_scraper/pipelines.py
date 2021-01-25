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
from sqlalchemy.orm import sessionmaker
from nsfw_scraper.models import Scene, db_connect, create_scenes_table


class vixenPipeline(object):
    """Vixen pipeline for storing scraped items in the database"""
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_scenes_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save deals in the database.

        This method is called for every item pipeline component.

        """
        session = self.Session()
        scene = Scene(**item)

        try:
            #if session.query(Scenes).filter_by(title=item['title']).first():
            #    pass
            #else:
            session.add(scene)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item