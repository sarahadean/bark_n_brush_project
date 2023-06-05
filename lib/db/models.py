from sqlalchemy import create_engine, desc, func
from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///barknbrush.db')
Base = declarative_base()

class Dog(Base):
    __tablename__ = 'dogs'

    id = Column(Integer(), primary_key=True)
    breed = Column(String())
    age = Column(Integer())



class Owner():
    __tablename__ = 'owners'

    id = Column(Integer(), primary_key=True)
    name = Column(String())


class Appointment():
    __tablename__ = 'appointments'