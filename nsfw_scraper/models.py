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

    id = Column(Integer, primary_key=True)
    studio = Column('studio', String)
    parent_studio = Column('parent_studio', String, nullable=True)
    title = Column('title', String)
    thumbnail_url = Column('thumbnail_url', String, nullable=True)
    preview_url = Column('preview_url', String, nullable=True)
    performers = Column("performers", ARRAY(String))
    director = Column('director', String, nullable=True)
    length = Column('length', Time, nullable=True)
    description = Column('description', Text(), nullable=True)
    release_date = Column('release_date', Date, nullable=True)
    rating_native = Column('native_rating', Float, nullable=True)
    gallary_urls = Column("gallary_urls", ARRAY(String), nullable=True)


class Performer(DeclarativeBase):
    """ c """
    __tablename__ = 'performers'

    id = Column(Integer, primary_key=True)
    name = Column('name', String)
    description = Column('description', Text(), nullable=True)
    profile_pic = Column('profile_pic', String)
    date_of_birth = Column('date_of_birth', String, nullable=True)
    birth_place = Column('birth_place', String, nullable=True)
    height = Column('height', String)
    measurments = Column('measurments', String, nullable=True)



