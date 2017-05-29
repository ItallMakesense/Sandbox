"""
For descr_3.py.
"""

from datetime import datetime
import re


class Model(object):

    def save(self):
        filter_func = lambda attr: not attr.startswith('__')
        class_names = filter(filter_func, self.__class__.__dict__)
        namespace = filter(filter_func, dir(self))
        print([self.__class__.__dict__[name] for name in class_names])
        print([getattr(self, attr) for attr in namespace])


class NameField(object):

    def __init__(self):
        self._name = None

    def __get__(self, obj, obj_type):
        return self._name

    def __set__(self, obj, name):
        if isinstance(name, str):
            self._name = name
        else:
            raise TypeError("Name must be str type")

    def __repr__(self):
        return self.__class__.__name__


class BirthdayField(object):

    def __init__(self):
        self._bday = None

    def __get__(self, obj, obj_type):
        return self._bday

    def __set__(self, obj, date):
        if isinstance(date, datetime):
            self._bday = date
        else:
            raise TypeError("Birthday must be datetime type")

    def __repr__(self):
        return self.__class__.__name__


class PhoneField(object):

    def __init__(self):
        self._phone = None

    def __get__(self, obj, obj_type):
        if self._phone:
            return re.sub(r'(\d{3}) (\d{2}) (\d{3})(\d{2})(\d{2})',\
                            r'\1 (\2) \3-\4-\5', self._phone)

    def __set__(self, obj, phone):
        if re.match(r'\d{3} \d{2} \d{7}', phone):
            self._phone = phone
        else:
            raise ValueError("Phone must be in format XXX XX XXXXXXX")

    def __repr__(self):
        return self.__class__.__name__
