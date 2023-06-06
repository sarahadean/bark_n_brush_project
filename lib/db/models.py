from datetime import datetime

from sqlalchemy import create_engine, desc, func
from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///barknbrush.db')
Base = declarative_base()

class Dog(Base):
    __tablename__ = 'dogs'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    breed = Column(String())
    age = Column(Integer())

    def __repr__(self):
        return f"Dog ID {self.id}:" \
            + f" Name: {self.name}," \
            + f" Breed: {self.breed}," \
            + f" Age: {self.age}," 


class Owner(Base):
    __tablename__ = 'owners'

    id = Column(Integer(), primary_key=True)
    name = Column(String())

    def __repr__(self):
        return f"Owner ID {self.id}:" \
            + f" Name: {self.name},"


class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer(), primary_key=True)
    date_and_time = Column(DateTime())
    service = Column(String())
    price = Column(Integer())
    dog_id = Column(Integer(), ForeignKey('dogs.id'))
    owner_id = Column(Integer(), ForeignKey('owners.id'))

    dog = relationship('Dog', backref='dogs')
    owner = relationship('Owner', backref='owners')

    def __repr__(self):
        return f"Appointment ID {self.id}:" \
            + f" Date and Time: {self.date_and_time,}" \
            + f"Service: {self.service}," \
            + f"Price: {self.price}," 
            
