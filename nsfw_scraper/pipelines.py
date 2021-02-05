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
import logging, os
from mongoengine import connect, disconnect
from .models import Scene, Performer, Movie, Director, Studio, Rating, ReleaseDate, Tag, Genre
from . import settings
import urllib
from dotenv import load_dotenv, find_dotenv
from sqlalchemy.orm import session

load_dotenv(find_dotenv())

user = urllib.parse.quote_plus(os.getenv("USER"))
passwd = urllib.parse.quote_plus(os.getenv("PASS"))


class ScenePipeline(object):

    """Vixen pipeline for storing scraped items in the database"""
    
    def __init__(self):
        connect(os.getenv("MONGO_DATABASE"), host= "mongodb+srv://%s:%s@mongo@cluster0.lalaj.mongodb.net/%s?retryWrites=true&w=majority" % (user, passwd, os.getenv("MONGO_DATABASE")))

    def process_item(self, item, spider):


        scene = Scene(
                    title = item['title'],
                    thumbnail_url = item['thumbnail_url'],
                    preview_url = item['preview_url'],
                    length = item['length'],
                    description = item['description'],
                    gallary_urls = item['gallary_urls'], 
                    #studio = item['studio'],        #FK
                    #performers = item['performers'],    #FK
                    #director = item['director'],    #FK
                    #release_date = item['release_date'],    #FK
                    #movie = item['movie'],  #FK
                    #tags = item['tags']     #FK
        )
        #performer
        for performer in item['performers']:
            performert = session.query(Performer).filter_by(name=performer).first()
            if performert is not None:
                scene.performers.append(performert)
            else:
                scene.performers.append(Performer(name=performer))

        #director
        for director in item['director']:
            directort = session.query(Director).filter_by(name=director).first()
            if directort is not None:
                scene.director = director
            else:
                scene.performer = Director(name=director)

        #tag
        for count,tag in enumerate(item['tags']):
            #logging.info(tag, "theNewOne" , type([tag]))
            tagt = session.query(Tag).filter_by(tag=tag).first()
            if tagt is not None:
                scene.tags.append(tagt)
            else:
                scene.tags.append(Tag(tag=tag))

        #studio
        studio = session.query(Studio).filter_by(studio=item['studio']).first()
        if studio is not None:
            scene.studio = studio
        else:
            scene.studio = Studio(studio=item['studio'], parent_studio=item['parent_studio'])
        
        #rating
        rating = session.query(Rating).filter_by(rating=item['rating']).first()
        if rating is not None:
            scene.rating = rating
        else:
            scene.rating = Rating(rating=item['rating'])

        #release_date
        release_date = session.query(ReleaseDate).filter_by(release_date=item['release_date']).first()
        if release_date is not None:
            scene.release_date = release_date
        else:
            scene.release_date = ReleaseDate(release_date=item['release_date'])

        scene_exists = session.query(Scene).filter_by(title=item['title']).first() is not None

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

class MoviePipeline(object):

    """Movie pipeline for storing scraped items in the database"""
    
    def __init__(self):
        connect(os.getenv("MONGO_DATABASE"), host= "mongodb+srv://%s:%s@mongo@cluster0.lalaj.mongodb.net/%s?retryWrites=true&w=majority" % (user, passwd, os.getenv("MONGO_DATABASE")))

    def process_item(self, item, spider):

        movie = Movie(
                    movie_title = item['movie_title'],
                    movie_cover = item['movie_cover'],
                    movie_trailer = item['movie_trailer'],
                    length = item['length'],
                    description = item['description'],
                    gallary_urls = item['gallary_urls'], 
                    #studio = item['studio'],            #FK
                    #performers = item['performers'],        #FK
                    #director = item['director'],        #FK
                    #release_date = item['release_date'],    #FK
                    #scenes = item['scenes'],            #FK
                    #genres = item['genres'],        #FK
                    #tags = item['tags']         #FK
        )
        
        #performer
        for performer in item['performers']:
            performert = session.query(Performer).filter_by(name=performer).first()
            if performert is not None:
                movie.performers.append(performert)
            else:
                movie.performers.append(Performer(name=performer))

        #director
        for director in item['director']:
            directort = session.query(Director).filter_by(name=director).first()
            if directort is not None:
                movie.director = director
            else:
                movie.performer = Director(name=director)

        #genre
        for genre in item['genres']:
            genret = session.query(Genre).filter_by(genre=genre).first()
            if genret is not None:
                movie.genres.append(genret)
            else:
                movie.genres.append(Genre(genre=genre))

        #tag
        for count,tag in enumerate(item['tags']):
            #logging.info(tag, "theNewOne" , type([tag]))
            tagt = session.query(Tag).filter_by(tag=tag).first()
            if tagt is not None:
                movie.tags.append(tagt)
            else:
                movie.tags.append(Tag(tag=tag))

        #studio
        studio = session.query(Studio).filter_by(studio=item['studio']).first()
        if studio is not None:
            movie.studio = studio
        else:
            movie.studio = Studio(studio=item['studio'], parent_studio=item['parent_studio'])
        
        #rating
        rating = session.query(Rating).filter_by(rating=item['rating']).first()
        if rating is not None:
            movie.rating = rating
        else:
            movie.rating = Rating(rating=item['rating'])

        #release_date
        release_date = session.query(ReleaseDate).filter_by(release_date=item['release_date']).first()
        if release_date is not None:
            movie.release_date = release_date
        else:
            movie.release_date = ReleaseDate(release_date=item['release_date'])


        movie_exists = session.query(Movie).filter_by(title=item['title']).first() is not None

        if movie_exists:
            logging.info(f'Item {movie} is in db')
            return item
        else:
            try:
                session.add(movie)
                session.commit()
                logging.info(f'Item {movie} stored in db')
            except:
                logging.info(f'Failed to add {movie} to db')
                session.rollback()
                raise
            finally:
                session.close()
        return item

class PerformerPipeline(object):
    """Performer pipeline for storing scraped items in the database"""
    
    def __init__(self):
        connect(os.getenv("MONGO_DATABASE"), host= "mongodb+srv://%s:%s@mongo@cluster0.lalaj.mongodb.net/%s?retryWrites=true&w=majority" % (user, passwd, os.getenv("MONGO_DATABASE")))


    def process_item(self, item, spider):

        
        performer = Performer(
                    name = item['name'],
                    aliases = item['aliases'],
                    gender = item['gender'],
                    description = item['description'],
                    profile_pic = item['profile_pic'],
                    date_of_birth = item['date_of_birth'], # get age from here
                    years_active = item['years_active'],
                    ethnicity = item['ethnicity'],
                    birth_place = item['birth_place'],
                    height = item['height'],
                    hair_color = item['hair_color'],
                    eye_color = item['eye_color'],
                    boobs = item['boobs'],
                    tattoos = item['tattoos'],
                    piercings = item['piercings'],
                    measurments = item['measurments'],
                    #rating = Rating(rating=item['rating'])
                    
        )

        rating = Rating.objects(rating=item['rating'])
        
        if rating is not None:
            performer.rating = rating
        else:
            performer.rating = Rating(rating=item['rating'])

        performer_exists = Performer.objects(name=item['name']) is not None

        if performer_exists:
            #logging.info(item['name'])
            #logging.info(session.query(Performer).filter_by(name=item['name']).first())
            logging.info(f'Item {performer} is in db')

            return item
        else:
            try:
                performer.save()
                logging.info(f'Item {performer} stored in db')
            except:
                logging.info(f'Failed to add {performer} to db')
                raise
            finally:
                disconnect
        return item