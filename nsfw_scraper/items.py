# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field



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

class performerItem(Item):

    name = Field()
    aliases = Field()
    gender = Field()
    description = Field()
    profile_pic = Field()
    date_of_birth = Field() # get age from here
    years_active = Field()
    ethnicity = Field()
    birth_place = Field()
    height = Field()
    hair_color = Field()
    eye_color = Field()
    boobs = Field()
    tattoos = Field()
    piercings = Field()
    measurments = Field()
    rating = Field()

class Studio(Item):

    name = Field()
    description = Field()
    logo_url = Field()


