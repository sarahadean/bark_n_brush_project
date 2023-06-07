from rich.console import Console
from rich.theme import Theme
from rich.table import Table
from rich.markdown import Markdown
from models import *
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
import time
from rich.progress import track

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
        self.start()

    def start(self):
        console.print(md)
        input("Press Enter to continue...")

    def create_table_list(self):
        
        console = Console()
        console.print(table)
        pass