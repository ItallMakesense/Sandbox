from myorm import Model, BirthdayField, NameField, PhoneField
from datetime import datetime


class Person(Model):

   name = NameField()
   birthday = BirthdayField()
   phone = PhoneField()


if __name__ == "__main__":
    p = Person()
    p.name = "Me"
    p.phone = "133 13 1331313"
    p.save() # All changes saved
    p.birthday = datetime.strptime("1011-12-13", "%Y-%m-%d")
    p.save()