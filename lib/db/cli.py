from rich.console import Console
from rich.theme import Theme
from rich.table import Table
from rich.markdown import Markdown
from models import Dog, Owner, Appointment, Menu_Item
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

#!!!FIND WAY TO CENTER DOG UNDER WELCOME MESSAGE
#!!!ADD MORE ASCII ART - APPT CREATED = SHOW HAPPY DOG, APPT DELETED = SHOW SAD DOG

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
1. View Services Menu
2. View all schedule appointments
3. Make a new appointment
4. Change an existing appointments
5. Cancel an appointment
6. Exit
"""

console = Console()
md = Markdown(MARKDOWN)

new_appt_art = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⠤⠤⠤⠤⢤⣤⣄⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣰⠶⠒⠚⠋⠁⠀⠀⢀⣀⡀⠀⠀⠀⠀⠈⠉⠛⠿⣶⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⢣⣶⠀⠀⠀⠀⠀⢰⣟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⢷⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠞⠁⠀⠀⠀⠀⠀⢘⡿⢿⠓⠚⠿⣷⣤⠀⠀⠀⠀⠀⠀⠀⠀⠉⢻⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⡤⠞⠁⠀⠀⠀⠀⣴⢄⣴⣿⣷⡿⣿⣤⠀⠀⠙⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣀⣤⠴⠶⠞⠛⠛⠛⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⣸⢻⡿⠿⠻⣿⣷⣬⣿⣆⠀⠀⠹⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢀⣴⠾⠟⠿⢶⣶⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠒⠿⣭⣉⣁⣿⣦⠀⠀⠀⠀⠀⠀⠀⣦⣄⡀⠀⠀⠀⠘⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢸⣿⣿⣷⣦⣨⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠃⠀⠀⠀⠀⠀⠀⢀⣀⣹⣿⣷⣄⡀⠀⠀⠀⣰⣿⣿⣷⣦⣀⢸⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢨⣿⣿⢛⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣷⣿⣿⣿⣿⡏⠛⠻⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢸⢿⡿⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⡄⠀⠀⠀⠈⢳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⠟⢡⣤⠄⠈⠻⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢫⢸⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣆⠀⠀⠀⠈⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⠇⢠⣿⡏⠀⠀⠀⠈⠻⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢸⣼⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠦⢤⣤⣿⣿⣿⣿⣶⣤⣀⣀⣀⣤⣾⣿⣿⣿⣿⡿⠣⡞⠋⠉⣿⡀⠀⠀⠀⠀⠈⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠘⢿⣿⠉⠙⠶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠁⠀⠀⢸⡇⠀⠀⠀⠀⠀⢹⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠉⠓⢦⣀⡈⠙⢶⣦⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣀⠀⢸⣿⣶⣷⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠙⠛⢶⣤⣈⠛⠿⠟⠛⠛⠛⠛⠛⠛⠛⠁⠀⢀⡤⠀⣰⡿⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢟⣸⣿⡇⠀⠀⠀⠀⠀⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠳⠶⠶⢾⣿⣶⣄⡀⠀⢠⡶⠿⠿⢿⣿⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣿⡟⠁⠉⠉⣼⡇⠀⠀⠀⠀⣿⢿⡇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⣿⡿⢿⣷⣄⠀⠀⠻⡏⠛⠿⠟⠛⠉⠉⠉⠉⣿⣿⠀⢸⣷⡀⠀⢸⣿⠁⠀⠀⠀⣴⣿⣼⡇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⣷⡀⢻⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⢤⣾⡿⠃⠀⢀⣿⣧⣀⣼⠏⠀⠀⢀⣧⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣧⠀⢻⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⡿⠛⣽⠏⠀⠀⠀⣼⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⡇⠘⡏⠙⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡇⣸⠏⠀⠀⠀⢸⣿⡿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⡄⣇⠀⢻⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣷⡏⠀⠀⠀⢰⣿⣿⡇⢸⠙⣍⠻⣿⣷⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣀⠀⣰⣿⣿⣿⣿⣿⣿⡇⢸⠀⠈⣇⠀⠀⠀⠀⠀⠀⢀⣤⠶⠿⠿⣿⡏⠀⠀⠀⢠⣿⣿⣿⠀⠈⠀⣿⠀⢻⣿⣧⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⢻⣿⣿⣿⣿⣿⣿⣇⡼⠀⠀⢿⠀⠀⠀⠀⠀⢠⠟⠁⠀⢀⣴⠏⠀⠀⠀⢠⣾⠇⣾⢿⠀⠀⠀⣿⠀⠘⠎⣿⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⡇⠉⠀⠀⠀⠘⠃⠀⠀⠀⢀⣸⣀⣠⡴⠟⠁⠀⠀⢀⡴⠛⠁⢠⡟⣿⠀⠀⠀⢿⠀⠀⠀⣿⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⢏⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢙⣿⣶⡴⠖⠀⠀⠀⡞⠀⠀⢠⣿⡇⢻⠀⠀⠀⠘⣆⠀⠀⢻⣧⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡟⢺⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣯⡤⠖⠀⠀⠀⠀⠀⠀⢠⣿⢿⡇⢸⠀⠀⠀⠀⠹⡀⠳⡀⢻⣦⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⣤⢿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠇⢸⡇⣼⠀⠀⡄⠀⠀⢻⡄⠙⣆⠹⣆⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⠵⠖⣀⣀⣤⣤⠀⠀⠀⠀⣸⡏⢀⣾⢳⡏⠀⠀⣧⠀⠀⠀⢿⡄⠘⣦⢻⡆⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⢶⡿⢋⣿⡿⠃⠀⠀⠀⢀⣿⠀⢸⡟⢸⠁⠀⠀⢿⠰⡄⠀⠈⣿⠀⢸⣿⡇⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⠏⣻⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⠏⣼⡷⢋⣿⠃⠀⠀⠀⠀⠸⢿⠀⣼⡇⠀⠀⢀⡄⢸⡆⡇⠀⠀⢹⡇⠀⡏⢣⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⣾⠏⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⣼⠀⣼⣳⢇⡆⠀⣼⡇⢀⣇⠘⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⣿⠀⠀⡤⠀⣀⠀⠀⠀⠀⢹⣧⡆⢰⠋⣰⢣⡟⡾⢰⠀⣿⠁⣾⣿⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡆⠀⣇⠀⡇⠀⠀⠀⡆⠘⣿⠁⣿⠀⣿⣾⣁⡇⣾⢺⣿⢠⣿⡇⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⡄⢿⣦⣿⡀⢦⠀⠸⣦⡙⣧⠹⣧⣿⣿⣿⣷⣿⣾⣿⣿⣿⡇⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢾⣿⣿⣷⣼⣧⣳⣬⣽⣿⣶⡙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠻⠿⠿⠿⠿⠿⠶⠷⠀⠙⢿⣿⣿⣿⣿⣿⣷⠈⠓⠆
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠛⠛⠿⠧⠄⠀
"""

