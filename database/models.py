from .database import Base
from sqlalchemy import Column, Integer, String, DateTime, Date
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship


class DbUser(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    events = relationship('DbEvents', back_populates='users', cascade='all, delete')


class DbEvents(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    event = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    qr_code_uuid = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    users = relationship('DbUser', back_populates='events', cascade='all, delete')
    categories = relationship("DbCategories", secondary="event_categories", back_populates='events')
    images = relationship('DbImages', back_populates='events', cascade='all, delete')
    other_users = relationship('DbOtherUsers', back_populates='events')


class DbImages(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True, autoincrement=True)
    image_name = Column(String, nullable=False)
    event_id = Column(Integer, ForeignKey('events.id'))
    other_users_id = Column(Integer, ForeignKey('other_users.id'))
    events = relationship("DbEvents", back_populates='images')
    other_users = relationship('DbOtherUsers', back_populates='images')



class DbCategories(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category = Column(String, nullable=False, unique=True)
    events = relationship("DbEvents", secondary="event_categories", back_populates='categories')



class EventCategories(Base):
    __tablename__ = 'event_categories'
    event_id = Column(Integer, ForeignKey('events.id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'), primary_key=True)



class DbOtherUsers(Base):
    __tablename__ = 'other_users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    device_name = Column(String, nullable=False)
    device_ip = Column(String, nullable=False)
    event_id = Column(Integer, ForeignKey('events.id'))
    
    events = relationship("DbEvents", back_populates='other_users')
    images = relationship('DbImages', back_populates='other_users')