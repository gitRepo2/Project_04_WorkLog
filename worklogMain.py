#!/user/bin/env python
# Work-Log with database project
# Lukas Straumann, 14-May-2018, V1.0
import pep8
import os
from collections import OrderedDict

import taskSearch
import uiAddEditTasks
import dbInteraction


def do_nothing():
    pass


def welcome_message():
    """This method prints a start text in the console for the user."""
    clear_screen()
    print('Welcome to Work-Log Project 04.\n')


def show_main_menu(MENU_OPTIONS):
    """This method shows the main menu to the user and returns the
    user input choice e.g. 'b'. """
    while True:
        print('\nWhat would you like to do:\n')
        for menu_item in MENU_OPTIONS:
                print(MENU_OPTIONS[menu_item][0])
        user_input = input().lower()
        if user_input in MENU_OPTIONS:
            return user_input
        else:
            print("Your input: '{}' is not available in the menu. ".format(
                user_input))
            print("Please try again.\n")


def show_search_menu(SEARCH_OPTIONS):
    """This method shows the search sub menu and ask the user to choose
    an option. It returns a choise e.g. 'a'. """
    while True:
        print('\nWould you like to search: ')
        for menu_item in SEARCH_OPTIONS:
                print(SEARCH_OPTIONS[menu_item][0])
        user_input = input().lower()
        if user_input in SEARCH_OPTIONS:
            return user_input
        else:
            print("Your input: '{}' is not available in ".format(
                user_input))
            print("the search menu. Please try again.\n")


def quit_program():
    """This method prints a good bye message to the user."""
    print('\nYou decided to quit. Have a good day.')


def show_search_result(found_tasks):
    """This method task self and found_tasks list a argument and provides
    the user with a displayed task where he can chose options for the
    found tasks."""
    found_tasks = list(found_tasks)
    if len(found_tasks) == 0:
        print('\nNo task was found or available.')
    else:
        current = 0
        while True:
            if len(found_tasks) > 0:
                print('\nResult: {} out of {} found tasks shown:'.format(
                    current+1,
                    len(found_tasks)))
                print(dbInteraction.view_task(found_tasks[current]))
            else:
                print('No more tasks to show.')
            text1 = 'Choose [P]revious, [N]ext, [E]dit, [D]elete, '
            text2 = '[R]eturn as a next action.'
            user_input = input(text1+text2).lower()
            # Evaluate user input
            if user_input == 'p':
                current -= 1
            elif user_input == 'n':
                current += 1
            elif user_input == 'e':
                if len(found_tasks) > 0:
                    uiAddEditTasks.edit_task(found_tasks[current])
                    break
                else:
                    print('No more tasks to edit.')
            elif user_input == 'd':
                if len(found_tasks) > 0:
                    dbInteraction.delete_task_from_db(found_tasks[current])
                    found_tasks.pop(current)
                else:
                    print('No more tasks to delete.')
            elif user_input == 'r':
                break
            else:
                print("\n'{}' is not a valid input. Please try again.".format(
                    user_input))
            if current == len(found_tasks):
                current = 0
            if current == -1:
                current = len(found_tasks)-1


def clear_screen():
    """This method clears the console screen."""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def ui_initialization():
    """This function defines the menu options."""
    # Main menu options definition
    d = OrderedDict()
    d['a'] = ['a: Add a new task.', uiAddEditTasks.add_task_ui]
    d['b'] = ['b: Search for a task.', do_nothing]
    d['c'] = ['c: Quit the program.', quit_program]
    MENU_OPTIONS = d
    # search options definition
    d = OrderedDict()
    d['a'] = ['a: by a date', taskSearch.search_by_date]
    d['b'] = ['b: by a range of dates', taskSearch.search_by_range_of_dates]
    d['c'] = ['c: by an exact pattern', taskSearch.search_by_exact_pattern]
    d['d'] = ['d: by employee name', taskSearch.search_by_employee]
    d['e'] = ['e: by the time spent', taskSearch.search_by_timespent]
    d['f'] = ['f: Return to main menu', do_nothing]
    SEARCH_OPTIONS = d
    # Search result menu options definition
    d = OrderedDict()
    d['b'] = ['[P]revious', do_nothing]
    d['n'] = ['[N]ext', do_nothing]
    d['e'] = ['[E]dit', uiAddEditTasks.edit_task]
    d['d'] = ['[D]elete', dbInteraction.delete_task_from_db]
    d['r'] = ['[R]eturn', do_nothing]
    S_RESULT_OPTIONS = d
    return MENU_OPTIONS, SEARCH_OPTIONS, S_RESULT_OPTIONS


def running():
    """This function runs the top level user interaction."""
    MENU_OPTIONS, SEARCH_OPTIONS, S_RESULT_OPTIONS = ui_initialization()
    welcome_message()
    while True:
        next_menu = show_main_menu(MENU_OPTIONS)
        # Call next_menu method based on user input
        MENU_OPTIONS[next_menu][1]()
        if next_menu == 'c':
            break
        if next_menu == 'b':
            # Enter the sub menu 'search options'
            while True:
                next_menu = show_search_menu(SEARCH_OPTIONS)
                found_tasks = SEARCH_OPTIONS[next_menu][1]()
                if next_menu == 'f':
                    break
                show_search_result(found_tasks)


if __name__ == "__main__":
    dbInteraction.initialize_database()
    running()
    dbInteraction.teardown()

checker = pep8.Checker('worklogMain.py')
checker.check_all()
