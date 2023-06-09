# THE BARK N BRUSH APPOINTMENT BOOK

Welcome to the BARK N BRUSH APPOINTMENT BOOK, the modern dog groomer's scheduling resource.

Step 1.<code>$ pipenv install</code>

Step 2.<code>$ pipenv shell</code>

Step 3.<code>$ cd lib/db </code>

Step 4.<code>$ python cli.py</code>


You are ready to plan pup pampering.

You will be greeted with a menu of your scheduling options:
1. To view all the appointments scheduled
2. To add a new appointment to your schedule
3. To change a part of an existing appointment
4. To cancel an appointment
5. Exit your appointment book


The <code>Models</code> we created are an Appointment class, an Owner class, and a Dog class. Their relationship best illustrated by this diagram:

         Owner -< Appointment >-Dog


- <code>**show_appts**</code> shows all appointments in a table

- <code>**new_appt**</code> allows the user to add the information of a new client appointment

- <code>**update_appts**</code> allows the user to view existing appointments and update their date and time

- <code>**delete_appt**</code> allows the user to view all appointments and cancel a specific one as necessary


And with all of those you are ready to track your appointments, press <code>5</code> and get to work!