update_art = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⢤⠤⢄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣻⠟⠛⠛⠳⣯⡓⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣞⡿⠋⠀⠀⠀⠀⠀⠻⣮⢳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣀⢴⣿⣭⣭⣟⠶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⡿⠁⠀⠀⠀⠀⡀⠀⠀⠘⢷⡹⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣰⣻⠟⠁⠀⠀⠈⠻⢦⡑⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣞⡾⠁⠀⠀⠀⠀⢠⡿⠀⠠⠀⠈⢷⡹⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣸⣳⠏⠀⠀⠀⠀⠀⠀⠈⠹⣦⡓⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣞⣾⠁⠀⠀⠀⠀⢀⣿⠃⢀⠁⠠⡀⠈⣷⣹⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢠⣯⡟⠀⠀⠀⣤⠀⠀⠀⠀⠀⠈⠻⣮⡣⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡜⣼⠃⠀⠀⠀⠀⠀⣼⡟⢀⠠⠐⠀⢡⠀⠘⣷⢳⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣼⣿⠃⠀⣴⠀⠹⣷⡀⠀⠀⠀⠀⠀⠈⢷⣜⢦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⠏⠀⠀⠀⠀⠀⢰⣿⠀⠄⠂⠐⡈⠀⢃⠀⢹⣎⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⡟⣿⠀⠀⠏⠀⡀⠻⣷⡀⠀⠀⠀⠀⠀⠈⢻⣌⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣏⡿⠀⠀⠀⠀⠀⠀⣸⡟⠀⠰⠀⠂⠡⢀⠸⡀⠈⣿⢿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢸⣟⡏⠀⣠⠂⠐⠀⡀⠙⣿⡄⠀⠀⠀⠀⠀⠀⠙⣧⡳⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⠃⠀⠀⠀⠀⠀⠀⣿⠇⡂⠁⠄⡁⠐⠠⠀⢡⠀⠸⣏⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢸⣿⡇⠀⣟⠀⠠⠁⠀⠄⡈⢿⣆⠐⠀⠀⠀⠀⠀⠈⢿⡜⢦⣀⣤⢴⣖⣶⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⣿⠀⡇⠈⡐⠀⠌⠐⠠⠘⡆⠀⢿⣼⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢸⣿⡇⠀⡯⠀⢂⠠⠁⠠⠀⠌⢿⣆⠀⠀⠀⠀⠀⠀⣀⣿⣾⡿⠛⠋⠉⠉⢹⡄⠀⢠⡿⠀⠀⠀⠀⠀⠀⠀⠀⣿⡄⣠⣐⡀⠁⠌⠠⢁⠀⢣⠀⠸⣏⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢸⣿⡇⠀⢃⠐⠀⠄⠠⠁⡐⠈⡈⣿⡆⠀⠀⢀⣴⠿⠛⠉⢸⡇⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠿⢟⠛⢻⡧⠐⠈⡐⠠⢀⠂⠆⠀⣿⣽⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢸⣿⡇⠀⠀⠂⢈⠀⢂⠐⠀⢂⠐⢸⣧⠀⠀⠀⠀⠀⠐⠀⢸⡁⠀⠀⠀⠀⠈⡗⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣧⣴⣤⡀⠂⢂⠀⡃⠀⢸⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠘⣿⡇⠀⠀⠡⠀⠂⠄⠂⢡⣾⠿⠿⠿⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⣟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠋⠉⠉⣿⡇⠀⠡⠀⢸⠀⠈⣧⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⡿⣿⠀⠠⠁⠐⠠⠐⠠⡘⢿⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣇⠀⠀⠀⠀⠀⢻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡟⠀⢈⠐⠠⠈⠀⠀⣿⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣿⣿⠀⠀⡃⢀⠂⠀⣿⡿⠛⠿⠶⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡀⠀⠀⠀⠀⠘⣧⠀⠀⠀⠀⠀⠀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠈⢷⡀⢀⠈⠄⠐⡀⠀⢼⡾⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢿⣿⡇⠀⡇⠀⡀⠂⢹⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⡇⠀⠀⠀⠀⠀⠈⠳⣄⡀⠀⢀⣾⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠈⢿⡄⠢⠐⠠⠀⠀⢸⡇⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢸⣿⣧⠀⠰⠀⠠⠐⠀⠹⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠟⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠶⣾⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠘⢿⣄⠂⠐⠀⠀⣼⢧⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠈⣿⣿⠀⠘⠄⠐⠀⠌⢠⡿⠀⠀⠀⠀⣀⣤⣦⣶⣤⣴⠏⠀⣀⣤⣴⣶⣶⣶⣦⣤⡀⠀⠀⠙⢿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠜⣿⡀⠈⠀⢠⣿⣿⠁⢀⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠸⣿⣇⠀⠻⡀⠈⠀⣿⠃⠀⠀⢠⣾⣿⣿⡿⢿⣿⠏⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠉⢿⡛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠐⠘⣿⣀⣴⣿⣿⣿⣿⣿⣭⣟⢦⣀⣀⣀⠀⠀
⠀⠀⠀⢻⣻⣆⠀⠱⣀⢩⣿⠀⠀⠀⠠⠟⠋⠁⠀⣰⠃⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠈⢷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⡟⠙⣿⣿⠁⠀⢹⣿⡿⠿⣯⡻⡆
⠀⠀⠀⠈⢻⣻⣦⠀⠉⢸⡗⠀⠀⠀⠀⠀⠀⠀⢠⡟⠀⠀⠀⠈⠛⠿⣿⣿⣿⠿⠛⠉⠀⠀⠀⠀⣀⠀⠀⠈⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⡶⠀⣿⣿⡀⠐⠈⢁⠠⠀⣼⣇⡇
⠀⠀⠀⠀⠀⠙⢽⡷⣦⣽⡇⠀⠀⠀⠀⠀⠀⠀⢰⡇⢀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠸⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⢿⣝⣿⡼⣿⣧⡐⠈⣠⣤⢾⣫⠟⠁
⠀⠀⠀⠀⠀⠀⠀⠙⢻⣿⠇⠀⠀⠀⠀⠀⠀⠀⢸⠇⠘⣧⠀⠀⠀⠀⠀⢀⣾⣧⣄⣀⢀⣀⣠⣾⠋⠀⠀⠀⠀⠙⢦⣀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣻⡇⠀⠘⢿⣿⣛⡿⠷⠋⠁⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⡾⣿⠀⠀⠀⠀⠀⠀⠀⢠⡟⠀⠀⠈⠳⣶⣤⡴⣾⢿⡹⢮⡝⣯⢻⣽⣿⣿⣄⠀⠀⠀⠀⠀⠀⠉⠓⠦⣤⣄⣀⣀⣠⣤⠿⢻⡞⣷⠀⠀⠀⠉⠁⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⣾⣷⣿⠀⠀⠀⠀⠀⣀⡴⠋⠀⠀⠀⠀⠀⠹⣷⡹⣎⢷⡹⢧⣻⣼⠿⣿⣄⠉⠙⢷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢻⣽⣧⣤⣀⣀⣠⡴⠞⠋⠀⠀⠀⠀⠀⠀⠀⠀⠘⠻⣯⣞⣭⣻⣟⣷⡀⢀⠛⢿⡄⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⣶⣶⣶⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⢿⣿⡿⠛⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠛⠛⠛⠻⣧⡈⠐⢈⣡⣾⠏⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⣯⠿⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠘⢿⣓⣶⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠻⠛⠋⠁⠀⠀⠀⠀⠀⠀⠶⠛⠉⢸⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣿⣺⣿⣿⣻⢦⣤⣤⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⢿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⢿⣿⣧⠀⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡿⣾⠹⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⠛⣯⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢈⣷⡿⠀⠘⠻⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠟⠁⠀⢿⣸⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⡇⠀⠀⠖⠀⠙⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⢶⠀⠀⢸⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

