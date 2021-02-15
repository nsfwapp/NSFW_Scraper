# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field



class sceneItem(Item):

    title = Field()
    thumbnail_url = Field()
    preview_url = Field()
    length = Field()
    description = Field()
    gallary_urls = Field()
    studio = Field()
    parent_studio = Field()
    performers = Field() 
    director = Field()
    release_date = Field()
    rating = Field()
    movie = Field()
    tags = Field()
    std_url=Field()

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


class movieItem(Item):

    movie_title = Field()
    movie_cover = Field()
    movie_trailer = Field()
    length = Field()
    description = Field()
    gallary_urls = Field()
    studio = Field()
    performers = Field() 
    director = Field()
    release_date = Field()
    rating = Field()
    scenes = Field()
    genres = Field()
    tags = Field()


