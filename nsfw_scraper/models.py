from sqlalchemy import create_engine, Column, Integer, String, DateTime, ARRAY, Time, Float
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

def Scene(DeclarativeBase):
    """ sql alchemy Scenes Model """
    __tablename__ = "scenes"

    id = Column(Integer, primary_key=True)
    studio = Column('studio', String, nullable=True)
    parent_studio = Column('parent_studio', String, nullable=True)
    title = Column('title', String)
    thumbnail_url = Column('thumbnail_url', String, nullable=True)
    preview_url = Column('preview_url', String, nullable=True)
    performers = Column("performers", ARRAY(String))
    director = Column('director', String, nullable=True)
    length = Column('length', Time, nullable=True)
    description = Column('description', String, nullable=True)
    release_date = Column('release_date', DateTime, nullable=True)
    native_rating = Column('native_rating', Float, nullable=True)
    gallary_urls = Column("gallary_urls", ARRAY(String))