delete_art = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡟⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣶⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡿⠀⢻⡆⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠟⠉⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⠜⠀⠈⣷⠀⠀⠀⠀⠀⠀⢀⣴⠟⠁⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠾⠛⠁⠀⠀⠀⣿⠀⠀⠀⠀⣠⡶⢟⠁⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⠟⠁⠀⠀⠀⠀⠀⠀⣿⠀⣀⣴⠞⠋⡰⠋⠀⠀⠀⠀⣠⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠞⠋⠀⠀⠀⠀⠀⠀⠀⢀⣴⣷⠾⠋⠁⢀⡞⠁⠀⠀⠀⠀⢠⢿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠞⠋⠁⠀⠀⠀⠀⠀⠀⣠⣴⡶⠛⠉⠀⠀⠀⠀⣼⠁⠀⠀⠀⠀⠀⢸⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⡤⠴⠖⠒⠚⠛⠉⠉⠙⠛⠒⠲⢤⣄⣤⡶⠛⠉⠀⠀⠀⠀⠀⠀⠀⢰⡇⠀⠀⠀⠀⠀⠀⢸⢸⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣴⠤⠶⠶⠶⠦⠤⣤⣄⣀⣀⣀⣀⣾⠉⣡⠴⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠃⠀⠀⠀⠀⠀⠀⡎⣸⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠈⢉⣡⡤⠟⠛⠳⢤⡀⠀⠀⠀⠀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣄⠀⠀⠀⠀⠀⠀⣰⠇⣠⡴⠀⠀⠀⠀⡸⠃⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣠⣿⣄⣠⣖⣲⣦⡤⠇⠀⠀⠀⠀⠀⠀⢀⣤⠤⠭⣵⣒⢶⣺⣷⢊⣟⣦⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠶⠶⠶⠾⠛⠻⠿⣮⣁⠀⠀⠰⢁⣼⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢻⣤⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⠤⠤⠤⠀⠀⠈⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⣢⣾⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢠⣿⡙⢶⣄⡀⠀⠀⠀⠀⠀⠀⠈⠉⠁⠀⠀⠀⠈⠓⠢⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡴⣶⣵⠾⠋⢳⣶⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⡞⢿⡉⢿⣾⠟⢯⣙⣲⣶⢤⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣶⣾⣿⠾⣟⡉⠀⠀⠀⠀⠈⠿⢿⣶⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⡇⡞⠉⢻⣿⢀⠞⣇⢿⣩⣟⢻⡛⣿⢿⢿⣿⣷⣦⣄⠀⠀⠀⠀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣦⡀⠙⢦⠀⠀⠀⠀⠀⠈⠻⣿⣆⠀⠀⠀⠀⣴⡗⠀⠀
⢻⡇⠀⠀⢿⣸⠀⠈⠀⠁⠈⠛⠿⠻⣏⢦⠶⢧⣙⢙⣧⡀⢀⠀⢿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢳⣜⣿⣆⠀⠀⣸⠀⠀⠀⠀⠀⠀⠀⠙⢿⣦⣤⣠⠞⣽⢀⣰⠀
⠀⠁⠀⠀⠘⢿⠀⠀⠀⠀⠀⠀⠀⠀⠘⢷⡀⠀⢉⣿⠾⡇⠈⢦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⡀⠀⠹⡍⠁⠀⣠⠏⠀⠀⠀⠀⠀⠀⠀⠀⣰⡟⠈⢻⣦⡷⠋⡟⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣧⡾⠋⢀⣠⡇⠀⠈⢳⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡇⠀⠀⢀⣀⣙⣷⡦⡷⠀⡞⠁⠀⠀⠀⠀⠀⠀⠀⢀⣴⠟⠀⢀⡾⠋⠀⣾⠁⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡟⠁⢀⣰⣟⡾⠁⠀⣠⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠇⣠⡤⠶⠾⠟⠉⠀⠀⠀⣇⠀⠀⠀⠀⠀⠀⠀⣰⡿⠋⠀⠀⣻⡄⠀⣼⣧⡀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠟⠀⣤⣼⣹⠟⠀⣀⠼⠃⠀⠀⠀⠀⠀⠀⠀⠀⣠⡾⠋⣰⠋⠀⠀⠀⠀⠀⠀⠀⢸⠏⠀⠀⠀⠀⠀⣠⡾⠏⠀⢀⡤⠛⢹⠋⠋⢁⣿⠋⠉
⠀⠀⠀⢀⣄⠀⠀⠀⠀⠀⠀⢀⡾⠋⠀⣤⣯⡽⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠴⠚⠁⣠⡜⠁⠀⠀⠀⠀⠀⠀⠀⢠⡏⠀⠀⠀⠀⣠⡾⠋⠁⠀⠐⣏⠀⢠⡏⠀⢀⡾⠋⠀⠀
⠀⠀⠀⠀⣿⡇⢸⣆⠀⠀⣰⣿⣄⢸⢦⡷⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄⠀⠀⣠⠟⠁⠀⠀⠀⠀⠀⠀⠀⢠⠏⠀⠀⢀⣠⡾⠋⠀⠀⢰⠋⠉⣿⠛⠋⢀⣴⢟⣁⢤⡤⠀
⠀⠀⠀⠀⢹⣽⣾⡜⢶⣾⠳⣿⣨⠿⠋⠀⠀⢀⣀⡤⠤⢶⣄⠀⠀⠀⠀⠀⠀⣸⠀⣰⠃⠀⠀⠀⠀⠀⠀⠀⢀⡴⠃⠀⣀⡴⣟⠿⠀⠀⠀⠀⠸⠦⠼⠁⢀⣴⠟⠻⠽⠾⠭⠤⠤
⠀⠀⠀⠀⠀⢿⡿⣧⣈⠽⠞⠋⠀⠀⢀⣠⠶⠛⠁⠀⠀⠀⠈⢹⡟⠛⠻⠆⣴⠃⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⣸⣥⣴⠟⠫⠛⠁⢠⠴⠲⡄⠀⠀⠀⣠⣴⠟⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠘⠷⣄⣀⣀⣀⣠⡴⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠹⣧⣀⠀⠸⡇⠀⠀⠀⠀⠀⠀⠀⢠⣾⣯⠾⠛⠉⠀⣀⣀⠀⠀⢺⣀⣀⡏⢀⣤⡾⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣦⣄⣻⣄⠀⠀⠀⢀⣠⠾⢿⣿⣶⣦⣀⠀⡞⠉⢹⠃⠀⠀⢈⣡⡶⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡉⠉⠉⠉⠛⠛⠋⢁⣀⣀⠀⠉⠻⢻⡄⠻⠤⠏⣀⣤⡶⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠴⢾⡿⣟⣆⠀⢰⢦⠀⠀⠈⠧⣸⠆⠀⢀⣼⣁⣠⣴⠿⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠋⣀⣽⣿⡀⠈⠛⠀⠀⠀⠀⣀⣤⣾⡿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢴⠿⠒⠋⠉⠀⠘⡻⢦⡤⠴⠶⠶⡛⡛⢉⣡⣞⡵⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""


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
                self.print_menu()
                input('Press Any Key When Done')

            if choice == "3":
                self.new_appt()
                input("Appointment Created")

            if choice == "2":
                self.show_appts()
                input('Press Any Key When Done')

            if choice == "4":
                self.update_appts()
                input('Appointment updated. Press any key to return to the main menu..')

            if choice == "5":
                self.delete_appt()
                # input('Appointment cancelled. Press any key to return to the main menu..')    
            elif choice == '6':
                exit = True



