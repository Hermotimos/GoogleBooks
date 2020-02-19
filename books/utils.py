"""Module for storing functions that may be used in multiple modules.

    get_current_year(): returns current date as int.
    is_date_or_empty(): check whether given string is a valid date or is empty.
"""

import datetime

from django import forms


def get_current_year():
    """Return current year as int."""
    return datetime.datetime.now().year


def is_date_or_empty(date_str):
    """
    Check whether string validates as a date against given date formats
    or as an empty string.
    
    Keyword arguments:
        date_str: string from user input in django.forms.SelectDateWidget
    
    Raises:
        If date_str is neither an empty string, nor a valid date as per
        comparison to the given date formats, ValidationError is raised with
        customized text prompting user to enter valid data.
    
    Returns:
        True if validation has been passed.
    """
    passed = True if date_str == '' else False
    formats = ('%Y-%m-%d', '%Y-%m', '%Y')
    for format_ in formats:
        try:
            datetime.datetime.strptime(date_str, format_)
            passed = True
        except ValueError:
            pass
    
    if passed:
        return True
    else:
        raise forms.ValidationError('Provide a valid date or none.')
