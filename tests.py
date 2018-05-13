#!/user/bin/env python

import unittest
from unittest.mock import patch
import coverage
from peewee import *
import datetime
import pytz
import dateutil
import os
import pep8

import worklogMain
import uiAddEditTasks
import taskSearch
import dbInteraction
import utility


# ------------------------------------------------------------------
class worklogMainTest(unittest.TestCase):
    def setUp(self):
        """Test the addition of a task to the Database."""
        self.first_name = 'taskSearchTestfn'
        self.family_name = 'taskSearchTestln'
        self.title = 'testSearchtask'
        self.date = '11/11/5555'
        self.time_spent = 10000000
        self.notes = 'testTaskSearchNotes'
        self.MENU_OPTIONS, self.SEARCH_OPTIONS, self.S_RESULT_OPTIONS\
            = worklogMain.ui_initialization()

    def add_task_to_DB(self, first_name, family_name, title, date,
                       time_spent, notes):
        """Test the addition of a task to the Database."""
        dbInteraction.add_task_to_db(first_name,
                                     family_name,
                                     title,
                                     utility.convert_datetime_to_utc(date),
                                     time_spent,
                                     notes)

    def test_initialize_database(self):
        """Test the creation of the database"""
        dbInteraction.db.close()
        dbInteraction.initialize_database()
        self.assertTrue(os.path.isfile('worklog.db'))

    def test_db_teardown(self):
        dbInteraction.teardown()
        self.assertTrue(dbInteraction.db.is_closed(), True)

    def test_do_nothing(self):
        self.assertEqual(worklogMain.do_nothing(), None)

    def test_welcome_message(self):
        print('\n--- test_welcome_message ---')
        worklogMain.welcome_message()

    @patch('builtins.input', side_effect=['t', '3', 'a'])
    def test_show_main_menu(self, mock):
        """Test for the entering the add a task menu"""
        print('\n--- test_show_main_menu ---')
        worklogMain.show_main_menu(self.MENU_OPTIONS)

    @patch('builtins.input', side_effect=['3', 'k', 'b'])
    def test_show_search_menu(self, mock):
        """Test for the entering the add a task menu"""
        print('\n--- show_search_menu ---')
        worklogMain.show_search_menu(self.SEARCH_OPTIONS)

    @patch('builtins.input')
    def test_show_search_result(self, mock):
        """Test for the entering the add a task menu"""
        # Add a test task to the database
        self.add_task_to_DB(self.first_name,
                            self.family_name,
                            self.title,
                            self.date,
                            self.time_spent,
                            self.notes)
        # query tasks
        found_tasks = dbInteraction.TaskEntry.select().\
            where(dbInteraction.TaskEntry.first_name == self.first_name)
        # test the employee search method
        print('\n--- test_show_search_result ---')
        mock.side_effect = ['4', 'p', 'p', 'n', 'n', 'd', 'n', 'r']
        found_tasks = worklogMain.show_search_result(found_tasks)
        # query for created task to remove it again
        found_tasks = dbInteraction.TaskEntry.select().\
            where(dbInteraction.TaskEntry.first_name == self.first_name)

    @patch('builtins.input')
    def test_running(self, mock):
        """Test for the entering the add a task menu"""
        # test the employee search method
        print('\n--- test_running ---')
        mock.side_effect = ['b', 'n', 'f', 'c']
        worklogMain.running()


# ----------------------------------------------------------------------------
class uiAddEditTasksTest(unittest.TestCase):
    def setUp(self):
        """Test the addition of a task to the Database."""
        self.first_name = '90df8sd0234234aaa'
        self.family_name = 'skywalker_main'
        self.title = 'testAddEdit'
        self.date = '03/03/2000'
        self.time_spent = 2342309428234
        self.notes = 'testnotes'

    def add_task_to_DB(self, first_name, family_name,
                       title, date, time_spent, notes):
        """Test the addition of a task to the Database."""
        dbInteraction.add_task_to_db(first_name,
                                     family_name,
                                     title,
                                     utility.convert_datetime_to_utc(date),
                                     time_spent,
                                     notes)

    @patch('builtins.input')
    def test_add_task_ui(self, mock):
        """Test for the entering the add a task menu"""
        print('\n--- test_add_task_ui ---')
        mock.side_effect = ['testfn',
                            'testln',
                            'testtn',
                            '01/01/0001',  # wrong date 1
                            '03/13/1000',  # wrong date 2
                            '12/31/9999',  # wring date format
                            'notInteger',  # not a integer
                            '999',  # minutes spent
                            'testnotes']
        uiAddEditTasks.add_task_ui()
        # query for created task to remove it again
        found_tasks = dbInteraction.TaskEntry.select().\
            where(dbInteraction.TaskEntry.first_name == 'testfn')
        found_tasks[0].delete_instance()

    @patch('builtins.input')
    def test_edit_task(self, mock):
        """Test for the entering the add a task menu"""
        # Add a task dummy task in order to edit it.
        self.add_task_to_DB(self.first_name,
                            self.family_name,
                            self.title,
                            self.date,
                            self.time_spent,
                            self.notes)
        # query for created task to edit it
        found_task = dbInteraction.TaskEntry.select().\
            where(dbInteraction.TaskEntry.first_name == self.first_name)
        # Actally test the method
        print('\n--- test_edit_task ---')
        mock.side_effect = ['e',
                            'test',
                            '13/13/1111',
                            '11/11/1111',
                            '111',
                            'r']
        uiAddEditTasks.edit_task(found_task[0])
        # query for created task to remove it again
        found_tasks = dbInteraction.TaskEntry.select().\
            where(dbInteraction.TaskEntry.first_name == self.first_name)
        found_tasks[0].delete_instance()


