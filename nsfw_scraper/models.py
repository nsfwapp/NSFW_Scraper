from sqlalchemy import ForeignKey, create_engine, MetaData, Column, Text,Date, Integer, String, DateTime, ARRAY, Time, Numeric, Table, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import relationship, backref

from nsfw_scraper import settings

DeclarativeBase = declarative_base()
Base = DeclarativeBase

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))

def create_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)

scene_cast_table = Table('scene_cast_table', Base.metadata,
                    Column("scene_id", Integer, ForeignKey('scenes.id')),
                    Column("performer_id", Integer, ForeignKey('performers.id'))
                    )

movie_cast_table = Table('movie_cast_table', Base.metadata,
                    Column("movie_id", Integer, ForeignKey('movies.id')),
                    Column("performer_id", Integer, ForeignKey('performers.id'))
                    )

scene_tags_table = Table('scene_tags_table', Base.metadata,
                    Column("scene_id", Integer, ForeignKey('scenes.id')),
                    Column("tag_id", Integer, ForeignKey('tags.id'))
                    )

movie_tags_table = Table('movie_tags_table', Base.metadata,
                    Column("movie_id", Integer, ForeignKey('movies.id')),
                    Column("tag_id", Integer, ForeignKey('tags.id'))
                    )

movie_genres_table = Table('movie_genres_table', Base.metadata,
                    Column("movie_id", Integer, ForeignKey('movies.id')),
                    Column("genre_id", Integer, ForeignKey('genres.id'))
                    )    

class Scene(DeclarativeBase):  # Scene is entity type and calling-out is entity, title is attribute type
    """ c """
    __tablename__ = 'scenes'
    #unique fields
    id = Column(Integer, primary_key=True)
    title = Column('title', String)
    thumbnail_url = Column('thumbnail_url', String, nullable=True)
    preview_url = Column('preview_url', String, nullable=True)
    length = Column('length', Time, nullable=True)
    description = Column('description', Text(), nullable=True)
    gallary_urls = Column("gallary_urls", ARRAY(String), nullable=True)
    #repetative fields
    
    studio_id = Column(Integer, ForeignKey('studios.id'))

    performers = relationship("Performer",secondary=scene_cast_table, backref='scenes', cascade_backrefs=False)
    
    director_id = Column(Integer, ForeignKey('directors.id'))

    release_date_id = Column(Integer, ForeignKey('releasedates.id'))

    rating_id = Column(Integer, ForeignKey('ratings.id'))

    movie_id = Column(Integer, ForeignKey('movies.id'))

    tags = relationship("Tag", secondary=scene_tags_table, backref='scenes', cascade_backrefs=False)

class Performer(DeclarativeBase):
    """ c """
    __tablename__ = 'performers'

    id = Column(Integer, primary_key=True)
    name = Column('name', String)
    aliases = Column('aliases', Text(), nullable=True)
    gender = Column('gender', Enum('Male', 'Female', 'Trans-M', 'Trans-F', 'Intersex', name='gender_type'))
    description = Column('description', Text(), nullable=True)
    profile_pic = Column('profile_pic', ARRAY(String))
    date_of_birth = Column('date_of_birth', Date, nullable=True) # get age from here
    years_active = Column('years_active', String)
    ethnicity = Column('ethnicity', String)
    birth_place = Column('birth_place', String, nullable=True)
    height = Column('height', String)
    hair_color = Column('hair_color', String)
    eye_color = Column('eye_color', String)
    boobs = Column('boobs', String)
    tattoos = Column('tattoos', String, nullable=True)
    piercings = Column('piercings', String, nullable=True)  
    measurments = Column('measurments', String, nullable=True)


    #repetative fields
    rating_id = Column(Integer, ForeignKey('ratings.id'))
    #rating = relationship("Rating", back_populates='performers')

   # scenes = relationship("Scene", secondary=scene_cast_table, backref='performers', cascade_backrefs=False)

   # movies = relationship("Movie", secondary=movie_cast_table, backref='performers', cascade_backrefs=False)

class Director(DeclarativeBase):
    """ c """
    __tablename__ = 'directors'

    id = Column(Integer, primary_key=True)
    name = Column('name', String, unique=True)

    scenes = relationship("Scene", backref='director', cascade_backrefs=False)

    movies = relationship("Movie", backref='director', cascade_backrefs=False)


class ReleaseDate(DeclarativeBase):
    """ c """
    __tablename__ = 'releasedates'

    id = Column(Integer, primary_key=True)
    release_date = Column('relesse_date', Date, unique=True)

    scenes = relationship("Scene", backref='release_date', cascade_backrefs=False)

    movies = relationship("Movie", backref='release_date', cascade_backrefs=False)


class Rating(DeclarativeBase):
    """ c """
    __tablename__ = 'ratings'

    id = Column(Integer, primary_key=True)
    rating = Column('rating', Numeric, unique=True)

    performers =relationship("Performer", backref = "rating", cascade_backrefs=False)

    scenes = relationship("Scene", backref='rating', cascade_backrefs=False)

    movies = relationship("Movie", backref='rating', cascade_backrefs=False)


class Movie(DeclarativeBase):
    """ Movie Model """
    __tablename__ = 'movies'
    #unique fields
    id = Column(Integer, primary_key=True)
    movie_title = Column('movie_title', String)
    movie_cover = Column('movie_cover', ARRAY(String))
    length = Column('length', Time)
    movie_trailer = Column('movie_trailer', String, nullable=True)
    description = Column('description', Text(), nullable=True)
    gallary_urls = Column("gallary_urls", ARRAY(String), nullable=True)
    #repetitive fields
    studio_id = Column(Integer, ForeignKey('studios.id'))

    director_id = Column(Integer, ForeignKey('directors.id'))

    performers = relationship("Performer", secondary=movie_cast_table, backref='movies')

    release_date_id = Column(Integer, ForeignKey('releasedates.id'))

    rating_id = Column(Integer, ForeignKey('ratings.id'))
    
    scenes = relationship("Scene", backref='movie', cascade_backrefs=False)

    genres = relationship("Genre", secondary=movie_genres_table, backref='movies',  cascade_backrefs=False)

    tags = relationship("Tag", secondary=movie_tags_table, backref='movies', cascade_backrefs=False)




class Studio(DeclarativeBase):
    """ c """
    __tablename__ = 'studios'

    id = Column(Integer, primary_key=True)
    studio = Column('studio', String, unique=True)
    parent_studio = Column('parent_studio', String, nullable=True)
    url = Column('url', String, nullable=True)
    despcription = Column('description', Text(), nullable=True)
    #repetative fields

    movies = relationship("Movie", backref="studio", cascade_backrefs=False)

    scenes = relationship("Scene", backref="studio", cascade_backrefs=False)


class Genre(DeclarativeBase):
    """ c """
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True)
    genre_name = Column('genre_name', String)

    #movies = relationship("Movie", secondary=movie_genres_table, back_populates='genres')



class Tag(DeclarativeBase):
    """ c """
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    tag_name = Column('tag', String, unique=True)

    #scenes = relationship("Scene", secondary=scene_tags_table, back_populates='tags') # back_populates ref to tag defiend in scenes table and vice versa 

    #movies = relationship("Movie", secondary=movie_tags_table, back_populates='tags')


