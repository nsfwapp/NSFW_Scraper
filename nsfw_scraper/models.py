from sqlalchemy import create_engine, MetaData, Column, Text,Date, Integer, String, DateTime, ARRAY, Time, Float, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

from nsfw_scraper import settings

DeclarativeBase = declarative_base()

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))

def create_scenes_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)
    
class Scene(DeclarativeBase):
    """ c """
    __tablename__ = 'scenes'
    #unique fields
    scene_id = Column(Integer, primary_key=True)
    title = Column('title', String)
    thumbnail_url = Column('thumbnail_url', String, nullable=True)
    preview_url = Column('preview_url', String, nullable=True)
    length = Column('length', Time, nullable=True)
    description = Column('description', Text(), nullable=True)
    gallary_urls = Column("gallary_urls", ARRAY(String), nullable=True)
    #repetative fields
    studio = Column('studio', String)   
    performers = Column("performers", ARRAY(String))
    director = Column('director', String, nullable=True)
    release_date = Column('release_date', Date, nullable=True)
    rating = Column('rating', Float, nullable=True)
    


class Performer(DeclarativeBase):
    """ c """
    __tablename__ = 'performers'

    performer_id = Column(Integer, primary_key=True)
    name = Column('name', String)
    description = Column('description', Text(), nullable=True)
    profile_pic = Column('profile_pic', ARRAY(String))
    status = Column('status', String)
    ethnicity = Column('ethnicity', String)
    aliases = Column('aliases', Text(), nullable=True)
    official_site = Column('official_site', String, nullable=True)
    profession = Column('profession', String)
    date_of_birth = Column('date_of_birth', String, nullable=True)
    birth_place = Column('birth_place', String, nullable=True)
    height = Column('height', String)
    eye_color = Column('eye_color', String)
    tattoos = Column('tattoos', String)
    piercings = Column('piercings', String)
    boobs = Column('boobs', String)
    hair_color = Column('hair_color', String)
    measurments = Column('measurments', String, nullable=True)

class Director(DeclarativeBase):
    """ c """
    __tablename__ = 'studios'

    director_id = Column(Integer, primary_key=True)
    name = Column('name', String)


class ReleseDate(DeclarativeBase):
    """ c """
    __tablename__ = 'relesedates'

    relesedate_id = Column(Integer, primary_key=True)
    relese_date = Column('relese_date', Date)


class Rating(DeclarativeBase):
    """ c """
    __tablename__ = 'ratings'

    rating_id = Column(Integer, primary_key=True)
    rating = Column('rating', Float)


class Movie(DeclarativeBase):
    """ Movie Model """
    __tablename__ = 'movies'
    #unique fields
    movie_id = Column(Integer, primary_key=True)
    movie_title = Column('movie_title', String)
    movie_cover = Column('movie_cover', ARRAY(String))
    length = Column('length', Time)
    movie_trailer = Column('movie_trailer', String, nullable=True)
    description = Column('description', Text(), nullable=True)
    #repetitive fields
    studio = Column('studio', String)
    relese_date = Column('relese_date', Date)
    director = Column('director', String)
    performers = Column('performers', ARRAY(String))
    genre = Column('genre', String)
    scenes = Column('scenes', ARRAY(String))
    rating = Column('rating', Float, nullable=True)



class Studio(DeclarativeBase):
    """ c """
    __tablename__ = 'studios'

    studio_id = Column(Integer, primary_key=True)
    studio = Column('studio', String)
    parent_studio = Column('parent_studio', String)
    url = Column('url', String)
    despcription = Column('description', Text())
    #repetative fields


class Genre(DeclarativeBase):
    """ c """
    __tablename__ = 'genres'

    genre_id = Column(Integer, primary_key=True)
    genre_name = Column('genre_name', String)



class Tag(DeclarativeBase):
    """ c """
    __tablename__ = 'Tags'

    tag_id = Column(Integer, primary_key=True)
    tag_name = Column('tag_name', String)