# ----------------------------------------------------------------------------
class taskSearchTest(unittest.TestCase):
    def setUp(self):
        """Test the addition of a task to the Database."""
        self.first_name = 'taskSearchTestfn'
        self.family_name = 'taskSearchTestln'
        self.title = 'testSearchtask'
        self.date = '11/11/5555'
        self.time_spent = 10000000
        self.notes = 'testTaskSearchNotes'

    def add_task_to_DB(self, first_name, family_name, title, date,
                       time_spent, notes):
        """Test the addition of a task to the Database."""
        dbInteraction.add_task_to_db(first_name,
                                     family_name,
                                     title,
                                     utility.convert_datetime_to_utc(date),
                                     time_spent,
                                     notes)

    @patch('builtins.input')
    def test_search_by_employee(self, mock):
        """Test for the entering the add a task menu"""
        # Add a test task to the database
        self.add_task_to_DB(self.first_name,
                            self.family_name,
                            self.title,
                            self.date,
                            self.time_spent,
                            self.notes)
        # test the employee search method
        print('\n--- test_search_by_employee ---')
        mock.side_effect = ['',  # enter empty string to create a list
                            '-1',  # pick first entry
                            'z',  # not an integer
                            '1',  # wrong entry 1
                            'n',  # next
                            'r']  # return
        found_tasks = taskSearch.search_by_employee()
        # query for created task to remove it again
        found_tasks = dbInteraction.TaskEntry.select().\
            where(dbInteraction.TaskEntry.first_name == self.first_name)
        found_tasks[0].delete_instance()

    @patch('builtins.input')
    def test_search_by_date(self, mock):
        """Test search by date method"""
        # Add a test task to the database
        self.add_task_to_DB(self.first_name,
                            self.family_name,
                            self.title,
                            self.date,
                            self.time_spent,
                            self.notes)
        # test the employee search method
        print('\n--- test_search_by_date ---')
        mock.side_effect = ['',
                            'not',  # wrong format
                            '-1',  # not existing choice
                            '1',  # right date
                            'n',  # next
                            'r']  # return
        found_tasks = taskSearch.search_by_date()
        # query for created task to remove it again
        found_tasks = dbInteraction.TaskEntry.select().\
            where(dbInteraction.TaskEntry.first_name == self.first_name)
        found_tasks[0].delete_instance()

    @patch('builtins.input')
    def test_search_by_range_of_dates(self, mock):
        """Test search by date method"""
        # Add a test task to the database
        self.add_task_to_DB(self.first_name,
                            self.family_name,
                            self.title,
                            self.date,
                            self.time_spent,
                            self.notes)
        # test the employee search method
        print('\n--- test_search_by_range_of_dates ---')
        mock.side_effect = ['not',  # wrong format
                            '02/01/0001-12/31/9998',
                            '1',  # right date
                            'n',  # next
                            'r']  # return
        found_tasks = taskSearch.search_by_range_of_dates()
        # query for created task to remove it again
        found_tasks = dbInteraction.TaskEntry.select().\
            where(dbInteraction.TaskEntry.first_name == self.first_name)
        found_tasks[0].delete_instance()

    @patch('builtins.input')
    def test_search_by_exact_pattern(self, mock):
        """Test search by date method"""
        # Add a test task to the database
        self.add_task_to_DB(self.first_name,
                            self.family_name,
                            self.title,
                            self.date,
                            self.time_spent,
                            self.notes)
        # Test the employee search method
        print('\n--- test_search_by_exact_pattern ---')
        mock.side_effect = ['testTaskSearchNotes',  # wrong format
                            'n',  # next
                            'r']  # return
        found_tasks = taskSearch.search_by_exact_pattern()
        # query for created task to remove it again
        found_tasks = dbInteraction.TaskEntry.select().\
            where(dbInteraction.TaskEntry.first_name == self.first_name)
        found_tasks[0].delete_instance()

    @patch('builtins.input')
    def test_search_by_timespent(self, mock):
        """Test search by date method"""
        # Add a test task to the database
        self.add_task_to_DB(self.first_name,
                            self.family_name,
                            self.title,
                            self.date,
                            self.time_spent,
                            self.notes)
        # test the employee search method
        print('\n--- test_search_by_timespent ---')
        mock.side_effect = ['notinteger',  # not an integer
                            '-1',  # invalid number
                            '1',  # valid choice
                            'n',  # next
                            'r']  # return
        found_tasks = taskSearch.search_by_timespent()
        # query for created task to remove it again
        found_tasks = dbInteraction. \
            TaskEntry.select().where(dbInteraction.
                                     TaskEntry.
                                     first_name == self.first_name)
        found_tasks[0].delete_instance()


