from sqlalchemy import create_engine, MetaData, Column, Text, Integer, String, DateTime, ARRAY, Time, Float, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

DeclarativeBase = declarative_base()

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(f'sqlite:///../{os.getenv("DATABASE")}')

def create_scenes_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)
    
class Scene(DeclarativeBase):
    """ c """
    __tablename__ = 'scenes'

    id = Column(Integer, primary_key=True)
    studio = Column('studio', String(80))
    parent_studio = Column('parent_studio', String, nullable=True)
    title = Column('title', String(100))
    thumbnail_url = Column('thumbnail_url', String, nullable=True)
    preview_url = Column('preview_url', String, nullable=True)
    performers = Column("performers", ARRAY(String))
    director = Column('director', String(80), nullable=True)
    length = Column('length', Time, nullable=True)
    description = Column('description', Text(), nullable=True)
    release_date = Column('release_date', DateTime, nullable=True)
    native_rating = Column('native_rating', Float, nullable=True)
    gallary_urls = Column("gallary_urls", ARRAY(String), nullable=True)



