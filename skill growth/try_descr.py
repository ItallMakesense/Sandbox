# """
# 1st case
# """

# from datetime import datetime
# from fields import BirthdayField, NameField, PhoneField


# class Person(object):
#     name = NameField()
#     birthday = BirthdayField()
#     phone = PhoneField()

# if __name__ == "__main__":
#     me = Person()
#     print("%s, %s, %s" % (me.name, me.birthday, me.phone))
#     me.name = "Me"
#     me.birthday = datetime.strptime("1011-12-13", "%Y-%m-%d")
#     me.phone = "012 34 5678910"
#     print("%s, %s, %s" % (me.name, me.birthday, me.phone))
#     # me.name = None
#     # me.birthday = "Day 13"
#     # me.phone = "012 (34) 567-89-10"
###############################################################################
"""
2nd case
"""

from doclib import DocAPI


class Foo(object):
    __doc__ = DocAPI()
    def __init__(self, x):
        self.x = x
    def meth(self, y):
        """Multiplies two values self.x and y."""
        return self.x * y

if __name__ == "__main__":
    print(Foo.__doc__)
    foo = Foo(10)
    print(foo.__doc__)