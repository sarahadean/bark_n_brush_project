from datetime import datetime
# from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import *

if __name__ == '__main__':
    engine = create_engine('sqlite:///barknbrush.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    
    d_1 = Drinks(name="Big Mama Latte", description="espresso with steamed milk & caramel + chocolate + marshmallow", price=8)
    app_1 = Appointment(dog='Chloe', Owner='Sarah', service='Bath + nail trim' price='20')


    session.commit()
    session.close()