#-----------SHOW MENU----------------------
    def print_menu(self):
        menu_table = Table(title='Service Menu', padding=1,header_style="bold black on #007ba7", style="bold black on #007ba7")
        menu_table.add_column("Name",  justify="center" , style="bold black on #007ba7")
        menu_table.add_column("Description", justify="center" , style="bold black on #007ba7")
        menu_table.add_column("Price", justify="center", style="bold black on #007ba7")

        query_menu_items = [item for item in session.query(Menu_Item)]
        for item in query_menu_items:
            menu_table.add_row(f'{item.name}', f'{item.description}', f'${item.price}')

        console.print(menu_table)

        

#------------SHOW ALL APPOINTMENTS------------------------ 
# !!!GET FANCY: list dog breed and age with dog name 
    def show_appts(self):
      
        table = Table(title='Current Appointments', padding=1,header_style="bold black on #007ba7", style="bold black on #007ba7")
        table.add_column('Appointment ID', justify='center', style="bold black on #007ba7")
        table.add_column("Dog",  justify="center" , style="bold black on #007ba7")
        table.add_column("Owner", justify="center" , style="bold black on #007ba7")
        table.add_column("Date and Time", justify="center" , style="bold black on #007ba7")
        table.add_column("Service", justify="center", style="bold black on #007ba7")
        table.add_column("Price", justify="center", style="bold black on #007ba7")
        

        query_show_appts = [appointment for appointment in session.query(Appointment)]
        for appointment in query_show_appts:
            appt_datetime_string = appointment.date_and_time.strftime('%B %d %Y %I:%M %p')
            table.add_row(f'{appointment.id}', f'{appointment.dog.name}', f'{appointment.owner.name}', f'{appt_datetime_string}', f'{appointment.service}', f'$ {appointment.price}')

        console.print(table)

    
