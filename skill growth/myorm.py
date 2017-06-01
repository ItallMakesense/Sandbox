"""
For descr_3.py.
"""

from datetime import datetime
import sqlite3
import re


class Model(object):

    def data_convert(self, namespace):
        column_types = ",".join(["%s text" % name for name in namespace])
        column_names = ",".join(namespace)
        column_values = [str(getattr(self, attr)) for attr in namespace]
        db = sqlite3.connect("orm.db")
        gate = db.cursor()
        gate.execute("create table if not exists Persons (%s)" % column_types)
        gate.execute("insert into Persons ({}) values (?,?,?)".format(column_names), column_values)
        db.commit()
        print([line for line in gate.execute("Select * from Persons")])
        db.close()

    def save(self):
        filter_func = lambda attr: True if not attr.startswith('__') and\
                                   not callable(getattr(self, attr)) else False
        namespace = list(filter(filter_func, dir(self)))
        self.data_convert(namespace)


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