# ----------------------------------------------------------------------------
class utilityTest(unittest.TestCase):
    def test_convert_utcdate_to_datestring(self):
        utc_date = '2000-03-02 23:00:00+00:00'
        result = '03/03/2000'
        self.assertEqual(utility.convert_utcdate_to_datestring(utc_date),
                         result)
        # raise error when input not aware
        with self.assertRaises(AttributeError):
            utility.convert_utcdate_to_datestring(datetime.datetime.now())
        # raise error when input not datetime.datetime format not aware
        with self.assertRaises(ValueError):
            utility.convert_utcdate_to_datestring('2000-03-02 23:00:00')

    def test_convert_datetime_to_utc(self):
        """Takes a datetime format information and localizes it with
            pytz to 'Europe/Paris' and returns utc."""
        date_input = '03/03/2000'
        # Test
        self.assertEqual(str(utility.convert_datetime_to_utc('03/03/2000')),
                         '2000-03-02 23:00:00+00:00')
        # check to convert a native datetime to an aware pytz format
        with self.assertRaises(ValueError):
            utility.convert_datetime_to_utc('03/03/20004')
        with self.assertRaises(ValueError):
            utility.convert_datetime_to_utc('03*03/2000')
        with self.assertRaises(OverflowError):
            utility.convert_datetime_to_utc('01/01/0001')

    def test_convert_minutes_time_format(self):
        """This function converts input argument minutes to hours and minutes
         to a printable format. This information is returned a string like
         this: xx Hours xx Minutes (=> xxx Minutes)"""
        minutes = 3
        result_string = '0 Hours 3 Minutes (=> 3 Minutes)'
        self.assertEqual(utility.convert_minutes_time_format(minutes),
                         result_string)
        minutes = 39393
        result_string = '656 Hours 33 Minutes (=> 39393 Minutes)'
        self.assertEqual(utility.convert_minutes_time_format(minutes),
                         result_string)
        with self.assertRaises(ValueError):
            utility.convert_minutes_time_format('e')
        with self.assertRaises(ValueError):
            utility.convert_minutes_time_format('3')


class DBInteractionTest(unittest.TestCase):
    def setUp(self):
        """Test the addition of a task to the Database."""
        self.first_name = '90df8sd09fs8d0f9sds'
        self.family_name = 'skywalker'
        self.title = 'thisss'
        self.date = '03/03/2000'
        self.time_spent = 2342309428234
        self.notes = 'testnotes'

    def test_initialize_database(self):
        """Test the creation of the database"""
        dbInteraction.db.close()
        dbInteraction.initialize_database()
        self.assertTrue(os.path.isfile('worklog.db'))

    def test_add_task_to_DB(self):
        """Test the addition of a task to the Database."""
        dbInteraction.add_task_to_db(self.first_name,
                                     self.family_name,
                                     self.title,
                                     utility.convert_datetime_to_utc(
                                         self.date),
                                     self.time_spent,
                                     self.notes)
        all_tasks = dbInteraction.TaskEntry.select()
        test_task = all_tasks.where(dbInteraction.
                                    TaskEntry.
                                    first_name == self.first_name).get()
        self.assertEqual(test_task.first_name, self.first_name)
        self.assertEqual(test_task.family_name, self.family_name)
        self.assertEqual(test_task.task_title, self.title)
        self.assertEqual(utility.convert_utcdate_to_datestring(
            test_task.due_date), self.date)
        self.assertEqual(test_task.time_spent, self.time_spent)
        self.assertEqual(test_task.notes, self.notes)
        test_task.delete_instance()

    def test_view_task(self):
        dbInteraction.add_task_to_db(self.first_name,
                                     self.family_name,
                                     self.title,
                                     utility.convert_datetime_to_utc(
                                         self.date),
                                     self.time_spent,
                                     self.notes)
        test_task = dbInteraction.TaskEntry.select().\
            where(dbInteraction.TaskEntry.first_name == self.first_name).get()
        result = """============================================================
Task title: thisss
============================================================
Employee's first name: 90df8sd09fs8d0f9sds
Employee's last name: skywalker
Task's due date: 03/03/2000
Time spent on task: 39038490470 Hours 34 Minutes (=> 2342309428234 Minutes)
Notes: testnotes
============================================================"""
        self.assertEqual(dbInteraction.view_task(test_task), result)
        test_task.delete_instance()

    def test_delete_task_from_DB(self):
        dbInteraction.add_task_to_db(self.first_name,
                                     self.family_name,
                                     self.title,
                                     utility.convert_datetime_to_utc(
                                         self.date),
                                     self.time_spent,
                                     self.notes)
        test_task = dbInteraction.TaskEntry.select().\
            where(dbInteraction.TaskEntry.first_name == self.first_name).get()
        test_task.delete_instance()


if __name__ == '__main__':
    unittest.main()


checker = pep8.Checker('tests.py')
checker.check_all()
