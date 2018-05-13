import regex
import pytz
import dateutil
import datetime
import pep8


def convert_datetime_to_utc(date_input):
    """Takes a string like 03/03/2018 information and localizes it with
    pytz to 'Europe/Paris' and returns utc."""
    parsed_datetime = datetime.datetime.strptime(date_input, '%m/%d/%Y')
    local_date = pytz.timezone('Europe/Paris').localize(parsed_datetime)
    utc_date = local_date.astimezone(pytz.utc)
    return utc_date


def convert_utcdate_to_datestring(utc_date):
    """This function take a pytz utc date like:
    '2000-03-02 23:00:00+00:00' and converts it to a '03/03/2000'
    formated string. This is returned."""
    # Parse string to datetime
    datetime = dateutil.parser.parse(utc_date)
    # Convert date from UTC to local
    astimezone_date = datetime.astimezone(pytz.timezone('Europe/Paris'))
    # Convert datetime to a date string
    return astimezone_date.strftime("%m/%d/%Y")


def convert_minutes_time_format(input):
    """This function converts input argument minutes to hours and minutes to
    a printable format. This information is returned a string like this:
    xx Hours xx Minutes (=> xxx Minutes)"""
    if isinstance(input, int):
        pass
    else:
        raise ValueError("The argument could not be converted to an int.")
    hours, minutes = input // 60, input % 60
    output = str(hours) + ' Hours ' + str(minutes) + ' Minutes'
    output += ' (=> ' + str(input) + ' Minutes)'
    return output


checker = pep8.Checker('utility.py')
checker.check_all()
