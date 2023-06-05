from datetime import datetime

from sqlalchemy import create_engine, desc, func
from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

if __name__ == '__main__':
    engine = create_engine('sqlite:///barknbrush.db')
    Base = declarative_base()


class Dog(Base):
    __tablename__ = 'dogs'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    breed = Column(String())
    age = Column(Integer())


class Owner(Base):
    __tablename__ = 'owners'

    id = Column(Integer(), primary_key=True)
    name = Column(String())


class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer(), primary_key=True)
    date_and_time = Column(DateTime())
    service = Column(String())
    price = Column(Integer())
    dog_id = Column(Integer, ForeignKey('dogs.id'))
    owner_id = Column(Integer(), ForeignKey('owners.id'))

    dog = relationship('Dog', backref='dogs')
    owner = relationship('Owner', backref='owners')
