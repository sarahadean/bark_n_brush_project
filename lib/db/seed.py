from datetime import datetime
# from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import *
Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    engine = create_engine('sqlite:///barknbrush.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    

    dog1  = Dog(name = 'Tucker', breed = 'Labradoodle', age = 3)
    dog2 = Dog(name = 'Doug', breed = 'Pug', age = 5)
    dog3 = Dog(name = 'Thor', breed = 'Husky', age = 7)

    owner1 = Owner(name = 'Matt')
    owner2 = Owner(name = 'Matty')
    owner3 = Owner(name = 'Sarah')

    session.add_all([dog1, dog2, dog3, owner1, owner2, owner3])

    session.commit()
    session.close()