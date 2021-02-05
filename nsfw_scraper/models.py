from mongoengine import connect, Document, StringField, IntField, URLField, DateTimeField, ListField, FloatField, ReferenceField
from sqlalchemy.orm import relationship
  
class Scene(Document):  # Scene is entity type and calling-out is entity, title is attribute type
    #unique fields
    title = StringField(required=True)
    thumbnail_url = URLField()
    preview_url = URLField()
    length = DateTimeField()
    description = StringField()
    gallary_urls = ListField()
    #repetative fields
    
    studio_id = ReferenceField('Studio')

    performers = relationship("Performer", backref='scenes', cascade_backrefs=False)
    
    director_id = ReferenceField('Director')

    release_date_id = ReferenceField('ReleaseDate')

    rating_id = ReferenceField('Rating')

    movie_id = ReferenceField('Movie')

    tags = relationship("Tag", backref='scenes', cascade_backrefs=False)

    meta = { 'collection': 'scenes'}

class Performer(Document):

    id = IntField(required=True)
    name = StringField(required=True)
    aliases = StringField()
    gender = StringField()
    description = StringField()
    profile_pic = URLField()
    date_of_birth = DateTimeField()
    years_active = StringField()
    ethnicity = StringField()
    birth_place = StringField()
    height = StringField()
    hair_color = StringField()
    eye_color = StringField()
    boobs = StringField()
    tattoos = StringField()
    piercings = StringField() 
    measurments = StringField()


    #repetative fields
    rating_id = ReferenceField('Rating')

    meta = { 'collection': 'performers'}
    #rating = relationship("Rating", back_populates='performers')

   # scenes = relationship("Scene", secondary=scene_cast_table, backref='performers', cascade_backrefs=False)

   # movies = relationship("Movie", secondary=movie_cast_table, backref='performers', cascade_backrefs=False)

class Director(Document):

    name = StringField(required=True)

    scenes = ReferenceField('Scene')

    movies = ReferenceField('Movie')

    meta = { 'collection': 'directors'}


class ReleaseDate(Document):

    release_date = DateTimeField(required=True)

    scenes = ReferenceField('Scene')

    movies = ReferenceField('Movie')

    meta = { 'collection': 'releasedates'}


class Rating(Document):

    rating = FloatField(required=True)

    performers = ReferenceField('Performer')

    scenes = ReferenceField('Scene')

    movies = ReferenceField('Movie')

    meta = { 'collection': 'ratings'}


class Movie(Document):

    movie_title = StringField(required=True)
    movie_cover = ListField(URLField())
    length = DateTimeField()
    movie_trailer = URLField()
    description = StringField()
    gallary_urls = ListField(URLField())
    #repetitive fields
    
    scenes = relationship("Scene", backref='movie', cascade_backrefs=False)

    studio_id = ReferenceField('Studio')

    performers = relationship("Performer", backref='scenes', cascade_backrefs=False)
    
    director_id = ReferenceField('Director')

    release_date_id = ReferenceField('ReleaseDate')

    rating_id = ReferenceField('Rating')

    scene_id = ReferenceField('Scene')

    tags = relationship("Tag", backref='scenes', cascade_backrefs=False)

    genres = relationship("Genre", backref='movies',  cascade_backrefs=False)


    meta = { 'collection': 'movies'}




class Studio(Document):

    studio = StringField(required=True)
    parent_studio = StringField()
    url = URLField()
    despcription = StringField()
    #repetative fields

    scenes = ReferenceField('Scene')

    movies = ReferenceField('Movie')


    meta = { 'collection': 'studios'}


class Genre(Document):

    genre_name = StringField(required=True)


    #movies = relationship("Movie", secondary=movie_genres_table, back_populates='genres')

    meta = { 'collection': 'genres'}



class Tag(Document):

    tag = StringField(required=True)

    #scenes = relationship("Scene", secondary=scene_tags_table, back_populates='tags') # back_populates ref to tag defiend in scenes table and vice versa 

    #movies = relationship("Movie", secondary=movie_tags_table, back_populates='tags')

    meta = { 'collection': 'tags'}


