from datetime import datetime
# from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Dog, Owner, Appointment

if __name__ == '__main__':
    engine = create_engine('sqlite:///barknbrush.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    session.query(Dog).delete()
    session.query(Owner).delete()

    #Appoinment: 
    # date_and_time
    # service
    # price
    # dog_id
    # owner_id
    # best_friends
    # owners

    #Dog:
    # name
    # breed
    # age


    
    owner1 = Owner(name = 'Matt')
    owner2 = Owner(name = 'Matty')
    owner3 = Owner(name = 'Sarah')

    dog1  = Dog(name = 'Tucker', breed = 'Labradoodle', age = 3)
    dog2 = Dog(name = 'Doug', breed = 'Pug', age = 5)
    dog3 = Dog(name = 'Thor', breed = 'Husky', age = 7)

#Teddy Code
    appointment1 = Appointment(date_and_time=datetime.now(), service='Grooming', price=50)
    appointment2 = Appointment(date_and_time=datetime.now(), service='Walk', price=25)
    
    # Associate dogs and owners with appointments
    dog1.appointments.append(appointment1)
    dog2.appointments.append(appointment1)
    dog2.appointments.append(appointment2)
    dog3.appointments.append(appointment2)
    
    owner1.appointments.append(appointment1)
    owner2.appointments.append(appointment1)
    owner2.appointments.append(appointment2)
    owner3.appointments.append(appointment2)
    
    session.add_all([dog1, dog2, dog3, owner1, owner2, owner3, appointment1, appointment2])
    session.commit()
    session.close()
#Teddy Code end
    
    # session.add_all([dog1, dog2, dog3, owner1, owner2, owner3])
    # session.commit()
    # session.close()