#--------------MAKES NEW APPOINTMENTS-------------------
#!!!!!!GET FANCY:  - Add contact info for owner - phone number and/or email
#                  - Hard code prices for services
#                  - Show total cost of appointment upon confirmation?
#                  - Can date/time be shown as a string? June 6, 2023
#                  - Able to select multiple services
#                  - Show happy dog ASCII upon appt creation

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
        session.commit()
        
        appt_date_and_time_str = input('Please enter a date and time in the following format: MM/DD/YYYY HH:MM AM/PM. Example: 12/31/2000 12:00 PM:')
        appt_date_and_time_obj = datetime.strptime(appt_date_and_time_str, "%m/%d/%Y %I:%M %p")

        questions = [
            {
                'type' : 'list',
                'name' : 'services',
                'message' : 'Choose A Service:',
                'choices' : [
                        "Nice 'N Easy Bath",
                        "Doggie Facial",
                        "Nail Clipping/Grinding",
                        "Paw Balm",
                        "Furminator De-Shedding",
                        "Deluxe Doggie Spa",
                        "Doggie Daycare",

                ]
            }
        ]
        answers = prompt(questions)
        # pprint(answers)
        selected_service = answers['services']
        #setting the price 
        service_price = int
        if selected_service == "Nice 'N Easy Bath":
            service_price = 35
        elif selected_service == "Doggie Facial":
            service_price = 20
        elif selected_service == "Nail Clipping/Grinding":
            service_price = 20
        elif selected_service == "Paw Balm":
            service_price = 15
        elif selected_service == "Furminator De-Shedding":
            service_price = 50
        elif selected_service == "Deluxe Doggie Spa":
            service_price = 200
        elif selected_service == "Doggie Daycare":
            service_price = 100

