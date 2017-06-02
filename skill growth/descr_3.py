from myorm import Model, BirthdayField, NameField, PhoneField
from datetime import datetime


class Person(Model):

    def __init__(self): ### Надо ПЕРЕДЕЛАТЬ - если делать через инит, то дальше обьекты-дискрипторы будут перезаписаны обычной строкой
        self.name = NameField()
        self.birthday = BirthdayField()
        self.phone = PhoneField()


if __name__ == "__main__":
    p = Person()
    p.name = "Me"
    p.phone = "133 13 1331313"
    p.save(prim_key='name') # All changes saved
    p.birthday = datetime.strptime("1011-12-13", "%Y-%m-%d")
    p.save(prim_key='name')
    p2 = Person()
    p2.name = "Else"
    p2.save(prim_key='name')