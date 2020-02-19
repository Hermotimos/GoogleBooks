import datetime

from django import forms


def get_current_year():
    return datetime.datetime.now().year


def is_date_or_empty(date_str):
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
