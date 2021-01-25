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

        #scene.studio = item['studio']
        #scene.parent_studio = item['parent_studio']
        #scene.title = item['title']
        #scene.thumbnail_url = item['thumbnail_url']
        #scene.preview_url = item['preview_url']
        #scene.performers = item['performers']
        #scene.director = item['director']
        #scene.length = item['length']
        #scene.discription = item['discription']
        #scene.release_date = item['release_date']
        #scene.rating_native = item['rating_native']
        #scene.gallary_urls = item['gallary_urls']

        try:
            if session.query(Scene).filter_by(title=item['title']).first():
                pass
            else:
                session.add(scene)
                session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item