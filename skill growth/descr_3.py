from myorm import Model, BirthdayField, NameField, PhoneField


class Person(Model):

   name = NameField()
   birthday = BirthdayField()
   phone = PhoneField()


if __name__ == "__main__":
    p = Person()
    p.name = "Me"
    p.phone = "133 13 1331313"
    p.save() # All changes saved