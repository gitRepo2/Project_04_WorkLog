#!/user/bin/env python
import datetime
import pytz
from peewee import *
import dateutil.parser
import pep8

import worklogMain
import utility

db = SqliteDatabase('worklog.db')


class TaskEntry(Model):
    timestamp_of_entry = DateTimeField(default=datetime.datetime.now)
    first_name = TextField()
    family_name = TextField()
    task_title = TextField()
    due_date = DateTimeField()
    time_spent = IntegerField()  # in minutes
    notes = TextField()

    class Meta:
        database = db


def initialize_database():
    db.connect()
    db.create_tables([TaskEntry], safe=True)


def teardown():
    db.close()


def add_task_to_db(first_name, family_name, title, date, time_spent, notes):
    """This method adds a task into the database."""
    # Enter the data into the database
    try:
        TaskEntry.create(first_name=first_name,
                         family_name=family_name,
                         task_title=title,
                         due_date=date,
                         time_spent=time_spent,
                         notes=notes)
    except Exception as e:
        print("Error. A task could not be written to the database.")


def view_task(task):
    # Parse task.due_date in printable date
    date_to_print = utility.convert_utcdate_to_datestring(task.due_date)
    # task.time_spent
    time_spent_to_print = utility.convert_minutes_time_format(task.time_spent)
    output = '=' * 60
    output += '\nTask title: ' + task.task_title
    output += "\n" + '=' * 60
    output += "\nEmployee's first name: " + task.first_name
    output += "\nEmployee's last name: " + task.family_name
    output += "\nTask's due date: " + date_to_print
    output += "\nTime spent on task: " + time_spent_to_print
    output += "\nNotes: " + task.notes
    output += "\n" + '=' * 60
    return output


def delete_task_from_db(task):
    """Delete a task from the database."""
    task.delete_instance()


checker = pep8.Checker('dbInteraction.py')
checker.check_all()