#!!!!add Input asking 'Add another service?'
        add_new_appt = Appointment(date_and_time=appt_date_and_time_obj, service=selected_service, price=f' {service_price}', dog_id=new_dog.id, owner_id=new_owner.id)
        #input("Appointment Summary:
        #       Owner:
        #       Dog:
        #       Service(s):
        #       Cost:
        #       Done?
        #       ")
        session.add(add_new_appt)
        session.commit()
        print(new_appt_art)




#--------UPDATES APPOINTMENTS--------------  
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
                                "Date and Time",
                                "Services"
                        ]
                    }
                ]
        answers = prompt(questions)
        # pprint(answers)
        selected_update = answers['fields'] # = Dog, Owner, Date and Time, or Service

        if selected_update == 'Date and Time':
            appt_date_and_time_str = input('Please enter a date and time in the following format: MM/DD/YYYY HH:MM AM/PM. Example: 12/31/2000 12:00 PM:')
            appt_date_and_time_obj = datetime.strptime(appt_date_and_time_str, "%m/%d/%Y %I:%M %p")
            filter_result.update({Appointment.date_and_time: appt_date_and_time_obj})
        elif selected_update == 'Services':
            questions = [
            {
                'type' : 'list',
                'name' : 'services',
                'message' : 'Choose A Service:',
                'choices' : [
                        "Nice 'N Easy Bath",
                        "Doggie Facial",
                        "Nail Clipping/Grinding",
                        "Paw Balm",
                        "Furminator De-Shedding",
                        "Deluxe Doggie Spa",
                        "Doggie Daycare",
                ]
            }
        ]
            answers = prompt(questions)
            pprint(answers)
            selected_service = answers['services']
            filter_result.update({Appointment.service: selected_service})
            print(update_art)
        else:
            input('Press any key to discard changes and go back to main menu')
        
        session.commit()
       


