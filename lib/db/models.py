from datetime import datetime

from sqlalchemy import create_engine, desc, func
from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from typing import List

engine = create_engine('sqlite:///barknbrush.db')
Base = declarative_base()

appointment_user = Table(
    'appointment_users',
    Base.metadata,
    #Column('attribute name', ForeignKey(table.id))
    Column('dog_id', ForeignKey('dogs.id'), primary_key=True),
    Column('owner_id', ForeignKey('owners.id'), primary_key=True),
    extend_existing=True,
)

class Dog(Base):
    __tablename__ = 'dogs'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    breed = Column(String())
    age = Column(Integer())
    

    # owner_id = Column(Integer(), ForeignKey('owners.id'))
    # owner = relationship('Owner', back_populates='best_friend')

    #column = relationship('Class_we're_pointing_to', back_populates='column_in_class_referred')
    owners = relationship('Owner', secondary=appointment_user, back_populates='best_friends')
    appointments = relationship('Appointment', backref=backref('dog'), cascade='all, delete-orphan')

    def __repr__(self):
        return f"Dog ID {self.id}," \
            + f" Name: {self.name}," \
            + f" Breed: {self.breed}," \
            + f" Age: {self.age}," \
            # + f" Owner: {self.owner}," \
            # + f" Owner ID: {self.owner_id},"


class Owner(Base):
    __tablename__ = 'owners'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    # dog = Column(String())

    # best_friend = relationship('Dog', back_populates='owner')

    best_friends = relationship('Dog', secondary=appointment_user, back_populates='owners')
    appointments = relationship('Appointment', backref=backref('owner'), cascade='all, delete-orphan')

    def __repr__(self):
        return f"Owner ID {self.id}:" \
            + f" Name: {self.name},"


class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer(), primary_key=True)
    date_and_time = Column(DateTime(), server_default=func.now())
    service = Column(String())
    price = Column(Integer())
    
    dog_id = Column(Integer(), ForeignKey('dogs.id'))
    owner_id = Column(Integer(), ForeignKey('owners.id'))

    # best_friends = relationship('Dog', secondary=appointment_user, back_populates='appointments')
    # owners = relationship('Owner', secondary=appointment_user, back_populates='best_friends')
    
    def __repr__(self):
        return f"Appointment ID {self.id}:" \
            + f" Date and Time: {self.date_and_time,}" \
            + f" Service: {self.service}," \
            + f" Price: {self.price}," \
            
Base.metadata.create_all(bind=engine)