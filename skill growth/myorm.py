"""
For descr_3.py.
"""

from datetime import datetime
import sqlite3
import re
import peewee


class Model(object):

    def write(self, namespace, prim_key):
        table_name = self.__class__.__name__
        obj_inx = table_name + str(self.__class__._count)
        # column_types = ",".join(["%s text" % name for name in namespace])
        columns = []
        for name in namespace:
            if name == prim_key:
                columns.append("%s text primary key" % name)
                continue
            columns.append("%s text" % name)
        column_types = ",".join(columns)
        column_names = ",".join(namespace)
        column_values = [str(getattr(self, attr)) for attr in namespace]
        print(namespace)
        print(column_values)
        db = sqlite3.connect("orm.db")
        gate = db.cursor()
        gate.execute("create table if not exists {} ({})".format(table_name, column_types))
        update_values = ",".join(["%s=\"%s\"" % pair for pair in zip(namespace, column_values)])
        gate.execute("insert or replace into {} ({}) values (?,?,?)".format(\
                        table_name, column_names), column_values)
        db.commit()
        print([line for line in gate.execute("select * from %s" % table_name)])
        db.close()

    def save(self, prim_key):
        filter_func = lambda attr: True if not attr.startswith('_') and\
                                   not callable(getattr(self, attr))\
                                   else False
        namespace = list(filter(filter_func, self.__dict__))
        self.write(namespace, prim_key)

    def __getattribute__(self, name):
        if name.startswith("__") or name == "save":
            return super().__getattribute__(name)
        else:
            obj = self
            obj_type = type(self)
            self = obj.__dict__[name]
            print(obj, obj_type, self)
            return self.__get__(obj, obj_type)


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