#---------------DELETE APPOINTMENTS------------------------------
#!!!!!!GET FANCY: - Show id or dogname with cancellation confirmation message:
#                   (Are you sure you want to cancel Tucker's appointment?)
    def delete_appt(self):
        self.show_appts()
        appt_del = int(input('ID you wish to delete: '))
        query_show_appts = [appointment for appointment in session.query(Appointment)]
        for appointment in query_show_appts:
            if appointment.id == appt_del:
                confirm = input(f'Press "Enter" to confirm cancellation for {appointment.dog.name}.')
                session.delete(appointment)
                session.commit()
                print(delete_art)
                self.show_appts()
                input('Appointment cancelled. Press any key to return to the main menu..')   
                break
        else:
            input('No appointment found with the specified ID. Press "Enter" to return to the main menu')





        # filtered_result = session.query(Appointment).filter(Appointment.id == appt_del)
        # confirm = input(f'Press any key to confirm cancellation for {filtered_result.dog_id}.')
        # filtered_result.delete()
        # session.commit()





    def close_appts(self):

        ascii_goodbye = """
    
                                                                                                    
                                                                                        
        ░░                    ░░        ██████████  ░░                    ░░            
                                    ████          ████                                  
                                  ████              ████                                
░░      ░░                    ░░██                      ██░░              ░░            
        ░░            ░░      ░░██  ██  ██      ██  ██  ██░░      ░░      ░░            
                              ██    ██              ██    ██                            
                              ██    ██              ██    ██                            
░░░░░░░░░░░░░░  ░░░░░░░░░░░░██      ██    ██████    ██      ██░░░░░░░░░░░░░░░░░░  ░░░░░░
        ░░            ░░    ██    ██        ██        ██    ██    ░░      ░░            
                            ██  ████    ██  ██  ██    ████  ██                          
                              ██  ██      ██  ██      ██  ██                            
                                    ██              ██                                  
                                      ██████████████                                    
                                    ██              ██                                  
                                    ██              ██                                  
                                    ██    ██  ██    ██                                  
                                  ████    ██  ██    ████                                
                                  ████    ██  ██    ████                                
                                ██  ██    ██  ██    ██  ██                              
                      ░░        ██  ██    ██  ██    ██  ██        ░░                    
                                  ████    ██████    ████                                
                                ██    ████      ████    ██                              
  ░░░░░░  ░░░░  ░░░░░░  ░░░░░░  ██████    ░░  ░░    ██████░░░░░░░░  ░░░░░░  ░░░░  ░░░░░░
        ░░            ░░      ░░                                  ░░      ░░            
                                                                                        
                                                                                        
                            LET'S HAVE A DOGGONE GOOD DAY!!!!!!
 
    
    
        """

        console.print(ascii_goodbye)
        







if __name__=='__main__':
    cli =CLI()
    cli.close_appts()