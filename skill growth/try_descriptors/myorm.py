"""
Simple ORM using data descriptors (Name-, Birthday- and PhoneField),
which stores descriptor values in an SQLite database.

See module usage in descr_3.py.
"""

from datetime import datetime
import sqlite3
import re


class Model(object):

    def save(self, prim_key):
        filter_func = lambda attr: True if not attr.startswith('_')\
                                    and not callable(getattr(self, attr))\
                                    else False
        namespace = list(filter(filter_func, dir(self)))
        table_name = self.__class__.__name__
        column_names = ",".join(namespace)
        column_values = [str(getattr(self, attr)) for attr in namespace]
        column_types = ["%s text" % name for name in namespace]
        column_types = ["%s primary key" % col if prim_key in col\
                        else col for col in column_types]
        column_types = ",".join(column_types)

        db = sqlite3.connect("orm.db")
        gate = db.cursor()

        gate.execute("create table if not exists {} ({})".format(table_name, column_types))
        gate.execute("insert or replace into {} ({}) values (?,?,?)".format(\
                        table_name, column_names), column_values)
        db.commit()
        db.close()


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
