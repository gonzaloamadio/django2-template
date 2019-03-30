"""
Library with some generic functions to use along the code
"""
# -*- coding: utf-8 -*-

from datetime import datetime
from django.utils import timezone
import pytz
from random import randint

# ----------------------------------------------------------------------------
#                    Model functions
# ----------------------------------------------------------------------------

def model_field_names(model):
    """
    Returns a list of field names in the model
    Direct from Django upgrade migration guide.
    """
    return list(
        set(
            chain.from_iterable(
                (field.name, field.attname)
                if hasattr(field, "attname")
                else (field.name,)
                for field in model._meta.get_fields()
                if not (field.many_to_one and field.related_model is None)
            )
        )
    )

def model_field_attr(model, model_field, attr):
    """
    Returns the specified attribute for the specified field on the model class.
    """
    fields = dict([(field.name, field) for field in model._meta.fields])
    return getattr(fields[model_field], attr)

# ----------------------------------------------------------------------------
#                    Date functions
# ----------------------------------------------------------------------------

def make_utc(dt):
    """
        Convert a datetime to UTC
    """
    if timezone.is_naive(dt): # This line does not work
        dt = timezone.make_aware(dt)
    return dt.astimezone(pytz.utc)

def to_epoch(param_date, miliseconds=True):
    """
        The Unix epoch (or Unix time or POSIX time or Unix timestamp) is the
        number of seconds that have elapsed since January 1, 1970
    """
    seconds = int((param_date - datetime(1970, 1, 1)).total_seconds())
    if miliseconds:
        ret = seconds * 1000
    else:
        ret = seconds
    return ret


def this_year_naive():
    """
        Returns this year, number. No TZ aware
    """
    return int(datetime.now().year)

def this_year_aware():
    """
        Returns this year, number. No TZ aware
    """
    return int(timezone.now().year)

def weekday_to_str(num):
    """
        Translate weekday to string
    """
    data = {
        '0': 'mon',
        '1': 'tue',
        '2': 'wed',
        '3': 'thu',
        '4': 'fri',
        '5': 'sat',
        '6': 'sun',
    }

    return data.get(str(num))

# ----------------------------------------------------------------------------
#                    STRING FUNCTIONS
# ----------------------------------------------------------------------------

def between(value, a, b):
    # Find and validate before-part.
    pos_a = value.find(a)
    if pos_a == -1: return ""
    # Find and validate after part.
    pos_b = value.rfind(b)
    if pos_b == -1: return ""
    # Return middle part.
    adjusted_pos_a = pos_a + len(a)
    if adjusted_pos_a >= pos_b: return ""
    return value[adjusted_pos_a:pos_b]

def before(value, a, last_appearance=False):
    # Find first part and return slice before it.
    # If last_appearance=True, look a from right of string, i.e. last appearance
    if last_appearance:
        pos_a = value.rfind(a)
    else:
        pos_a = value.find(a)
    if pos_a == -1: return ""
    return value[0:pos_a]

def after(value, a, last_appearance=False):
    # Find and validate first part.
    # If last_appearance=True, look a from right of string, i.e. last appearance
    if last_appearance:
        pos_a = value.rfind(a)
    else:
        pos_a = value.find(a)

    if pos_a == -1: return ""
    # Returns chars after the found string.
    # Adjusted position, because find gives the first position of chain founded.
    adjusted_pos_a = pos_a + len(a)
    if adjusted_pos_a >= len(value): return ""
    return value[adjusted_pos_a:]


# ----------------------------------------------------------------------------
#                    Num functions
# ----------------------------------------------------------------------------

def gen_random_num_of_length(num):
    """
        Gen random number of n cyphers.
    """
    range_start = 10 ** (num - 1)
    range_end = (10 ** num) - 1
    return randint(range_start, range_end)

# ----------------------------------------------------------------------------
#                    Dict functions
# ----------------------------------------------------------------------------

# ####################
# FORMAT DICTIONARIES

# "data": [
# {
# "cost_price": 10,
# "id": 1,
# "valid": true
# .....
# }
# ],

#  FORMATED TO:

# "data": {
# "1" : {
# "cost_price": 10,
# "id": 1,
# "valid": true
# .....
# }
# },


def list_to_dict(lista):
    """
        Argument: list of objects.
        Output: Dict where key is the ID, and value the hole object.
    """
    ret = {}
    try:
        for obj in lista:
            clave = obj.get('id')
            if clave:
                ret[clave] = obj
        return ret
    except Exception as err:  # pylint: disable=unused-variable
        #        return ret
        raise Exception("[list_to_dict] Error processing data.")


