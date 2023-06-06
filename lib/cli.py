from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, update
from models import *

engine = create_engine('sqlite:///barknbrush.db')
Session = sessionmaker(bind=engine)
session = Session()