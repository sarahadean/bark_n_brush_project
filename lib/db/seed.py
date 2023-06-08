from datetime import datetime
# from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Dog, Owner, Appointment, Menu_Item

if __name__ == '__main__':
    engine = create_engine('sqlite:///barknbrush.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Dog).delete()
    session.query(Owner).delete()
    session.query(Appointment).delete()

    # Appoinment:
    # date_and_time
    # service
    # price
    # dog_id
    # owner_id

    # Dog:
    # name
    # breed
    # age

    owner1 = Owner(name='Matt')
    owner2 = Owner(name='Matty')
    owner3 = Owner(name='Sarah')
    owner4 = Owner(name="Evan")
    owner5 = Owner(name="Ash")

    dog1 = Dog(name='Tucker', breed='Labradoodle', age=3)
    dog2 = Dog(name='Doug', breed='Pug', age=5)
    dog3 = Dog(name='Thor', breed='Husky', age=7)
    dog4 = Dog(name='Big Boy', breed='Beagle', age=2)
    dog5 = Dog(name="Growlithe", breed='Pokemon', age=1)

# Teddy Code
    appointment1 = Appointment(
        date_and_time=datetime(2023, 7, 21, 9, 30, 15), service='Grooming', price=50)
    appointment2 = Appointment(
        date_and_time=datetime(2023, 8, 2, 12, 45, 20), service='Walk', price=25)
    appointment3 = Appointment(
        date_and_time=datetime(2023, 9, 10, 16, 0, 5), service='Grooming', price=50)
    appointment4 = Appointment(
        date_and_time=datetime(2023, 10, 5, 8, 15, 35), service='Walk', price=25)
    appointment5 = Appointment(
        date_and_time=datetime(2023, 11, 18, 20, 50, 10), service='Grooming', price=50)

    # Associate dogs and owners with appointments
    dog1.appointments.append(appointment1)
    dog2.appointments.append(appointment2)
    dog3.appointments.append(appointment3)
    dog4.appointments.append(appointment4)
    dog5.appointments.append(appointment5)

    owner1.appointments.append(appointment1)
    owner2.appointments.append(appointment2)
    owner3.appointments.append(appointment3)
    owner4.appointments.append(appointment4)
    owner5.appointments.append(appointment5)

    # name
    # description
    # price

    m1 = Menu_Item(name="Nice 'N Easy Bath", description="A simple and relaxing bath that includes: brush out, ear cleaning, nail clip, cologne.", price=35)
    m2 = Menu_Item(name="Doggie Facial", description="Our blueberry and apricot facial helps clear eye stains while cleaning and brightening your face of your pet.", price=20)
    m3 = Menu_Item(name="Nail Clipping/Grinding", description="This process is quick and a pain-free way to trim and smooth nails", price=20)
    m4 = Menu_Item(name="Paw Palm", description="Our paw balm conditions and soothes dry, cracked paws and itchy hot spots. It contains infusions of certified organic botanicals such as calendula and sunflower seed oil.", price=15)
    m5 = Menu_Item(name="Furminator Treatment", description="We remove the old, loose undercoat from your pet. This treatment can eliminate up to 90 percent of shedding from your pet at home", price=50)
    m6 = Menu_Item(name="Deluxe Doggie Spa", description="Bring your pupper by for a relaxing day. Includes all services listed above.", price=200)
    m7 = Menu_Item(name="Doggie Daycare", description="Our facility has a dog pool, sprinkler, playground and toys galore!", price=100)

    session.add_all([dog1, dog2, dog3, dog4, dog5, owner1, owner2,
                    owner3, owner4, owner5, appointment1, appointment2, appointment3, appointment4, appointment5])
    session.commit()
    session.close()


# Teddy Code end

    # session.add_all([dog1, dog2, dog3, owner1, owner2, owner3])
    # session.commit()
    # session.close()
