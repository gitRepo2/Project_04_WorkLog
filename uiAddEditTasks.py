#!/user/bin/env python
import pytz
import datetime
import regex
import pep8

import utility
import dbInteraction


def add_task_ui():
    """This method take self as argument and ask the user to input
    all necessary information to add a task. The new task is added to
    the database."""
    while True:
        # Ask for the name of the user
        first_name = input("Please key in your first name. ")
        family_name = input("Please key in your last name. ")
        task_title = input("Please key in the name of the task. ")
        print("\nWhen is this task due? ")
        while True:
            date_input = input("Please use MM/DD/YYYY format. ")
            try:
                utc_date = utility.convert_datetime_to_utc(date_input)
                break
            except Exception:
                print("'{}' doesn't seem to be a valid date.".format(
                    date_input))
        # Ask for time spent on the task
        print("\nHow much time did you spend on task '{}'? ".format(
            task_title))
        while True:
            time_input = input("Please add a time in Minutes. ")
            try:
                time_spent = int(time_input)
                if time_spent < 0:
                    print("That's not positive number. Please try again.")
                    continue
                break
            except ValueError:
                print("'{}' doesn't seem to be a valid time in Minutes.".
                      format(time_input))
        # Ask for notes to the task
        notes = input("Please key any notes to this task. ")
        break
    # Add (write) the new task into the database
    dbInteraction.add_task_to_db(first_name, family_name, task_title,
                                 utc_date, time_spent, notes)
    print('Task was successfully added.')


def edit_task(task):
    """This method takes self and a task as argument. The user is guided
    step by step to edit the task.
    Records can be deleted and edited, letting the user change the date,
    task name, time spent, and/or notes. Once done, the task is update in the
    database."""
    # Ask for the name of the user
    print('\n' + '=' * 60)
    while True:
        # Ask for the name of the task
        print("Your task to edit: '{}'. ".format(task.task_title))
        task_title = input("Please key in your new task name. ")
        print("\nWhat is the task's new due date? ")
        # Ask for the date of the task
        while True:
            date_input = input("Please use MM/DD/YYYY format. ")
            try:
                utc_date = utility.convert_datetime_to_utc(date_input)
                break
            except Exception:  # ValueError:
                print("{} doesn't seem to be a valid date.".format(
                    date_input))
        # Ask for time spent on the task
        text = "\nHow much time does it take to finish the task "
        print(text + "'{}'? ".format(task_title))
        while True:
            time_input = input("Please add a time in Minutes. ")
            try:
                time_spent = int(time_input)
                if time_spent < 0:
                    print("That's not positive number. Please try again.")
                    continue
                break
            except ValueError:
                print("'{}' doesn't seem to be a valid time in Minutes.".
                      format(time_input))
        # Ask for notes to the task
        notes = input("Please key any notes to this task. ")
        break
    # Remove old task from database
    dbInteraction.delete_task_from_db(task)
    # Add (write) the new task into the database
    dbInteraction.add_task_to_db(task.first_name, task.family_name, task_title,
                                 utc_date, time_spent, notes)
    print('Task was successfully edited.')

checker = pep8.Checker('uiAddEditTasks.py')
checker.check_all()
