from sqlalchemy import ForeignKey, create_engine, MetaData, Column, Text,Date, Integer, String, DateTime, ARRAY, Time, Float, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import relationship

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
    studio = relationship("Studio", back_populates='scenes')

    performers = relationship("Performer",secondary=scene_cast_table, back_populates='scenes')
    
    director_id = Column(Integer, ForeignKey('directors.id'))
    director = relationship("Director", back_populates='scenes')

    release_date_id = Column(Integer, ForeignKey('releasedates.id'))
    release_date = relationship("ReleaseDate", back_populates='scenes')

    rating_id = Column(Integer, ForeignKey('ratings.id'))
    rating = relationship("Rating", back_populates='scenes')

    movie_id = Column(Integer, ForeignKey('movies.id'))
    movie = relationship("Movie", back_populates='scenes')

    tags = relationship("Tag", secondary=scene_tags_table, back_populates='scenes')

class Performer(DeclarativeBase):
    """ c """
    __tablename__ = 'performers'

    id = Column(Integer, primary_key=True)
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

    #repetative fields
    rating_id = Column(Integer, ForeignKey('ratings.id'))
    rating = relationship("Rating", back_populates='performers')

    scenes = relationship("Scene", secondary=scene_cast_table, back_populates='performers')

    movies = relationship("Movie", secondary=movie_cast_table, back_populates='performers')

class Director(DeclarativeBase):
    """ c """
    __tablename__ = 'directors'

    id = Column(Integer, primary_key=True)
    name = Column('name', String)

    scenes = relationship("Scene", back_populates='director')

    movies = relationship("Movie", back_populates='director')


class ReleaseDate(DeclarativeBase):
    """ c """
    __tablename__ = 'releasedates'

    id = Column(Integer, primary_key=True)
    release_date = Column('relesse_date', Date)

    scenes = relationship("Scene", back_populates='release_date')

    movies = relationship("Movie", back_populates='release_date')


class Rating(DeclarativeBase):
    """ c """
    __tablename__ = 'ratings'

    id = Column(Integer, primary_key=True)
    rating = Column('rating', Float)

    performers =relationship("Performer", back_populates='rating')

    scenes = relationship("Scene", back_populates='rating')

    movies = relationship("Movie", back_populates='rating')


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
    #repetitive fields
    studio_id = Column(Integer, ForeignKey('studios.id'))
    studio = relationship("Studio", back_populates='movies')

    director_id = Column(Integer, ForeignKey('directors.id'))
    director = relationship("Director", back_populates='movies')

    performers = relationship("Performer", secondary=movie_cast_table, back_populates='movies')

    release_date_id = Column(Integer, ForeignKey('releasedates.id'))
    release_date = relationship("ReleaseDate", back_populates='movies')

    rating_id = Column(Integer, ForeignKey('ratings.id'))
    rating = relationship("Rating", back_populates='movies')
    
    scenes = relationship("Scene", back_populates='movie')

    genres = relationship("Genre", secondary=movie_genres_table, back_populates='movies')

    tags = relationship("Tag", secondary=movie_tags_table, back_populates='movies')




class Studio(DeclarativeBase):
    """ c """
    __tablename__ = 'studios'

    id = Column(Integer, primary_key=True)
    studio = Column('studio', String)
    parent_studio = Column('parent_studio', String)
    url = Column('url', String)
    despcription = Column('description', Text())
    #repetative fields

    movies = relationship("Movie", back_populates="studio")

    scenes = relationship("Scene", back_populates="studio")


class Genre(DeclarativeBase):
    """ c """
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True)
    genre_name = Column('genre_name', String)

    movies = relationship("Movie", secondary=movie_genres_table, back_populates='genres')



class Tag(DeclarativeBase):
    """ c """
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    tag = Column('tag', String)

    scenes = relationship("Scene", secondary=scene_tags_table, back_populates='tags') # back_populates ref to tag defiend in scenes table and vice versa 

    movies = relationship("Movie", secondary=movie_tags_table, back_populates='tags')


