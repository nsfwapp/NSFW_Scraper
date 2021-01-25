# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class NsfwScraperItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class vixenScene(Item):

    studio = Field()
    parent_studio = Field()
    title = Field()
    thumbnail_url = Field()
    preview_url = Field()
    performers = Field()
    director = Field()
    length = Field()
    description = Field()
    release_date = Field()
    rating_native = Field()
    gallary_urls = Field()

