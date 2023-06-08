from rich.console import Console
from rich.theme import Theme
from rich.table import Table
from rich.markdown import Markdown
from models import Dog, Owner, Appointment
from sqlalchemy import create_engine, update, DateTime, MetaData
from sqlalchemy.orm import sessionmaker
import datetime
from PyInquirer import prompt
from pprint import pprint
from datetime import datetime
from rich.progress import track
from rich.prompt import Prompt

metadata = MetaData()
engine = create_engine('sqlite:///barknbrush.db')
Session = sessionmaker(bind=engine)
session = Session()

MARKDOWN = """
# Welcome to Bark 'n Brush! 

            __    __
            \/----\/
              \0  0/    WOOF!
            _ \  /_
           _|  \/  |_
          | | |  | | |
         _| | |  | | |_
        "---|_|--|_|---"



        
Please select your desired function by number
1. Make new appointment
2. See all scheduled appointments
3. Change an existing appointments
4. Cancel an appointment
5. Exit
"""

console = Console()
md = Markdown(MARKDOWN)

single_appointment = """
# Single Appointment Screen

Please select your desired function by number
1. Show services menu
2. Add a new service
3. List current selected services
4. Delete an item 
5. Checkout 

"""
console = Console()
sa = Markdown(single_appointment)

class CLI:
    def __init__(self):
        # self.dogs = session.query(Dog).all()
        # self.owners = [owner for owner in session.query(Owner)]
        # self.appointments = [appointment for appointment in session.query(Appointment)]
        self.start()

    def start(self):
        exit = False
        while exit == False:

            console.print(md)
            choice = input("Make a selection to continue...")

            if choice == "1":
                self.new_appt()


            if choice == "2":
                self.show_appts()
                input('PRESS ANY KEY WHEN DONE')

            if choice == "3":
                self.update_appts()
                input('MODIFY APPOINTMENT')

            if choice == "4":
                self.show_appts()
                self.delete_appt()    
            elif choice == '5':
                exit = True
    
    def show_appts(self):
      
        table = Table(title='Current Appointments', padding=1,header_style="bold black on #007ba7", style="bold black on #007ba7")
        table.add_column("Dog",  justify="center" , style="bold black on #007ba7")
        table.add_column("Owner", justify="center" , style="bold black on #007ba7")
        table.add_column("Date and Time", justify="center" , style="bold black on #007ba7")
        table.add_column("Service", justify="center", style="bold black on #007ba7")
        table.add_column("Price", justify="center", style="bold black on #007ba7")
        
    #advanced deliverable - under dog name, list breed and age
        query_show_appts = [appointment for appointment in session.query(Appointment)]
        for appointment in query_show_appts:
            table.add_row(f'{appointment.dog.name}', f'{appointment.owner.name}', f'{appointment.date_and_time}', f'{appointment.service}', f'{appointment.price}')

        console.print(table)

    #ask who is owner - enter owner name?
    #ask who is dog - enter dog name, breed, age
    #make sure new owner and dog persist in db
    #session.add()
    #session.commit()

    #!!! COME BACK LATER AND ADD CONTACT INFO ATTRIBUTE FOR OWNER
    def new_appt(self):
        
        dog_name = input('Enter Dog Name: ')
        dog_breed = input('Enter Dog Breed: ')
        dog_age = input('Enter Dog Age: ')

        new_dog=Dog(name=dog_name, breed=dog_breed, age=dog_age)
        session.add(new_dog)
        session.commit()

        owner_name = input('Enter Owner Name: ')
        new_owner = Owner(name=owner_name)
        new_owner.best_friends.append(new_dog)
        session.add(new_owner)
        #session.commit()
        
        # service_choices = {
        #     "1": "Bath",
        #     "2": "Nail Trim",
        #     "3": "Grooming",
        #     "4": "Deluxe Doggie Spa"
        # }

        appt_date_and_time_str = input('Please enter a date and time in the following format: MM/DD/YYYY HH:MM AM/PM. Example: 12/31/2000 12:00 PM:')
        appt_date_and_time_obj = datetime.strptime(appt_date_and_time_str, "%m/%d/%Y %I:%M %p")


        questions = [
            {
                'type' : 'list',
                'name' : 'services',
                'message' : 'Choose A Service:',
                'choices' : [
                        "Bath",
                        "Nail Trim",
                        "Grooming",
                        "Deluxe Doggie Spa"
                ]
            }
        ]
        answers = prompt(questions)
        pprint(answers)
        selected_service = answers['services']

        add_new_appt = Appointment(date_and_time=appt_date_and_time_obj, service=selected_service, price=50, dog_id=new_dog.id, owner_id=new_owner.id)
        
        session.add(add_new_appt)
        session.commit()

        #show table
        #
        #session.query(Appointment).filter(Appointment.id == selected_id)
        #choose id
        #if id == self.id?
    def update_appts(self):
        self.show_appts()
        selected_id = input("Please enter Appointment id..")
        filter_result = session.query(Appointment).filter(Appointment.id == selected_id)

        questions = [
                    {
                        'type' : 'list',
                        'name' : 'fields',
                        'message' : 'Choose Field to update:',
                        'choices' : [
                                "Dog",
                                "Owner",
                                "Date and Time",
                                "Service"
                        ]
                    }
                ]
        answers = prompt(questions)
        pprint(answers)
        selected_update = answers['fields']
        
        pass
        #service_prompt = Prompt.ask(
            #"Please select a service:" , choices = service_choices
       # )
        #session.add(Appointment(service=service_prompt))
        
        # session.commit()

    def delete_appt(self):
        self.show_appts()
        appt_del = input('Select by ID: ')
        filtered_result = session.query(Appointment).filter(Appointment.id == appt_del)
        filtered_result.delete
        session.commit()


CLI()