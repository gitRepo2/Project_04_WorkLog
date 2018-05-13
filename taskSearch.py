#!/user/bin/env python
import datetime
import pytz
import regex
import dbInteraction
import dateutil.parser
import pep8

import utility


def search_by_employee():
    """This method tasks takes no argument. The function ask the user
    to input a search string to search for employees that entered
    tasks in the database. I presents these name to the user and let him
    choose a full name from the list. A list of tasks in the database with
    the choosen names is returned. """
    # Concatenate first name with family name to search in both names
    concat_name = dbInteraction.TaskEntry.first_name.concat(' ').concat(
        dbInteraction.TaskEntry.family_name)
    # Extract tasks for database
    tasks = dbInteraction.TaskEntry.select(concat_name)
    # End the method if no task is available
    if len(tasks) == 0:
        return []
    # Ask the user for a employee to search for
    user_input = input('Please key a name or press enter to obtain a list.')
    # Database query
    found_tasks = (dbInteraction.TaskEntry
                   .select(dbInteraction.TaskEntry.first_name,
                           dbInteraction.TaskEntry.family_name)
                   .where(concat_name.contains(user_input))
                   .order_by(concat_name)
                   .distinct())
    # End the method if no task was found
    if len(found_tasks) == 0:
        return []
    # Print explanation to user
    print("\nHere is a list of names to choose tasks from:")
    # Print names to console
    index = 0
    for task in found_tasks:
        index += 1
        print(str(index) + ': ' + str(task.first_name) +
              ' ' + str(task.family_name))
    while True:
        user_input = input("Please choose a name by choosing a number: ")
        choice = 0
        try:
            choice = int(user_input)
            if 0 < choice and choice <= index:
                break
            else:
                text = "This number was not given as choice. "
                print(text + "Please try again.")
        except ValueError:
            print("That was not a number input.")
    # Quries for the choosen name
    found_tasks = dbInteraction.TaskEntry.select().\
        where(dbInteraction.TaskEntry.first_name ==
              found_tasks[choice-1].first_name,
              dbInteraction.TaskEntry.family_name ==
              found_tasks[choice-1].family_name).\
        order_by(dbInteraction.TaskEntry.due_date.desc())
    return found_tasks


def search_by_date():
    """This method takes self as argument. It get the tasks dates as a
    list from the database and guides the user to chose tasks with
    a specific date from the given list. It returns a list with eventually
    found tasks."""
    # Extract tasks for database
    tasks = dbInteraction.TaskEntry.select(dbInteraction.TaskEntry.due_date)\
        .order_by(dbInteraction.TaskEntry.due_date).distinct()
    # End the method if not task is available
    if len(tasks) == 0:
        return []
    # Print explanation to user
    print("Here is a list of dates to choose tasks from:")
    # Print dates to console
    index = 0
    # Get dates in a list
    utc_date_list = []
    for task in tasks:
        index += 1
        print(str(index) + ': ' + utility.convert_utcdate_to_datestring(
            task.due_date))
        utc_date_list.append(task.due_date)
    while True:
        user_input = input("Please choose a date by choosing a number: ")
        choice = 0
        try:
            choice = int(user_input)
            if 0 < choice and choice <= index:
                break
            else:
                text = "This number was not given as choice. "
                print(text + "Please try again.")
        except ValueError:
            print("That was not a number input.")
    chosen_date = utc_date_list[choice-1]
    found_tasks = []
    # Database query
    found_tasks = dbInteraction.TaskEntry.select().\
        where(dbInteraction.TaskEntry.due_date == chosen_date)
    return found_tasks


def search_by_range_of_dates():
    """This method takes self as argument. It get the tasks as a
    list from the text file and guides the user to search tasks within
    a specific range of dates. It returns a list with eventually found
    tasks."""
    # End the method if not task is available
    tasks = dbInteraction.TaskEntry.select().order_by(dbInteraction.
                                                      TaskEntry.
                                                      due_date.desc())
    if len(tasks) == 0:
        return []
    # Ask for a search date
    print("\nIn which period of time has the task been assinged for? ")
    while True:
        date_input = input("Please use MM/DD/YYYY-MM/DD/YYYY format. ")
        try:
            date_start, date_end = date_input[:10], date_input[11:21]
            utc_date_start = utility.convert_datetime_to_utc(date_start)
            utc_date_end = utility.convert_datetime_to_utc(date_end)
            break
        except ValueError:
            print("'{}' doesn't seem to be valid dates.".format(
                date_input))
    # Database query
    found_tasks = tasks.where(dbInteraction.TaskEntry.
                              due_date > utc_date_start,
                              dbInteraction.TaskEntry.
                              due_date < utc_date_end)
    return found_tasks


def search_by_exact_pattern():
    """This method takes self as argument and allows the user to
    key in a search string. It then loops over all the tasks to
    find the exact string. A list of a tasks with matches string is
    returned."""
    # Extract tasks for database
    tasks = dbInteraction.TaskEntry.select().order_by(dbInteraction.
                                                      TaskEntry.
                                                      due_date.desc())
    # End the method if not task is available
    if len(tasks) == 0:
        return []
    # Ask for the name of the task
    text = "Please key in the exact search term of the task. "
    search_input = input(text)
    found_tasks = []
    for task in tasks:
        if search_input in task.task_title or search_input in task.notes:
            found_tasks.append(task)
    return found_tasks


def search_by_timespent():
    """This method takes self as argument and allows the user to
    search tasks by the time spent on the task. It then loops over all
    the tasks to find the exact amount of time spent in minutes.
    A list of a tasks with matches string is returned."""
    # Extract tasks for database
    tasks = dbInteraction.TaskEntry.select().order_by(dbInteraction.
                                                      TaskEntry.
                                                      due_date.desc())
    # End the method if not task is available
    if len(tasks) == 0:
        return []
    # Get spent times in a list
    time_spent_list = []
    for task in tasks:
        time_spent_list.append(task.time_spent)
    # Remove duplicates and sort the list
    time_spent_list = sorted(list(set(time_spent_list)))
    times = []
    for time_spent in time_spent_list:
        # Parse utc datetime to date string
        times.append(time_spent)
    # Print explanation to user
    print("Here is a list of time spent on a task to choose tasks from:")
    # Print times to console
    index = 0
    for time in times:
        index += 1
        print(str(index) + ': ' + utility.convert_minutes_time_format(time))
    while True:
        user_input = input("Please choose a time spent by choosing a number: ")
        choice = 0
        try:
            choice = int(user_input)
            if 0 < choice and choice <= index:
                break
            else:
                text = "This number was not given as choice. "
                print(text + "Please try again.")
        except ValueError:
            print("That was not a number input.")
    chosen_time = times[choice - 1]
    found_tasks = []
    # Database query
    found_tasks = tasks.where(dbInteraction.TaskEntry.
                              time_spent == chosen_time)
    return found_tasks


checker = pep8.Checker('taskSearch.py')
checker.check_all()
