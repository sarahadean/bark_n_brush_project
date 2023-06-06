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

    
    dog1  = Dog('Tucker', 'Labradoodle', 3)
    dog2 = Dog('Doug', 'Pug', 5)
    dog3 = Dog('Thor', 'Husky', 7)

    owner1 = Owner('Matt')
    owner2 = Owner('Matty')
    owner3 = Owner('Sarah')

    session.commit()
    session.close()