"""Module for storing functions that may be used in multiple modules.

    get_current_year(): returns current date as int.
    get_date_or_empty(): return valid date from string or empty string.
"""

import datetime

from django import forms


def get_current_year():
    """Return current year as int."""
    return datetime.datetime.now().year


def get_date_or_empty(date_str):
    """
    Check whether string validates as a date against given date formats
    or as an empty string and return the result.
    
    Keyword arguments:
        date_str: string from user input in django.forms.SelectDateWidget
    
    Raises:
        If date_str is neither an empty string, nor a valid date
        ValidationError is raised with customized text prompting user to enter
        valid data.
    
    Returns:
        1) Empty string if argumement is an empty string.
        2) Valid date if string argument forms a valid date.
    """
    if date_str == '':
        return date_str
    else:
        date_list = date_str.split('-')
        [year, month, day] = date_list
    
        if int(year) and int(month) and int(day):
            return date_str
        elif int(year) and int(month):
            return year + '-' + month
        elif int(year) and int(day):
            raise forms.ValidationError('Provide a valid date or none.')
        elif int(year):
            return year
        else:
            raise forms.ValidationError('Provide a valid date or none.')
